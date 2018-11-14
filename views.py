from flask import render_template

def home_page():
    return render_template('pages/home.html')
def events_page():
    return render_template('pages/events.html')
