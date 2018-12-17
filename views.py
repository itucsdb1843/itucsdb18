import sys
import datetime
from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required,logout_user,current_user
from functools import wraps
import os

after_registration = False
scored = False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated():
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def home_page():
	if request.method == 'GET':
		return render_template('pages/index.html')


@login_required
def profile_page():
	if request.method == 'GET':

		from database import universitiesTable,clubsTable,usersTable
		users_table = usersTable()
		users_table.getAvatar(current_user.id)
		universities_table = universitiesTable()
		clubs_table = clubsTable()
		university_names = universities_table.getUniversityNames()
		club_names = clubs_table.getClubNames()
		return render_template('pages/profile.html', university_names = university_names, club_names = club_names)

	else:
		if 'editProfileInfoForm' in request.form:
			form_result_map = request.form.to_dict()
			from database import usersTable
			users_table = usersTable()
			changes_are_made = users_table.editUserProfileInfo(form_result_map)
			#return render_template('pages/profile.html', profile_edited=changes_are_made)
		elif 'changeProfilePhotoForm' in request.form and 'photo' in request.files:
			from database import usersTable
			users_table = usersTable()
			avatar_changed = users_table.changeAvatar(request.files)
			#return render_template('pages/profile.html', avatar_changed=avatar_changed)
		elif 'addEventForm' in request.form:
			from database import eventsTable
			events_table = eventsTable()
			event_added = events_table.addEvent(request.form)
			#return render_template('pages/profile.html', event_added=event_added)
		return redirect(url_for('profile'))


@login_required
def study_chains_page():
	if request.method == 'GET':
		from database import chainsTable
		chains_table = chainsTable()
		chains = chains_table.getAllChainsOfTheUser()
		from database import todosTable
		todos_table = todosTable()
		todos_list = []
		for each_chain in chains:
			todos_list.append(todos_table.getAllTodosOfAChain(each_chain[0]))
		return render_template('pages/study_chains.html',chains = chains, todos = todos_list)

	else:
		if 'addToDo' in request.form:
			from database import todosTable
			todos_table = todosTable()
			todos_table.addToDo(request.form)
			return redirect(url_for('study_chains'))
		elif 'createChain' in request.form:
			from database import chainsTable
			chains_table = chainsTable()
			chain_title = request.form['title']
			chains_table.createChain(chain_title)
			return redirect(url_for('study_chains'))




@login_required
def events_page():
	if request.method == 'GET':
		from database import eventsTable
		events_table = eventsTable()
		all_events_tuple = events_table.getAllEvents()

		from database import commentsTable
		comments_table = commentsTable()
		all_comments_tuple = comments_table.getAllComments()

		return render_template('pages/events.html', events = all_events_tuple, comments = all_comments_tuple)

	else:
		
		if 'commentForm' in request.form:
			form_result_map = request.form.to_dict()
			if form_result_map['eventScore'] != 'None':
				from database import eventsTable
				events_table = eventsTable()
				events_table.addScore(form_result_map)
			if form_result_map['commentBody']:
				from database import commentsTable
				comments_table = commentsTable()
				comments_table.addComment(form_result_map)
		if 'upvote' in request.form:
			form_result_map = request.form.to_dict()
			from database import commentsTable
			comments_table = commentsTable()
			comment_id = form_result_map['commentId']
			comments_table.updateUpvote(comment_id)
		elif 'downvote' in request.form:
			form_result_map = request.form.to_dict()
			from database import commentsTable
			comments_table = commentsTable()
			comment_id = form_result_map['commentId']
			comments_table.updateDownvote(comment_id)
		elif 'deleteComment' in request.form:
			form_result_map = request.form.to_dict()
			from database import commentsTable
			comments_table = commentsTable()
			comment_id = form_result_map['commentId']
			comments_table.deleteCommentById(comment_id)
		elif 'deleteEvent' in request.form:
			form_result_map = request.form.to_dict()
			from database import eventsTable
			events_table = eventsTable()
			event_id = form_result_map['eventId']
			events_table.deleteEventById(event_id)
		return redirect(url_for('events'))


@login_required
def clubs_page(club_id=None):
	if request.method == 'GET':
		if club_id == None:
			from database import clubsTable
			clubs_table = clubsTable()
			clubs_tuple = clubs_table.getAllClubs()

			from database import universitiesTable
			universities_table = universitiesTable()
			university_tuple = universities_table.getAllUniversityNamesAndIds()
			return render_template('pages/clubs.html', clubs = clubs_tuple, universities = university_tuple)

		else:
			from database import clubsTable
			clubs_table = clubsTable()
			club = clubs_table.getClubById(club_id)

			from database import eventsTable
			events_table = eventsTable()
			events_tuple = events_table.getEventsByClubId(club_id)

			from database import commentsTable
			comments_table = commentsTable()

			list_of_comment_tuples = []

			for each_event in events_tuple:
				comments_tuple = comments_table.getCommentsByEventId(each_event[0])
				list_of_comment_tuples.append(comments_tuple)

			return render_template('pages/club_single.html', club= club, events = events_tuple, comments = list_of_comment_tuples)
	else:
		if(club_id):
			if 'addEventForm' in request.form:
				form_result_map = request.form.to_dict()
				from database import eventsTable
				events_table = eventsTable()
				events_table.addEventByClubId(form_result_map, club_id)
			elif 'commentForm' in request.form:
				form_result_map = request.form.to_dict()
				if form_result_map['eventScore'] != 'None':
					from database import eventsTable
					events_table = eventsTable()
					events_table.addScore(form_result_map)
				if form_result_map['commentBody']:
					from database import commentsTable
					comments_table = commentsTable()
					comments_table.addComment(form_result_map)
		elif 'upvote' in request.form:
			form_result_map = request.form.to_dict()
			from database import commentsTable
			comments_table = commentsTable()
			comment_id = form_result_map['commentId']
			comments_table.updateUpvote(comment_id)
		elif 'downvote' in request.form:
			form_result_map = request.form.to_dict()
			from database import commentsTable
			comments_table = commentsTable()
			comment_id = form_result_map['commentId']
			comments_table.updateDownvote(comment_id)
		elif 'deleteComment' in request.form:
			form_result_map = request.form.to_dict()
			from database import commentsTable
			comments_table = commentsTable()
			comment_id = form_result_map['commentId']
			comments_table.deleteCommentById(comment_id)

		return redirect(url_for('clubs'))



