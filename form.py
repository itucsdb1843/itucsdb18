import re
import datetime

class formValidation:
    
    def validateEmail(self, email):
        match = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$)", email)
        if match == None:
            return False
        return True
        
        
    def validateDate(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False
        return True
        
        
    def validateScore(self, form_result_map):
        campus = int(form_result_map['campus'])
        social = int(form_result_map['social'])
        education = int(form_result_map['education'])
        if int(campus)>100 or int(social)>100 or int(education)>100:
            return False
            if int(campus) + int(social) + int(education) == 300:
                return False
        return True

		
