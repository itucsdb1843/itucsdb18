import os
import psycopg2 as dbapi2
import datetime
from server import login_manager, bcrypt, photos, app
from flask_login import login_user, current_user, logout_user
import base64
from models.user import User

global_database_url = "postgres://vfssrhxrwgmkjb:a9106ca3abea0a13108ea5de84abdf8f06ff2678d5488f0155f435ef0c8d5bba@ec2-107-20-211-10.compute-1.amazonaws.com:5432/desn7uabq7s0di"

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
            #print(university_tuple)
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

        from form import formValidation
        form_validation = formValidation()
        score_validation_result = form_validation.validateScode(form_result_map)
        if not score_validation_result:
            return False

        if score_id:
            cursor.execute("UPDATE avg_score SET score_by_campus= ( (score_by_campus * score_count) + %d) / (score_count+1) WHERE (id=%d)" % (campus,score_id))
            cursor.execute("UPDATE avg_score SET score_by_education= ( (score_by_education * score_count) + %d) / (score_count+1) WHERE (id=%d)" % (education,score_id))
            cursor.execute("UPDATE avg_score SET score_by_social_life= ( (score_by_social_life * score_count) + %d) / (score_count+1), score_count=score_count+1 WHERE (id=%d)" % (social,score_id))
            cursor.execute("UPDATE avg_score SET average_score=(score_by_campus+score_by_education+score_by_social_life)/3.0 WHERE (id=%d)" % (score_id))
        else:
            cursor.execute("INSERT INTO avg_score (score_by_campus,score_by_education,score_by_social_life) VALUES (%d,%d,%d)" % (int(campus),int(education),int(social)))
            db_connection.commit()
            cursor.execute("SELECT MAX(id) FROM avg_score")
            new_score_id = cursor.fetchone()
            cursor.execute("UPDATE avg_score SET average_score=(score_by_campus+score_by_education+score_by_social_life)/3.0 WHERE (id=%d)" % (new_score_id[0]))
            cursor.execute("UPDATE universities SET score_id=%d WHERE(name='%s')" % (new_score_id[0],university_name))

        db_connection.commit()
        cursor.close()
        return True

        

