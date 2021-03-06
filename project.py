from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Making an API endpoint 
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menu_id).one()
	return jsonify(MenuItems=[item.serialize])

@app.route('/')
#app.route('/home')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id):
	#restaurant = session.query(Restaurant).first()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items = items)

	# Embedding HTML within the Python script is not a best practice
	# output = ''
	# for item in items:
	# 	output += item.name
	# 	output += '<br>'
	# 	output += item.price
	# 	output += '<br>'
	# 	output += item.description
	# 	output += '<br><br>'
	# return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash('New item has been created')
		return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedMenuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		editedMenuItem.name = request.form['name']
		session.add(editedMenuItem)
		session.commit()
		flash('Item has been edited')
		return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, 
			menu_id = menu_id, i = editedMenuItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedMenuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
    	session.delete(deletedMenuItem)
    	session.commit()
    	flash('Item has been deleted')
    	return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
    	return render_template('deletemenuitem.html', restaurant_id = restaurant_id,
    		menu_id = menu_id, item = deletedMenuItem)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)