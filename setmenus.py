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

import json

category_json = json.loads(open('res_data.json', 'r').read())


for e in category_json['all_categories']:
  res = Restaurant(name=str(e['name']))
  session.add(res)
  session.commit()
  for m in e['menu']:
    menuItem = MenuItem(name=m['name'], description=m['description'], price=m['price'], restaurant=res)
    session.add(menuItem)
    session.commit()

print "added menu items!"
