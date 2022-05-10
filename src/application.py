# Import libraries
from flask import Flask, request, render_template, jsonify, flash
from utils.forms import ValidateDate, ValidateFile
from utils.models import DBController, predictions
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from config import DATA_BASE
import pymysql, os

# Setting paths to database and creating instance of DBController
os.chdir(os.path.dirname(__file__))
dbcontroller = DBController(DATA_BASE)

# App configurations
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config["DEBUG"] = True

# Endpoints

# Home
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Predictions
@app.route("/api/v1/predictModel/", methods=["GET", "POST"])
def predict_model():
    form = ValidateDate()
        
    if request.method == "GET":
        return render_template("predict.html", form=form)

    else:
        if form.validate:
            if form.data["submit"] == True:

                try:
                    flash("Flash funciona!!!")
                    return render_template("predict.html", form=form)

                except pymysql.Error as e:
                    print(e)
                    flash("Database error, please contact with your administrator")
                    return render_template("predict.html", form=form)

        else:
            flash("You must enter the data correctly")
            return render_template("predict.html", form=form)

# Refresh database
@app.route("/api/v1/refreshDatabase/", methods=["GET", "POST"])
def refresh_database():
    form = ValidateFile()
        
    if request.method == "GET":
        return render_template("update.html", form=form)

    else:
        if form.validate:
            if form.data["submit"] == True:
                if form.data["file"][-4:] == ".csv":

                    try:
                        flash("The database has been updated")
                        return redirect(url_for("home"))

                    except pymysql.Error as e:
                        print(e)
                        flash("Database error, please contact with your administrator")
                        return render_template("update.html", form=form)

                else:
                    flash("You must upload a .csv file")
                    return render_template("update.html", form=form)

        else:
            flash("You must enter the data correctly")
            return render_template("update.html", form=form)