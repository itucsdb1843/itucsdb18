.. _scope:

*************
PROJECT SCOPE
*************

Promised
========
Here is the project scope that was promised in the project proposal, however it occured to have some changes about the capabilities of users and fisibilities of some pages which are explained in details in `Current Version <file:///home/user/DB/itucsdb1843/_build/html/scope.html#current-version>`_ part.

Short Discription
-----------------
Univertown is a project that aims to be a website that will help students
to make the most clever decision while choosing a collage. Students will
also have an individual area to keep track of their pilot test history
successively so that they can observe their improvement. Also they will
have a chance to see the experienced collage students' ideas to clear
their minds about collage life and courses.


Long Description
----------------
• What are the data that will be stored and processed?
	‣ Data of most of the universities,
	‣ University comments,
	‣ University ratings,
	‣ Data of departments and academicians of each university
	‣ Data of students (users),
	‣ Data of study history of students.

• What type of users will use the system?
	- Account-owner users will exist on the system. They will not be in admin privileges, but they will edit the website under some validation rules.

• What will the users be able to do with the data and the application?
	➡ A non-admin user:
		‣ While not signed-in, will be able to:
			- read the content but cannot edit it.
			- list the universities by city or rating.
			- view the academicians and course plans of the universities.
		
		‣ While signed-in, will be able to:
			- read the content and can request to edit it.
			- list the universities by city or rating.
			- view the academicians and course plans of the universities.
			- comment and rate a university
			- making a request to add a university to the system.
			- save their pilot test history. This way, students can keep track of their records and can set their aims wiser.
				✓ In adequate numbers, system will list the available collages that the student can join with her/his current records.

	➡ An admin (us):
		- can delete the inappropriate accounts
		- can update the data of collages if any change occurs.


Current Version
===============

This is the project scope of the current version.

Short Discription
-----------------
Univertown is a project that is meant to be a guide for:

1) Undergraduate students
	- to have a better access to the information of the events of clubs in universities to be more social and planned,
	- to be more organized with study chains.

2) Highschool students 
	- to be clearer about their university goal and decisions by the help of different scoring criterias of a university,
	- to be more orginezed with study chains.


Long Description
----------------
• What are the data that is stored and processed?
	‣ Data of the top universities in Turkey:
		- Scores
		- Images
		- Unique Information
		
	‣ Data of clubs of universities:
		- Metadata of a club

	‣ Data of events of clubs,

	‣ Data of students (users),

	‣ Data of study chains of students.

	For a further explanation, check out the `Data Processed <file:///home/user/DB/itucsdb1843/_build/html/database.html#data-processed>`_ part.

• What type of users use the system?
	- Account-owner users exist on the system. They do not have the admin privileges, but they can edit the website under some validation rules.

• What do the users be able to do with the data and the application?
	➡ A non-admin user:
		‣ While not logged-in, is able to:
			- cannot facilitate the website, because sessions is used to keep track of the user activities and most of the facilities require certain user information to process. 
		
		‣ While logged-in, is able to:
			- read the content and can request to edit it,
			- list the universities by rating,
			- view the clubs and their events,
			- Score a university
			- Comment on an event
			- save their study chains as a todo list with timing information.

	➡ An admin (us):
		- can delete the inappropriate accounts,
		- can add clubs,
 		- can add universities,
		- can update the data of universities if any change occurs.



Requirements
============

Website is created using:

- Python 3.6
- Framework: Flask
- Extentions: 
	- Flask-Bcrypt
	- Flask-Login
	- Flask-Uploads
- Database: PostgreSql


