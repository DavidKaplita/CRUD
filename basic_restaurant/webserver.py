#!/usr/bin/env python3

import http.server
import os
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from http.server import BaseHTTPRequestHandler, HTTPServer

#DBNAME="restaurantmenu"
DBNAME="sqlite:///restaurantmenu.db"
DEFAULT_RESTAURANT_LIMIT=100
db = create_engine(DBNAME)

# Comment out if not using binding ORM
Base.metadata.bind = db
DBSession = sessionmaker(bind=db)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    #def get_all_restaurants(self, db_connection, limit_num):
    #    """Return restaurants and limit the result."""
    #    rows = db_connection.execute("""
    #    SELECT name, id
    #    FROM Restaurant
    #    ORDER BY name ASC
    #    LIMIT """ + str(DEFAULT_RESTAURANT_LIMIT))
    #
    #    return rows

    #def get_restaurant(self, db_connection, id_number):
    #    """Return restaurants and limit the result."""
    #    rows = db_connection.execute("""
    #    SELECT name
    #    FROM Restaurant
    #    WHERE id = """ + str(id_number))
    #
    #    return rows

    def do_GET(self):
        try:

            if self.path == "/restaurants":
                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<body></html>\n"
                output += "  <h1>Restaurants</h1>\n"
                #conn = db.connect()
                #restaurants = self.get_all_restaurants(conn, DEFAULT_RESTAURANT_LIMIT)
                for restaurant in restaurants:
                    output += ("  <p><b>" + restaurant.name + "</b> -- <a href=\"/restaurants/" + str(restaurant.id) + "/edit\">Edit</a> / <a href=\"/restaurants/" + str(restaurant.id) + "/delete\">Delete</a></p>\n")
                #conn.close()
                output += "</body></html>\n"
                self.wfile.write(output.encode())
                print(output)
                return

            elif self.path == "/restaurants/new":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>\n"
                output += "<h1>Create Restaurant</h1>\n"
                output += "<p>Name</p>\n"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text" placeholder="New Restaurant Name"><input type="submit" value="Create"> </form>\n'''
                output += "</body></html>\n"
                self.wfile.write(output.encode())
                print(output)
                return

            elif self.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<body></html>\n"
                output += "  <h1>Links" + self.path + "</h1>\n"
                output += "  <p><a href=\"/restaurants\">List Restaurants</a></p>"
                output += "  <p><a href=\"/restaurants/new\">Create New Restaurant</a></p>"
                output += "</body></html>\n"
                self.wfile.write(output.encode())
                print(output)
                return

            elif self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>\n"
                    output += "<h1>Edit Restaurant</h1>\n"
                    output += "<p><b>Curent ID: " + restaurantIDPath + "</b></p>\n"
                    output += "<p><b>Curent Name: " + myRestaurantQuery.name + "</b></p>\n"
                    output += "<p><b>New Name:</b></p>\n"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/''' + restaurantIDPath + '''/edit'><input name="newRestaurantName" type="text" placeholder="New Restaurant Name"><input type="submit" value="Edit"> </form>\n'''
                    output += "</body></html>\n"
                    self.wfile.write(output.encode())
                    print(output)
                    return
                else:
                    self.send_response(422)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<body></html>\n"
                    output += "  <h1>Unknown restaurant ID \"" + restaurantIDPath + "\"</h1>\n"
                    output += "  <p>Please go back to the <a href=\"/\">home page</a>.</p>\n"
                    output += "</body></html>\n"
                    self.wfile.write(output.encode())
                    print(output)
                    return

            elif self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>\n"
                    output += "<h1>Delete Restaurant</h1>\n"
                    output += "<p>Are you sure you want to delete <b>" + myRestaurantQuery.name + "</b>?</p>\n"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/''' + restaurantIDPath + '''/delete'><input type="submit" value="Delete"> </form>\n'''
                    output += "</body></html>\n"
                    self.wfile.write(output.encode())
                    print(output.encode())
                    return
                else:
                    self.send_response(422)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<body></html>\n"
                    output += "  <h1>Unknown restaurant ID \"" + restaurantIDPath + "\"</h1>\n"
                    output += "  <p>Please go back to the <a href=\"/\">home page</a>.</p>\n"
                    output += "</body></html>\n"
                    self.wfile.write(output.encode())
                    print(output)
                    return



            elif self.path.endswith("/server_error"):
                output = ""
                output += "<html><body>\n"
                output += "  <h1>Server Error</h1>\n"
                output += "  <p>Please go back to the <a href=\"/\">home page</a>.</p>\n"
                output += "</body></html>\n"
                self.wfile.write(output.encode())
                print(output)
                return

            else:
                print("In GET")
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<body></html>\n"
                output += "  <h1>Unknown Page</h1>\n"
                output += "  <p>Please go back to the <a href=\"/\">home page</a>.</p>\n"
                output += "</body></html>\n"
                self.wfile.write(output.encode())
                print(output)
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    print("Editing restaurant \"" + str(messageContent[0].decode()) + "\"")

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messageContent[0].decode()
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return
                    else:
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/server_error')
                        self.end_headers()
                        return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                print("Deleting restaurant \"" + restaurantIDPath+ "\"")

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
                else:
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/server_error')
                    self.end_headers()
                    return

            elif self.path == "/restaurants/new":
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newRestaurantName')

                # Create new Restaurant Object
                print("Adding new restaurant \"" + str(messageContent[0].decode()) + "\"")
                newRestaurant = Restaurant(name=str(messageContent[0].decode()))
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            else:
                print("In POST");
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/server_error')
                self.end_headers()
                return

        except Exception as e:
            print(e)
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/server_error')
            self.end_headers()
            return

def main():
    try:
        port = int(os.environ.get('PORT', 8080))   # Use PORT if it's there.
        server_address = ('', port)
        server = http.server.HTTPServer(server_address, WebServerHandler)
        server.serve_forever()
        print ("Web Server running on port 8080")
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()

