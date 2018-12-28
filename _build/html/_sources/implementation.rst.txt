********************
IMPLEMENTATION NOTES
********************

Models
======
.. automodule:: user
   :members:

- User model is used for the session that keeps track of the user activities.
- Carrying every attribute that a user has.
- Comunicating with the Flask-Login_Manager.


- Anonymous model is used for Guest session which pretty much does nothing but provides a name to anonymous users.
- Does not carry the information of the guests.

Views
=====
➡ 9 view_functions for 9 routes(url_rules).

- home_page()
	- Homepage with hyeperlinks.
- profile_page()
	- Requires login.
	- Uses current user in the session.
	- Reads from universities, clubs and users relations in database.
	- Writes(Updates) to users relation in database.
	- Answers 3 post requests:
		- Editing profile info
		- Changing profile photo
		- Adding an event
- study_chains_page()
	- Requires login.
	- Uses current user in the session.
	- Reads from chains and todos relations in database.
	- Writes(Updates) to chains and todos relations in database.
	- Answers 2 post requests:
		- Adding a new chain
		- Adding a todo to a chain
- events_page()
	- Requires login.
	- Uses current user in the session.
	- Reads from events and comments relations in database.
	- Writes(Updates) to events and comments relations in database.
	- Answers 5 post requests:
		- Commenting an event
		- Deleting a comment
		- Upvoting a comment
		- Downvoting a comment
		- Deleting an event
- clubs_page(club_id=None)
	- Requires login.
	- Uses current user in the session.
	- Reads from clubs, events and universities relations in database.
	- Writes(Updates) to events and comments relations in database.
	- Answers 6 post requests:
		- Adding an event
		- Commenting an event
		- Scoring an event
		- Upvoting a comment
		- Downvoting a comment
		- Deleting a comment
- upload_university_photo_page()
	- Requires login.
	- Reads from universities relation in database.
	- Writes(Updates) to universities and university_photos relations in database.
	- Answers 1 post request:
		- Uploading an image
- university_rankings_page()
	- Does not require login.
	- Reads from universities and university_photos relations in database.
	- Writes(Updates) to universities and avg_score relations in database.
	- Answers 1 post request:
		- Scoring a university
- register_page()
	- Does not require login.
	- Reads from universities relation in database.
	- Writes(Updates) to users relation in database.
	- Answers 1 post request:
		- Registration of a guest
- login_page()
	- Does not require login.
	- Does not read from any relation.
	- Does not write to any relation.
	- Answers 1 post request:
		- Login of a guest

- click `here <file:///home/user/DB/itucsdb1843/_build/html/pages.html#feasibilities>`_ to see what these functions is used for in a User Interface perspective.


Methods (Controllers)
=====================

➡ 8 classes for 9 tables(relations) to implement their methods.
	- method for the table avg_score is implemented in the class for universities table.

➡ Method names are tried to be given clean so that no explanation would be needed.

- class universitiesTable:
	- uploadAndSetPhoto(self,request_files, request_form):
	- getImagesIdByUniversityName(self,university_name):
	- getUniversityNames(self):
	- getUniversityIDbyName(self,university_name):
	- getScoreIdByName(self,university_name):
	- getAllUniversityNamesAndIds(self):
	- getUniversitiesAndScoresOrderedByScore(self):
	- addScore(self,request_form):
	
- class usersTable:
	- editUserProfileInfo(self,form_result_map):
	- changeAvatar(self,request_files):
	- addUser(self,form_result_map):
	- makeUserLoggedIn(self, form_nickname, form_password):
	- getUserObjectByID(self, user_id):
	- getAvatar(self,user_id):

- class eventsTable:
	- getAllEvents(self):
	- getEventsByClubId(self, club_id):
	- addScore(self,form_result_map):
	- addEventByClubId(self,form_request_map, club_id):
	- deleteEventById(self,event_id):

- class commentsTable:
	- getAllComments(self):
	- getCommentsByEventId(self, event_id):
	- addComment(self,form_result_map):
	- updateUpvote(self,comment_id):
	- updateDownvote(self,comment_id):
	- deleteCommentById(self,comment_id):

- class todosTable:
	- addToDo(self,request_form):
	- getAllTodosOfAChain(self,chain_id):

- class chainsTable:
	- getAllChainsOfTheUser(self):
	- getChainIdByTitle(self,chain_name):
	- createChain(self,chain_title):

- class universityPhotosTable:
	- fetchAllPhotos(self,theListOfUniversityTuples):
	- updatePhoto(self,filename,photo_type,images_id):
	- addPhoto(self,filename,photo_type,university_name):
	- getPhoto(self):

- class clubsTable:
	- getClubNames(self):
	- getAllClubs(self):
	- getClubById(self, club_id):








