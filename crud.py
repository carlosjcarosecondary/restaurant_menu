from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Establishing what DB to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')

# Connecting the engine to the Base class
Base.metadata.bind = engine

# Session maker onject to connect our code
# executions and the engine just created
DBSession = sessionmaker(bind = engine)

# A session allows us to write down all the commands
# we want to execute without sending them to the DB until
# we commit
session = DBSession()

#################################################
# CREATE
#################################################
# Adding content to the DB
myFirstRestaurant = Restaurant(name = "Pizza Palace")  
session.add(myFirstRestaurant)
session.commit()

# Query to view the DB content (verification)
session.query(Restaurant).all()

# cheesepizza = MenuItem('''
# 	name = 'Cheese Pizza', 
# 	description = 'Made with all natural indredients and
# 	fresh mozarella',
# 	course = 'Entree',
# 	price = '$8.99',
# 	restaurant = myFirstRestaurant''')

cheesepizza = MenuItem(
	name = 'Cheese Pizza', 
	description = 'Made with all natural indredients and fresh mozarella',
	course = 'Entree',
	price = '$8.99',
	restaurant = myFirstRestaurant)

session.add(cheesepizza)
session.commit()

# Query to view the DB content (verification)
session.query(MenuItem).all()

#################################################
# READ
#################################################
items = session.query(MenuItem).all()
for item in items:
	print(item.name)
	print(item.description)
	print(item.price)

#################################################
# UPDATE
#################################################
# 1. Find entry
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
UrbanVeggierBurger = session.query(MenuItem).filter_by(id = 8).one()

# 2. Reset values
UrbanVeggierBurger.price = '$2.99'

# 3. Add to session
session.add(UrbanVeggierBurger)

# 4. Session commi
session.commit()

#################################################
# DELETE
#################################################
# 1. Find entry
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()

# 2. Session delete
session.delete(spinach)

# 3. Session commit
session.commit()
