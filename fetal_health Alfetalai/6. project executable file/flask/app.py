from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle


model = pickle.load(open(r'fetal_health1.pkl','rb'))
app=Flask(__name__)

@app.route("/")
def f():
    return render_template("index.html")
    


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve form data
        prolongued_decelerations = float(request.form['prolongued_decelerations'])
        abnormal_short_term_variability = float(request.form['abnormal_short_term_variability'])
        percentage_of_time_with_abnormal_long_term_variability = float(request.form['percentage_of_time_with_abnormal_long_term_variability'])
        histogram_variance = float(request.form['histogram_variance']) 
        histogram_median = float(request.form['histogram_median'])
        mean_value_of_long_term_variability = float(request.form['mean_value_of_long_term_variability']) 
        histogram_mode = float(request.form['histogram_mode'])
        # Check if "accelerations" field is not empty
        accelerations_input = request.form['accelerations']
        if accelerations_input:
            accelerations = float(accelerations_input)
        else:
            return "Error: Please provide a value for accelerations"

        x = [[prolongued_decelerations, abnormal_short_term_variability, percentage_of_time_with_abnormal_long_term_variability, histogram_variance, histogram_median, mean_value_of_long_term_variability, histogram_mode, accelerations]]
        output = model.predict(x)

        out = ['Normal', 'Pathological', 'Suspect']
        if int(output[0]) == 0:
            output = 'Normal'
        elif int(output[0]) == 1:
            output = 'Pathological'
        else:
            output = 'Suspect'

        return render_template('output.html', output=output)
    else:
        return "Method not allowed"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__=='__main__':
    app.run(debug=True)