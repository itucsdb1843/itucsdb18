import sys
from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required,logout_user,current_user
from functools import wraps
import os

after_registration = False



def home_page():
	if request.method == 'GET':
		from database import universityPhotosTable
		university_photos_table = universityPhotosTable()
		return render_template('pages/index.html')




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
		return redirect(url_for('index'))


def university_rankings_page():
	if request.method == 'GET':
		from database import universitiesTable,universityPhotosTable
		universities_table = universitiesTable()
		theListOfUniversityTuples = universities_table.getUniversitiesAndScoresOrderedByScore()
		university_photos_table = universityPhotosTable()
		university_photos_table.fetchAllPhotos(theListOfUniversityTuples)
		return render_template('pages/university_rankings.html', theList = theListOfUniversityTuples)

	else:
		from database import universitiesTable
		universities_table = universitiesTable()
		universities_table.addScore(request.form)
		return redirect(url_for('university_rankings'))
	     

def register_page():
	
	if request.method == 'GET':
		from database import universitiesTable
		universities_table = universitiesTable()
		university_names = universities_table.getUniversityNames()
		return render_template("pages/register.html", university_names = university_names)
	else:
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



        