@login_required
def upload_university_photo_page():
	if request.method == 'GET':
		from database import universitiesTable
		universities_table = universitiesTable()
		university_names = universities_table.getUniversityNames()
		return render_template('pages/upload_university_photo.html', university_names = university_names)
	elif request.method == 'POST' and 'photo' in request.files:
		from database import universitiesTable
		universities_table = universitiesTable()
		universities_table.uploadAndSetPhoto(request.files, request.form)
		return redirect(url_for('upload_university_photo'))


def university_rankings_page():
	global scored
	if request.method == 'GET':
		from database import universitiesTable,universityPhotosTable
		universities_table = universitiesTable()
		theListOfUniversityTuples = universities_table.getUniversitiesAndScoresOrderedByScore()
		university_photos_table = universityPhotosTable()
		photo_exists_list = university_photos_table.fetchAllPhotos(theListOfUniversityTuples)
		university_names = universities_table.getUniversityNames()
		
		oldScored = scored
		scored = False
		return render_template('pages/university_rankings.html', theList = theListOfUniversityTuples, university_names = university_names, photo_exists_list = photo_exists_list, scored = oldScored)

	else:
		from database import universitiesTable
		universities_table = universitiesTable()
		scored = universities_table.addScore(request.form)
		return redirect(url_for('university_rankings'))
	     

def register_page():
	
	if request.method == 'GET':
		from database import universitiesTable
		universities_table = universitiesTable()
		university_names = universities_table.getUniversityNames()
		return render_template("pages/register.html", university_names = university_names)
	else:
		from form import formValidation
		form_validation = formValidation()

		form_result_map = request.form.to_dict()
		email = form_result_map['email']
		email_validation_result = form_validation.validateEmail(email)
        #if not email_validation_result:
            #return "Email should be in the form of 'example@example.com'"

		from database import usersTable
		users_table = usersTable()
		#to get the form result as a whole (best approach) (form names are unknown)
		form_result_map = request.form.to_dict()
		users_table.addUser(form_result_map)
		global after_registration
		after_registration = True
		if current_user.is_authenticated():
			return redirect(url_for("index"))
		else:
			return redirect(url_for("login"))

		#NOTES ##################################################################################

		#request.form['firstname'] : gives the firstname's value. Firstame must be required.
		#request.form.get('firstname') : gives the firstname's value. Firstname may not be required.
		#request.form.getlist('firstname') : key is sent multiple times and you want a list of values.
		#form_result = request.form : returns an ImmutableMultiDict object. In the form of:
			#ImmutableMultiDict([('firstname', 'ahmet'), ('lastname', 'yilmaz'), ('nickname', ''), ('email', ''), ('password', ''), ('city', '')])
			#for each_item in form_result:
				#print(each_item)
			#prints out the console:
			#>> firstname
			#>> lastname
			#>> nickname
			#>> email
			#>> password
			#>> city
		#form_result_as_dict = request.form.to_dict() : returns a dictionary as a map. In the form of:
			#{'firstname': 'ahmet', 'lastname': 'yilmaz', 'nickname': 'ayilmaz123', 'email': '', 'password': '', 'city': ''}
			#for each_item in form_result_as_dict:
				#print(each_item)
			#prints out the console:
			#>> firstname
			#>> lastname
			#>> nickname
			#>> email
			#>> password
			#>> city
			#but this time, they can be used as keys to access the values in the map.

		##########################################################################################


		#one by one approach (form is known)
		#form_firstname = request.form['firstname']
		#print(form_first_name)
		#form_lastname = request.form['lastname']
		# .
		# .
		# .

def login_page():
	
	if request.method == 'GET':
		if current_user.is_authenticated():
			logout_user()
			return render_template('pages/login.html', after_registration = False, login_failed = False, logged_out = True)
		else:
			global after_registration
			temp_after_registration = after_registration
			after_registration = False
			return render_template('pages/login.html', after_registration = temp_after_registration, login_failed = False, logged_out = False)
	else:
		from database import usersTable
		users_table = usersTable()
		form_nickname = request.form['nickname']
		form_password = request.form['password']
		user_login_status = users_table.makeUserLoggedIn(form_nickname, form_password)
		login_failed = False
		if user_login_status == False:
			login_failed = True
			return render_template('pages/login.html', after_registration = False, login_failed = login_failed, logged_out = False)
		return redirect(url_for('index'))


        


