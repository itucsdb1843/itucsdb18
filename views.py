from flask import render_template

def home_page():
    return render_template('pages/index.html')
def events_page():
    return render_template('pages/events.html')
def results_page():
    return render_template('pages/results.html')
