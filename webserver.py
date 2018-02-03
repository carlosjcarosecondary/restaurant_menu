from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

# Objectives
# 1. List out all restaurants --> DONE
# 2. Each restaurant must have 'Edit' and 'Delete' buttons --> DONE
# 3. Create new restaurants (Admin)
# 4. Rename a restaurant
# 5. Delete a restaurant

####################################################
# Connecting to the database
####################################################

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

####################################################
# Client code
####################################################
class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
	 	self.send_header('content-type','text/html')
	 	self.end_headers()

	 	if self.path.endswith("/home"):
	 		restaurants = session.query(Restaurant).all()

	 		output = "<html><body>"
	 		output += "<header>"
		 	output += "<h1>Restaurant Project</h1>"
		 	output += "<h2><a href='/addmore'>Add a restaurant</a><h2>"
		 	output += "</header>"
		 	for restaurant in restaurants:
		 		output += "<section>"
		 		output += "<h2>%s<h2>"%restaurant.name
				#output += "<a href='#''>Edit</a>"
				#output += "<a href='#''>Delete</a>"
				output += """<form method='POST' enctype='multipart/form-data'  action='/edit'>
	 					<input type='submit' value='Edit'></form>
	 					<form method='POST' enctype='multipart/form-data'  action='/delete'>
	 					<input type='submit' value='Delete'></form>"""
				output += "</section>"
		 		output += """<style>
		 				header {
		 					text-align: center;
		 					margin-bottom: 5%;}


		 				body {background: #a7a7a7;}

		 				a {font-size:0.75em;}

		 				section {border-bottom: solid blue 2px;
		 				 		  margin-left: 5%;
		 				 		  margin-right: 5%;}

		 				section a {margin-right: 2.5%;`}
		 				</style>"""
		 	self.wfile.write(output) 

	 	if self.path.endswith("/addmore"):
	 		output = " "
	 		output += "<html><body>"
	 		output += "<header>"
		 	output += "<h1>Restaurant Project</h1>"
		 	output += "</header>"
	 		output += "<h3>What's name of the new restaurant?</h3>"
	 		output += """<form method='POST' enctype='multipart/form-data'  action='/addmore'>
	 					<input name='name' type='text'>
	 					<input type='submit' value='Add'>
	 					</form>"""

		 	output += """<style>
		 				header {
		 					text-align: center;
		 					margin-bottom: 5%;}


		 				body {background: #a7a7a7;}

		 				a {font-size:0.75em;}

		 				h3, form {margin-left: 5%;
		 				 	margin-right: 5%;}
						 
		 				</style>"""
	 		self.wfile.write(output)

	 	return	
	
	def do_POST(self):
		self.send_response(302)
	 	self.send_header('content-type','text/html')
	 	self.end_headers()

		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		test = cgi.FieldStorage()

	 	if ctype == 'multipart/form-data':
	 		fields = cgi.parse_multipart(self.rfile, pdict)
	 		messagecontent = fields.get('name')
	 		new_restaurant = Restaurant(name = messagecontent[0])
	 		session.add(new_restaurant)
	 		session.commit()

			output = ""
	 		output += "<html><body>"
	 		output += "<header>"
		 	output += "<h1>Restaurant Project</h1>"
		 	output += "</header>"
	 		output += "<h3>What's name of the new restaurant?</h3>"
	 		output += """<form method='POST' enctype='multipart/form-data'  action='/addmore'>
	 					<input name='name' type='text'>
	 					<input type='submit' value='Submit'>
	 					</form>"""
			output += "<h3>Thank you!</h3>"
	 		output += "<h4>Please click <a href='/home'>here</a> to return back</h4>"
	 		output += "</html></body>"
	 		output += """<style>
		 				header {
		 					text-align: center;
		 					margin-bottom: 5%;}


		 				body {background: #a7a7a7;}

		 				a {font-size:0.75em;}

		 				h3, h4, form {margin-left: 5%;
		 				 	margin-right: 5%;}

		 				 
		 				</style>"""
	 		self.wfile.write(output)

		return

####################################################
# Server code
####################################################

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print("Web server running on port %s" % port)
		server.serve_forever()

	except KeyboardInterrupt:
		print("^C entered, stopping web server ...")
		server.socket.close()

if __name__ == '__main__':
	main()