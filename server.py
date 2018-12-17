import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES



from models.user import Anonymous
import views


def create_app():

    app = Flask(__name__)
    
    app.add_url_rule('/', 'index', view_func=views.home_page)

    app.add_url_rule('/events','events', view_func=views.events_page, methods = ["GET","POST"])

    app.add_url_rule('/clubs','clubs', view_func=views.clubs_page, methods = ["GET","POST"])
    app.add_url_rule('/clubs/<path:club_id>','clubs', view_func=views.clubs_page, methods = ["GET","POST"])

    app.add_url_rule('/register','register', view_func=views.register_page, methods = ["GET","POST"])
    
    app.add_url_rule('/login','login', view_func=views.login_page, methods = ["GET","POST"])
        
    app.add_url_rule('/university_rankings', 'university_rankings', view_func=views.university_rankings_page, methods = ["GET","POST"])

    app.add_url_rule('/upload_university_photo', 'upload_photo', view_func=views.upload_university_photo_page, methods = ["GET","POST"])

    app.add_url_rule('/profile','profile', view_func=views.profile_page, methods = ["GET","POST"])

    app.add_url_rule('/study_chains','study_chains', view_func=views.study_chains_page, methods = ["GET","POST"])
    
    return app


app = create_app()

app.config.from_pyfile('config.py')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
    from database import usersTable
    users_table = usersTable()
    user = users_table.getUserObjectByID(user_id)
    return user



photos = UploadSet('photos',IMAGES)
configure_uploads(app, photos)


if __name__ == "__main__":

    app.run()

# implementation notes:
# For method names, camelCase is used.
# For variable names, under_score is used.