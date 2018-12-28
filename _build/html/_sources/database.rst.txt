.. Univertown documentation master file, created by
   sphinx-quickstart on Wed Dec 26 15:04:34 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*******************
DATABASE MANAGEMENT
*******************
To store the data we have used PostgreSQL which is an open-source relational SQL Database with a higher reliability and speed. Other than that, to map the relationships between tables, foreign keys are directly supported. Also, Heroku app provides a path to our Docker PostgreSQL database over an Amazon Web Service which is ready to use. So, the PostgreSQL is reliable, fast, easy to manage and totally eligible for an application that would work fine with a relational database.

Relations and Data Processed
============================
➡ 9 relations(tables) are used to process the data.

- users
	- main relation.
	- data processed:
		✓id
		✓name
		✓surname
		✓nickname
		✓password
		✓email
		✓status
		✓city
		✓university_id
		✓last_login
		✓registration_time
		✓avatar


- universities
	- main relation.
	- data processed:
		✓id
		✓name
		✓city
		✓country
		✓images_id
		✓score_id
		✓address
		✓phone_no
		✓website


- university-photos
	- side relation of universities.
	- data processed:
		✓ id
		✓ logo
		✓ background


- avg-score
	- side relation of universities.
	- data processed:
		✓id
		✓average_score
		✓score_by_campus
		✓score_by_education
		✓score_by_social_life
		✓score_count


- clubs
	- main relation.
	- data processed:
		✓id
		✓name
		✓departman_name
		✓foundation_date
		✓member_count
		✓contact_mail
		✓university_id


- events
	- main relation.
	- data processed:
		✓id
		✓title
		✓description
		✓price
		✓place
		✓event_date
		✓event_time
		✓duration
		✓club_id
		✓puan
		✓number_of_evaluation
		✓user_id
		

- comments
	- main relation
	- data processed:
		✓id
		✓title
		✓body
		✓country
		✓useful_no
		✓useless_no
		✓user_id
		✓event_id
		✓comment_time
		✓user_nickname
		

- chains
	- side relation of todos
	- data processed:
		✓id
		✓title
		✓user_id


- todos
	- main relation
	- data processed:
		✓id
		✓body
		✓start_date
		✓expected_end_date
		✓real_end_date
		✓completed
		✓chain_id


