# Import libraries
from flask import Flask, request, render_template, jsonify, flash
from utils.forms import ValidateDate, ValidateFile, SubmitRetrain
from utils.models import predictions, modification_data, create_db_csv, modelo_entrenar
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from config import DATA_BASE, MODEL, USER, PASSWORD, HOST, ENDPOINT
import pymysql, csv, os

# Setting path init
os.chdir(os.path.dirname(__file__))

# App configurations
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config["DEBUG"] = True

# Endpoints for visual

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
                    predict = predictions(form.data["period"], MODEL)
                    flash(predict)
                    return render_template("predict.html", form=form)

                except pymysql.Error as e:
                    print(e)
                    flash("Error en al base de datos, por favor contacta con tu administrador")
                    return render_template("predict.html", form=form)

                except ValueError as e:
                    print(e)
                    flash("Debes introducir un campo válido")
                    return render_template("predict.html", form=form)

        else:
            flash("Debes introducir los datos correctamente")
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
                        if request.files:
                            data = []
                            uploaded_file = request.files[form.data["file"]]
                            filepath = os.path.join(app.config["FILE_UPLOADS"], uploaded_file.filename)
                            with open(filepath) as file:
                                csv_file = csv.reader(file)
                                for row in csv_file:
                                    data.append(row)
                        create_db_csv(modification_data("data/users_web.csv"), HOST, PASSWORD, USER)
                        flash("La base de datos se ha actualizado correctamente")
                        return redirect(url_for("home"))

                    except pymysql.Error as e:
                        print(e)
                        flash("Error en al base de datos, por favor contacta con tu administrador")
                        return render_template("update.html", form=form)

                else:
                    flash("Debes introducir un archivo .csv")
                    return render_template("update.html", form=form)

        else:
            flash("Debes introducir los datos correctamente")
            return render_template("update.html", form=form)

# Retrain the model
@app.route("/api/v1/retrainModel/", methods=["GET", "POST"])
def retrain_model():
    form = SubmitRetrain()

    if request.method == "GET":
        return render_template("retrain.html", form=form)
    
    else:
        if form.validate:
            if form.data["submit"] == True:
                try:
                    modelo_entrenar(MODEL, HOST, PASSWORD, USER)
                    flash("El modelo se ha actualizado correctamente")
                    return redirect(url_for("home"))

                except pymysql.Error as e:
                    print(e)
                    flash("Error en al base de datos, por favor contacta con tu administrador")
                    return render_template("retrain.html", form=form)

        else:
            flash("Debes introducir los datos correctamente")
            return render_template("retrain.html", form=form)

if __name__ == "__main__":
    app.run()