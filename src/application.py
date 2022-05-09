# Import libraries
from flask import Flask, request, render_template, jsonify, flash
from utils.forms import ValidateDate, ValidateFile
from utils.models import DBController
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
    flash("Flash funciona!!!")
    return render_template("home.html")

# Predictions
@app.route("/api/v1/predictModel/", methods=["GET", "POST"])
def predict_model():
    form = ValidateDate()
        
    if request.method == "GET":
        flash("Flash funciona!!!")
        return render_template("predict.html", form=form)

    else:
        if form.validate:
            if form.data["submit"] == True:

                try:
                    flash("Hago submit")
                    return render_template("predict.html", form=form)

                except pymysql.Error as e:
                    print(e)
                    flash("Database error, please contact with your administrator")
                    return render_template("predict.html", form=form)

        else:
            flash("You must enter the data correctly")
            return render_template("predict.html", form=form)

# Model Retrain
@app.route("/api/v1/retrainModel/", methods=["GET", "POST"])
def retrain_model():
    form = ValidateFile()
        
    if request.method == "GET":
        flash("Flash funciona!!!")
        return render_template("retrain.html", form=form)

    else:
        if form.validate:
            if form.data["submit"] == True:
                if form.data["file"][-4:] == ".csv":

                    try:
                        flash("The model has been retrained succesfully")
                        return redirect(url_for("home"))

                    except pymysql.Error as e:
                        print(e)
                        flash("Database error, please contact with your administrator")
                        return render_template("retrain.html", form=form)

                else:
                    flash("You must upload a .csv file")
                    return render_template("retrain.html", form=form)

        else:
            flash("You must enter the data correctly")
            return render_template("retrain.html", form=form)