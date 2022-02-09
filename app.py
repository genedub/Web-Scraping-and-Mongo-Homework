# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# import pymongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mongo_finish")
# create instance of Flask app


# create route that renders index.html template
@app.route("/")
def home():

    mission_mars_data = mongo.db.mission.find_one()
    # call data base to get scraped data
    return render_template("index.html", text="Mission To Mars", data=mission_mars_data)

@app.route("/scrape")
def button(): 

    new_scraped_data = scrape_mars.scrape()
    # run the scrape
    # mongo.db.mission.insert_one(new_scraped_data)
    mongo.db.mission.update({}, new_scraped_data, upsert=True)
    # store scape into mongo db
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
