from flask import Flask, render_template
from datetime import datetime
import views
#app = Flask(__name__)


#@app.route("/")
#def home_page():
#    return "ello"

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', view_func=views.home_page)
    app.add_url_rule('/events','events', view_func=views.events_page)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
