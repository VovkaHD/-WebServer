from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('/res'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = ""
                output += '''
                <span>Add a new Restaurant:</span>
                <form method='POST' enctype='multipart/form-data' action='/res/new'>
                    <input name="resName" type="text" placeholder="restaurant name">
                    <input type="submit" value="Submit">
                </form>'''
                output += "<p>Restaurants are: </p>"
                for res in restaurants:
                    output += res.name + '''
                    </br>
                    <a href='/res/{!s}/edit'>edit</a>
                    <a href='/res/{!s}/delete'>delete</a>
                    </br></br>'''.format(res.id, res.id)
                self.wfile.write(output)
                return
            if self.path.endswith('edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                id = self.path.split('/')[2]
                
                theRes = session.query(Restaurant).filter_by(id=id).one()
                
                output = '''
                <span>Edit a Restaurant name:</span>
                <form method='POST' enctype='multipart/form-data' action='/res/{!s}/edit'>
                    <input name="resName" type="text" placeholder="{!s}">
                    <input type="submit" value="Submit">
                </form>'''.format(id, theRes.name)
                self.wfile.write(output)
                
            if self.path.endswith('delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
    
                id = self.path.split('/')[2]
    
                theRes = session.query(Restaurant).filter_by(id=id).one()
    
                output = '''
                <span>Delete a Restaurant:</span>
                <form method='POST' enctype='multipart/form-data' action='/res/{!s}/delete'>
                    <p>Name: {!s}</p>
                    <input type="submit" value="Delete">
                </form>'''.format(id, theRes.name)
                self.wfile.write(output)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    def do_POST(self):
        try:
            if self.path.endswith('/res/new'):
            
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                resName = fields.get('resName')[0]

                newRes = Restaurant(name=resName)
                session.add(newRes)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/res')
                self.end_headers()

            if self.path.endswith('edit'):
    
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                resName = fields.get('resName')[0]
                id = self.path.split('/')[2]
                
                res = session.query(Restaurant).filter_by(id=id).one()
                res.name = resName
                session.commit()
    
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/res')
                self.end_headers()
                
            if self.path.endswith('delete'):
    
                # ctype, pdict = cgi.parse_header(
                #     self.headers.getheader('content-type'))
                # if ctype == 'multipart/form-data':
                #     fields = cgi.parse_multipart(self.rfile, pdict)
                id = self.path.split('/')[2]
    
                res = session.query(Restaurant).filter_by(id=id).one()
                session.delete(res)
                session.commit()
    
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/res')
                self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()