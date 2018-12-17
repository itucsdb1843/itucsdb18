import os
import psycopg2 as dbapi2
from server import login_manager, bcrypt, photos, app
from flask_login import login_user, current_user, logout_user
import base64
from models.user import User

global_database_url = "postgres://itucs:itucspw@localhost:32768/itucsdb"




class usersTable:

    #def __init__(self):
    #    if os.getenv("DATABASE_URL") is None:
    #        self.url = "postgres://itucs:itucspw@localhost:32769/itucsdb"
    #    else:
    #        self.url = os.getenv("DATABASE_URL")
    

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
    
        print(add_user_query)
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
        user = User(user_tuple)
        return user

    def getAvatar(self,user_id):
        db_connection = dbapi2.connect(global_database_url)
        cursor = db_connection.cursor()
        query = "SELECT (avatar) FROM users WHERE(id=%d)" % (user_id)
        cursor.execute(query)
        imgdata = cursor.fetchone()
        if(imgdata[0] != None):
            image = base64.b64decode(imgdata[0])
        else:
            return None

        filename = 'static/img/userProfile.jpg'
        with open(filename, 'wb') as photo:
            photo.write(image)
            print("avatar fetched")
            #os.remove(filename)
            #print("avatar removed")
        #return photo




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








