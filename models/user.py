from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin):
 
    def __init__(self,user_tuple):
        self.id = user_tuple[0]
        self.name = user_tuple[1]
        self.surname = user_tuple[2]
        self.nickname = user_tuple[3]
        self.password = user_tuple[4]
        self.email = user_tuple[5]
        self.status = user_tuple[6]
        self.city = user_tuple[7]
        self.university_id = user_tuple[8]
        self.last_login = user_tuple[9]
        self.signin_time = user_tuple[10]
        
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
        
    def get_id(self):
        return self.id



class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = 'Guest'

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return True
        
    def is_active(self):
        return True




