import os
import psycopg2 as dbapi2
from server import login_manager, bcrypt, photos, app
from flask_login import login_user, current_user, logout_user
import base64
from models.user import User

global_database_url = "postgres://itucs:itucspw@localhost:32768/itucsdb"


class universitiesTable:


    def uploadAndSetPhoto(self,request_files, request_form):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        filename = photos.save(request_files['photo'])
        universities_table = universitiesTable()
        university_name = request_form['university_selection']
        photo_type = request_form['photo_type']
        images_id = universities_table.getImagesIdByUniversityName(university_name)
        university_photos_table = universityPhotosTable()
        if images_id == None:
            university_photos_table.addPhoto(filename, photo_type, university_name)
        else:
            university_photos_table.updatePhoto(filename, photo_type, images_id)





    def getImagesIdByUniversityName(self,university_name):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT (images_id) FROM universities WHERE(name='%s')" % (university_name)
        cursor.execute(query)
        images_id = cursor.fetchone()
        return images_id[0]


    def getUniversityNames(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        university_names = []
        cursor.execute("SELECT name FROM universities")
        university_names_list = cursor.fetchall()
        for each_university_name in university_names_list:
            university_names.append(each_university_name[0])
        db_connection.commit()
        cursor.close()
        return university_names


    def getUniversityIDbyName(self,university_name):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM universities WHERE (name='%s')" % (university_name))
        university_id = cursor.fetchall()
        db_connection.commit()
        cursor.close()
        if university_id:
            return university_id[0][0]

    def getScoreIdByName(self,university_name):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT (score_id) FROM universities WHERE(name='%s')" % (university_name)
        cursor.execute(query)
        score_id = cursor.fetchone()
        db_connection.commit()
        cursor.close()
        return score_id[0]

    def getAllUniversityNamesAndIds(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT id,name from universities ORDER BY name"
        cursor.execute(query)
        universities_tuple = cursor.fetchall()
        cursor.close()
        return universities_tuple

    def getUniversitiesAndScoresOrderedByScore(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        cursor.execute("SELECT (name, city, country, average_score, address, phone_no, website) FROM universities,avg_score WHERE (universities.score_id = avg_score.id) ORDER BY average_score DESC")
        universities_list = cursor.fetchall();
        print(universities_list)

        list_of_tuples = []
        #for place,each_tuple in enumerate(universities_list, start=1) #for indexed traversing
        
        for each_tuple_of_tuples in universities_list:
            tuplesAsString = each_tuple_of_tuples[0]
            #print(type(tuplesAsString))
            #print(tuplesAsString) #tuplesAsStrings
            translation_table = dict.fromkeys(map(ord, '"()'), None) # {' " ' : None, '(':None ,  }
            tuplesAsString = tuplesAsString.translate(translation_table)
            #print(tuplesAsString)
            university_tuple = tuple(tuplesAsString.split(','))
            #print(type(university_tuple))
            list_of_tuples.append(university_tuple)


        db_connection.commit()
        cursor.close()
        return list_of_tuples


    def addScore(self,request_form):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        universities_table = universitiesTable()
        form_result_map = request_form.to_dict()
        university_name = form_result_map['university_selection']
        score_id = universities_table.getScoreIdByName(university_name)
        campus = int(form_result_map['campus'])
        social = int(form_result_map['social'])
        education = int(form_result_map['education'])
        cursor.execute("UPDATE avg_score SET score_by_campus= ( (score_by_campus * score_count) + %d) / (score_count+1) WHERE (id=%d)" % (campus,score_id))
        cursor.execute("UPDATE avg_score SET score_by_education= ( (score_by_education * score_count) + %d) / (score_count+1) WHERE (id=%d)" % (education,score_id))
        cursor.execute("UPDATE avg_score SET score_by_social_life= ( (score_by_social_life * score_count) + %d) / (score_count+1), score_count=score_count+1 WHERE (id=%d)" % (social,score_id))
        cursor.execute("UPDATE avg_score SET average_score=(score_by_campus+score_by_education+score_by_social_life)/3.0 WHERE (id=%d)" % (score_id))
        db_connection.commit()
        cursor.close()

        


class universityPhotosTable:

    def fetchAllPhotos(self,theListOfUniversityTuples):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        universities_table = universitiesTable()
        logoname = 'static/img/logo'
        backname = 'static/img/back'
        index = 1
        for each_tuple in theListOfUniversityTuples:
            university_id = universities_table.getUniversityIDbyName(each_tuple[0])
            query = "SELECT (logo) FROM university_photos WHERE(id=(SELECT (images_id) FROM universities WHERE (id=%d)) )" % (int(university_id))
            cursor.execute(query)
            imgdata = cursor.fetchone()
            if(imgdata[0] != None):
                image = base64.b64decode(imgdata[0])
            else:
                continue
            looplogoname = logoname + "%d.jpg" % (index)
            with open(looplogoname, 'wb') as logo:
                logo.write(image)  
            query = "SELECT (background) FROM university_photos WHERE(id=(SELECT (images_id) FROM universities WHERE (id=%d)) )" % (int(university_id))
            cursor.execute(query)
            imgdata = cursor.fetchone()
            if(imgdata[0] != None):
                image = base64.b64decode(imgdata[0])
            else:
                continue 
            loopbackname = backname + "%d.jpg" % (index)
            with open(loopbackname, 'wb') as back:
                back.write(image)
            index = index+1


    
    def updatePhoto(self,filename,photo_type,images_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        with open("static/img/%s" % (filename), "rb") as university_photo:
            if university_photo == None:
                print("Cannot open image.")
                return
            university_photo_encoded = base64.b64encode(university_photo.read())
            university_photo_encoded_str = university_photo_encoded.decode('utf-8')

            if photo_type == 'Logo':
                cursor.execute("UPDATE university_photos SET logo='%s' WHERE(id='%s')" % (university_photo_encoded_str, str(images_id) ))
            else:
                cursor.execute("UPDATE university_photos SET background='%s' WHERE(id='%s')" % (university_photo_encoded_str, str(images_id) ))

            db_connection.commit()
            cursor.close()


    def addPhoto(self,filename,photo_type,university_name):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        with open("static/img/%s" % (filename), "rb") as university_photo:
            if university_photo == None:
                print("Cannot open image.")
                return
            university_photo_encoded = base64.b64encode(university_photo.read())
            university_photo_encoded_str = university_photo_encoded.decode('utf-8')

            if photo_type == 'Logo':
                cursor.execute("INSERT INTO university_photos (logo) VALUES('%s')" % (university_photo_encoded_str))
                

            else:
                cursor.execute("INSERT INTO university_photos (background) VALUES('%s')" % (university_photo_encoded_str))

            db_connection.commit()
            cursor.execute("UPDATE universities SET images_id=(SELECT MAX(id) from university_photos) WHERE (name='%s')" % (university_name))
            db_connection.commit()
            cursor.close()




    def getPhoto(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT (logo) FROM university_photos WHERE(id=4)"
        

class eventsTable:

    def getAllEvents(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * FROM events ORDER BY(event_date)"
        cursor.execute(query)
        events_tuple = cursor.fetchall()
        cursor.close()
        return events_tuple


    def getEventsByClubId(self, club_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * FROM events WHERE(club_id=%d)" % (int(club_id))
        cursor.execute(query)
        events_tuple = cursor.fetchall()
        cursor.close()
        return events_tuple



    def addScore(self,form_result_map):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()

        event_id = int(form_result_map['eventId'])
        score = int(form_result_map['eventScore'])

        query = 'UPDATE events SET puan= ( (puan * number_of_evaluation) + %d) / (number_of_evaluation+1), number_of_evaluation=number_of_evaluation+1 WHERE (id=%d)' % (score,event_id)
        cursor.execute(query)
        db_connection.commit()
        cursor.close()

    def addEvent(self,request_form):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        event_added = 0
        form_request_map = request_form.to_dict()
        title = form_request_map['title']
        description = form_request_map['description']
        price = form_request_map['price']
        place = form_request_map['place']
        time = form_request_map['time_selection']
        date = form_request_map['date']
        duration = form_request_map['duration']
        club_name = form_request_map['club_selection']
        university_name = form_request_map['university_selection']
        universities_table = universitiesTable()
        university_id = universities_table.getUniversityIDbyName(university_name)
        club_id_query = "SELECT (clubs.id) FROM universities,clubs WHERE ((universities.id=clubs.university_id)AND(clubs.name='%s')AND(universities.id=%d))" % (club_name,university_id)

        cursor.execute(club_id_query)

        club_id = cursor.fetchone()
        print(club_id)
        add_event_query = "INSERT INTO events (title,description,price,place,event_date,event_time,duration,club_id,user_id) VALUES('%s','%s',%f,'%s','%s','%s',%d,%d,%d)" % (title,description,float(price),place,date,time,int(duration),int(club_id[0]),current_user.id)
        cursor.execute(add_event_query)
        db_connection.commit()
        event_added = 1
        return event_added

    def deleteEventById(self,event_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "DELETE FROM events WHERE(id=%d)" % (int(event_id))
        cursor.execute(query)
        db_connection.commit()
        cursor.close()


class commentsTable:

    def getAllComments(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * FROM comments"
        cursor.execute(query)
        comments_tuple = cursor.fetchall()
        cursor.close()
        return comments_tuple


    def getCommentsByEventId(self, event_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * FROM comments WHERE (event_id=%d)" % (int(event_id))
        cursor.execute(query)
        comments_tuple = cursor.fetchall()
        cursor.close()
        return comments_tuple


    def addComment(self,form_result_map):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()

        comment_title = form_result_map['commentTitle']
        comment_body = form_result_map['commentBody']
        event_id = int(form_result_map['eventId'])
        user_id = current_user.id
        user_nickname = current_user.nickname

        query = "INSERT INTO comments (title,body,event_id,user_id,user_nickname) VALUES('%s','%s',%d,%d,'%s')" % (comment_title,comment_body,event_id,user_id,user_nickname)
        cursor.execute(query)
        db_connection.commit()
        cursor.close()


    def updateUpvote(self,comment_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "UPDATE comments SET useful_no = (useful_no+1) WHERE (id=%d)" % (int(comment_id))
        cursor.execute(query)
        db_connection.commit()
        cursor.close()

    def updateDownvote(self,comment_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "UPDATE comments SET useless_no = (useless_no+1) WHERE (id=%d)" % (int(comment_id))
        cursor.execute(query)
        db_connection.commit()
        cursor.close()

    def deleteCommentById(self,comment_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "DELETE FROM comments WHERE(id=%d)" % (int(comment_id))
        cursor.execute(query)
        db_connection.commit()
        cursor.close()