class usersTable:

    def editUserProfileInfo(self,form_result_map):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        changes_are_made = 0
        name = form_result_map['firstname']
        if name:
            query = "UPDATE users SET name='%s' WHERE (id=%d)" % (name,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            changes_are_made = 1

        surname = form_result_map['lastname']
        if surname:
            query = "UPDATE users SET surname='%s' WHERE (id=%d)" % (surname,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            changes_are_made = 1

        nickname = form_result_map['nickname']
        if nickname:
            query = "UPDATE users SET nickname='%s' WHERE (id=%d)" % (nickname,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            changes_are_made = 1

        password = form_result_map['password']
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            query = "UPDATE users SET password='%s' WHERE (id=%d)" % (hashed_password,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            changes_are_made = 1

        status = form_result_map['status']
        if status:
            query = "UPDATE users SET status='%s' WHERE (id=%d)" % (status,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            changes_are_made = 1

        city = form_result_map['city']
        if city:
            query = "UPDATE users SET city='%s' WHERE (id=%d)" % (city,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            changes_are_made = 1

        universities_table = universitiesTable()
        university_name = form_result_map['university_selection']
        if university_name != 'None':
            university_id = universities_table.getUniversityIDbyName(university_name)
            university_id_as_str = str(university_id)
        else:
            university_id_as_str = "NULL"
        query = "UPDATE users SET university_id=%s WHERE (id=%d)" % (university_id_as_str,current_user.id)
        cursor.execute(query)
        db_connection.commit()

        cursor.close()
        return changes_are_made


    def changeAvatar(self,request_files):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        avatar_changed = 0
        filename = photos.save(request_files['photo'])
        with open("static/img/%s" % (filename), "rb") as user_avatar:
            if user_avatar == None:
                print("Cannot open image.")
                return avatar_changed
            user_avatar_encoded = base64.b64encode(user_avatar.read())
            user_avatar_encoded_str = user_avatar_encoded.decode('utf-8')

            query = "UPDATE users SET avatar='%s' WHERE(id=%d)" % (user_avatar_encoded_str,current_user.id)
            cursor.execute(query)
            db_connection.commit()
            avatar_changed = 1
            return avatar_changed



    def addUser(self,form_result_map):
        
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()

        name = form_result_map['firstname']
        surname = form_result_map['lastname']
        nickname = form_result_map['nickname']
        email = form_result_map['email']

        password = form_result_map['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        status = form_result_map['status']
        city = form_result_map['city']

        universities_table = universitiesTable()
        university_name = form_result_map['university_selection']
        if university_name != 'None':
            university_id = universities_table.getUniversityIDbyName(university_name)
            university_id_as_str = str(university_id)
        else:
            university_id_as_str = "NULL"

        add_user_query = "INSERT INTO users (name, surname, nickname, email, password, status, city, university_id) VALUES('%s','%s','%s','%s','%s','%s','%s',%s)" % (name,surname,nickname,email,hashed_password,status,city,university_id_as_str)

        cursor.execute(add_user_query)
        db_connection.commit()
        cursor.close()


    def makeUserLoggedIn(self, form_nickname, form_password):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * FROM users WHERE (nickname='%s')" % (form_nickname)
        cursor.execute(query)
        user_tuple = cursor.fetchone()
        db_connection.commit()
        
        if(user_tuple != None):
            password_check = bcrypt.check_password_hash(user_tuple[4],form_password)
            if(password_check):
                #print(password_check)
                login_user(self.getUserObjectByID(user_tuple[0]))
            else:
                cursor.close()
                return False
        else:
            cursor.close()
            return False
        cursor.close()
        db_connection.commit()
        return True


    def getUserObjectByID(self, user_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * FROM users WHERE (id = %d)" % (user_id)
        cursor.execute(query)
        user_tuple = cursor.fetchone()
        if user_tuple:
            user = User(user_tuple)
            return user
        return None

    def getAvatar(self,user_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT (avatar) FROM users WHERE(id=%d)" % (user_id)
        cursor.execute(query)
        imgdata = cursor.fetchone()
        if imgdata[0]:
            image = base64.b64decode(imgdata[0])
        else:
            return None

        filename = 'static/img/userProfile.jpg'
        with open(filename, 'wb') as photo:
            photo.write(image)
            #print("avatar fetched")
            #os.remove(filename)
            #print("avatar removed")
        #return photo




class universityPhotosTable:

    def fetchAllPhotos(self,theListOfUniversityTuples):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        universities_table = universitiesTable()
        logoname = 'static/img/logo'
        backname = 'static/img/back'

        photoExistsList = []


        index = 1
        for each_tuple in theListOfUniversityTuples:

            logo_back = ()

            university_id = universities_table.getUniversityIDbyName(each_tuple[0])

            cursor.execute("SELECT images_id FROM universities WHERE(id=%d)" % (university_id))
            images_id_tuple = cursor.fetchone()
            images_id = images_id_tuple[0]



            logo_back = list(logo_back)

            if images_id:
                
                query = "SELECT (logo) FROM university_photos WHERE(id=(SELECT (images_id) FROM universities WHERE (id=%d)) )" % (int(university_id))
                cursor.execute(query)
                imgdata = cursor.fetchone()
                if imgdata[0]:
                    logo_back.append(1)
                    image = base64.b64decode(imgdata[0])
                    looplogoname = logoname + "%d.jpg" % (index)
                    with open(looplogoname, 'wb') as logo:
                        logo.write(image)
                else:
                    logo_back.append(0)
            else:
                logo_back.append(0)

            
            if images_id:
                
                query = "SELECT (background) FROM university_photos WHERE(id=(SELECT (images_id) FROM universities WHERE (id=%d)) )" % (int(university_id))
                cursor.execute(query)
                imgdata = cursor.fetchone()
                if imgdata[0]:
                    logo_back.append(1)
                    image = base64.b64decode(imgdata[0])
                    loopbackname = backname + "%d.jpg" % (index)
                    with open(loopbackname, 'wb') as back:
                        back.write(image)
                else:
                    logo_back.append(0)
            else:
                logo_back.append(0)

            logo_back = tuple(logo_back)
            photoExistsList.append(logo_back)
            index = index+1

        return photoExistsList


    
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
        #cursor.execute(query)
        #imgdata = cursor.fetchone()
        #if(imgdata != None):
        #    image = base64.b64decode(imgdata[0])
        #else:
        #    return None

        #filename = 'temp.jpg'
        #with open(filename, 'wb') as photo:
        #    photo.write(image)
        #return photo


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

    def addEventByClubId(self,form_request_map, club_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        
        from form import formValidation
        form_validation = formValidation()
        date = form_request_map['date']
        date_validation_result = form_validation.validateDate(date)
        if not date_validation_result:
            return False

        title = form_request_map['title']
        description = form_request_map['description']
        price = form_request_map['price']
        place = form_request_map['place']
        time = form_request_map['time_selection']
        duration = form_request_map['duration']

        add_event_query = "INSERT INTO events (title,description,price,place,event_date,event_time,duration,club_id,user_id) VALUES('%s','%s',%f,'%s','%s','%s',%d,%d,%d)" % (title,description,float(price),place,date,time,int(duration),int(club_id),current_user.id)
        cursor.execute(add_event_query)
        db_connection.commit()

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

class clubsTable:
    def getClubNames(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        club_names = []
        cursor.execute("SELECT name FROM clubs")
        club_names_list = cursor.fetchall()
        for each_club_name in club_names_list:
            club_names.append(each_club_name[0])
        db_connection.commit()
        cursor.close()
        return club_names

    def getAllClubs(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * from clubs ORDER BY name"
        cursor.execute(query)
        clubs_tuple = cursor.fetchall()
        cursor.close()
    
        return clubs_tuple

    def getClubById(self, club_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT * from clubs WHERE (id=%d)" % (int(club_id))
        cursor.execute(query)
        club = cursor.fetchone()
        cursor.close()

        return club


class chainsTable:

    def getAllChainsOfTheUser(self):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM chains")
        chains = cursor.fetchall()
        cursor.close()
        return chains

    def getChainIdByTitle(self,chain_name):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        cursor.execute("SELECT (id) FROM chains WHERE (title='%s')" % (chain_name))
        chain_id = cursor.fetchone()
        cursor.close()
        return int(chain_id[0])

    def createChain(self,chain_title):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO chains (title,user_id) VALUES('%s',%d)" % (chain_title,current_user.id))
        db_connection.commit()
        cursor.close()



class todosTable:

    def addToDo(self,request_form):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()

        form_result_map = request_form.to_dict()
        title = form_result_map['chain_title_selection']
        body = form_result_map['description']
        start = form_result_map['startDate']
        end = form_result_map['expEndDate']
        chains_table = chainsTable()
        chain_id = chains_table.getChainIdByTitle(title)

        cursor.execute("INSERT INTO todos (body,start_date,expected_end_date,chain_id) VALUES ('%s','%s','%s',%d)" % (body,start,end,chain_id))
        db_connection.commit()
        cursor.close()

    def getAllTodosOfAChain(self,chain_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM todos WHERE (chain_id=%d)" % (int(chain_id)))
        todos = cursor.fetchall()
        cursor.close()
        return todos








