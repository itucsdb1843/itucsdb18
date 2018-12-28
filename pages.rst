*****
PAGES
*****

➡ This document is about what users are able to do in each url of the website.

Feasibilities
=============

➡ 10 url's exist that can be visited in the website which will be referred with "html" extensions.

- Homepage: (click `here1 <https://itucsdb1843.herokuapp.com/>`_ to visit)
	- index.html
	- Rendered in home_page() view function.
	- Homepage is the a page where only hyperlinks are provided.
- User Profile: (click `here2 <https://itucsdb1843.herokuapp.com/profile>`_ to visit)(login required)
	- profile.html
	- Rendered in profile_page() view function.
	- Here, a registered user is able to:
		- See the profile photo(avatar).
		- Read and change the profile information.
		- Change the profile photo.
		- Hyperlink to the photo upload page for universities.
		- Hyperlink to own study chains.
- University Rankings: (click `here3 <https://itucsdb1843.herokuapp.com/university_rankings>`_ to visit)
	- university_rankings.html
	- Rendered in university_rankings() view function.
	- Here, a user is able to:
		- See the universities ordered by score.
		- Universities are rendered with logo, background, and all the other data.
		- Score a university
- Clubs: (click `here4 <https://itucsdb1843.herokuapp.com/clubs>`_ to visit)(login required)
	- clubs.html
	- Rendered in clubs_page() view function.
	- Here, a registered user is able to:
		- See the list of universities with their clubs.
		- Hyperlink to a club profile by clicking on it.
- Events: (click `here5 <https://itucsdb1843.herokuapp.com/events>`_ to visit)(login required)
	- events.html
	- Rendered in events_page() view function.
	- Here, a registered user is able to:
		- See the all events with all the information they have.
		- Delete an event if he/she is the creator of that event.
		- Comment on an event by clicking on the event card.
		- Score an event by clicking on the event card.
		- Delete a comment if he/she is the creator of that comment.
		- Upvote any comment.
		- Downvote any comment.
- Club Profile: (click `here6 <https://itucsdb1843.herokuapp.com/clubs/1>`_ to visit)(login required)(wildcard needed)
	- club_single.html
	- Rendered in clubs_page() view function.
	- Here, a registered user is able to:
		- See only the events of that particular club.
		- Add an event for that club.
		- Comment on an event by clicking on the event card.
		- Score an event by clicking on the event card.
		- Delete a comment if he/she is the creator of that comment.
		- Upvote any comment.
		- Downvote any comment.

- Login: (click `here7 <https://itucsdb1843.herokuapp.com/login>`_ to visit)
	- login.html
	- Rendered in login_page() view function.
	- Here, a non-logged-in user is able to:
		- Login by nickname and password.
- Registration: (click `here8 <https://itucsdb1843.herokuapp.com/register>`_ to visit)
	- register.html
	- Rendered in register_page() view function.
	- Here, a user is able to:
		- Register by filling the registration form and submitting it.
		- Read the names of the universities that the system has to pick one during registration.
- Upload University Photo: (click `here9 <https://itucsdb1843.herokuapp.com/upload_university_photo>`_ to visit)(login required)
	- upload_university_photo.html
	- Rendered in profile_page() view function.
	- Here, a registered user is able to:
		- Read the names of the universities that the system has to pick one.
		- Select the photo type as either logo or background.
		- Browse a photo to upload.
		- Submit the changes.
- User Study Chains: (click `here <https://itucsdb1843.herokuapp.com/study_chains>`_ to visit)(login required)
	- study_chains.html
	- Rendered in study_chains() view function.
	- Here, a registered user is able to:
		- See the profile photo(avatar).
		- Add a new study chain by filling up the designated form.
		- Add a new TODO to one of the own study chains by filling up the designated form.
		- See the existing study chains and TODO's of them.


