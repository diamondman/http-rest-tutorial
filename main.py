#!/usr/bin/python3

from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from os import path

"""Every library has some form of suggested startup.
   Here is Flask's http://flask.pocoo.org/docs/0.10/quickstart/"""
app = Flask(__name__)
app.debug = True
"""There is a library acalled flask-sqlalchemy that connects flask's 
     requests to sqlalchemy's sessions. These lines come from 
     https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
   The DATABASE_URI line below is specifying what database to use. The URI 
     format is specified here:
     http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls
   The guide shows how to interpret the URI below. The important thing is
     that we are using sqlite as the database (driver). Sqlite is a simple
     database originally made to run on missiles. Sqlite needs a file to 
     store the database. The file will appear in the same folder as this 
     file. https://en.wikipedia.org/wiki/SQLite """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
db = SQLAlchemy(app)

"""The database model that generates SQL for us through sqlalchemy."""
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(120))
    description = db.Column(db.String)

    """This is a format string that makes User objects look like 
    <User(1) 'Ceisel' rose> instead of some random numbers."""
    def __repr__(self):
        return '<Plant(%d) %r %s>' % (self.id, self.name, self.type)

"""These lines that start with @ are called decorators.
   How they work internally is complex. For now just know that they modify a function."""
@app.route('/')
def home_view():
    return render_template('home.html')

"""HTTP uses one of several 'methods' in each request. The common ones are
   GET, PUT, POST, DELETE. GET is by far the most common. Whenever you type
   a URL in the browser and hit enter, that is a GET request (GET is default).
   POST is often used when logging into a website or when creating an entry
   in a database somehow. PUT is supposed to be used to specify updates to
   existing data. And DELETE is suposed to delete the data at the url.
   https://en.wikipedia.org/wiki/Representational_state_transfer """
@app.route('/plant', methods=['GET'])
def plants_view():
    return render_template('plants.html', entries=Plant.query.all())

@app.route('/plant', methods=['POST'])
def plants_add_view():
    #Create the new database entry, add the change to be saved, then commit the change.
    #The request variable is provided by flask and has the decoded content of the
    #request message sent from the client (the browser asking for the page). Here we
    #are reading the form data sent when the submit button was pressed.
    plant = Plant(name=request.form['name'], type=request.form['type'],
                  description=request.form['description'])
    db.session.add(plant)
    db.session.commit()
    #Return a message saying the plant was added.
    #The 201 is an http status code (like 404). 201 means something was created.
    #Flask lets us return the status code as a 2nd return argument and it handles
    #the rest of the details of building the response to the client.
    return render_template('plant_add.html', entry=plant), 201

"""View for displaying details about a single plant"""
@app.route('/plant/<int:plantid>', methods=['GET'])
def plant_view(plantid):
    plant = Plant.query.filter(Plant.id==plantid).one()
    #Here I am doing something odd. I am either loading the plant or plant_edit template
    #based on if edit=1 is in the url. This could be done in the template but I liked it
    #here instead.
    if request.args.get('edit') == '1':
        return render_template('plant_edit.html', entry=plant)
    return render_template('plant.html', entry=plant)

"""View for updating details about a single plant"""
@app.route('/plant/<int:plantid>', methods=['PUT'])
def plant_update_view(plantid):
    #Get the plant in question from the id provided.
    #This is the plant we will update.
    plant = Plant.query.filter(Plant.id==plantid).one()
    #For each of the 3 fields we can update check if the field is in the
    #form data and if it is update the plant's data.
    if 'name' in request.form:
        plant.name = request.form['name']
    if 'type' in request.form:
        plant.type = request.form['type']
    if 'description' in request.form:
        plant.description = request.form['description']
    #Save the changes to the database.
    db.session.add(plant)
    db.session.commit()
    #No need to render a template since this endpoint can only be accessed through javascript.
    return "SUCCESS"

"""View for displaying details about a single plant
   Because the world is full of injustice, forms in html can not send delete or put
   requests. Those requests have to be sent with javascript. I hate this so much."""
@app.route('/plant/<int:plantid>', methods=['DELETE'])
def plant_delete_view(plantid):
    #Get the plant row from the database. Mark it for deletion. Commit the change.
    plant = Plant.query.filter(Plant.id==plantid).one()
    db.session.delete(plant)
    db.session.commit()
    #No need to render a template since this endpoint can only be accessed through javascript.
    return "SUCCESS"


####################################################################
####################Tutorial routes#################################
#These are for showing how http and rest work with mostly templates#
####################################################################
@app.route("/tutorial")
def tutorials_view():
    return redirect("/tutorial/1")

@app.route("/tutorial/<int:tut_num>", methods=["GET", "POST"])
def tutorial_view(tut_num):
    """from bs4 import BeautifulSoup
    soup = BeautifulSoup(render_template("tutorial_%d.html"%tut_num, tut_num=tut_num),
                         'html.parser')
    return soup.prettify()"""
    return render_template("tutorial_%d.html"%tut_num, tut_num=tut_num,
                           is_not_last=path.isfile("templates/tutorial_%d.html"%(tut_num+1)))


#http://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    app.run()
