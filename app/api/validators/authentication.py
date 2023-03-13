from email_validator import validate_email


def id_validator(data):
    if data.isdecimal() and len(data) == 11:
        return True
    

def name_validator(data):
    if data.isalpha():
        return True


def mail_validator(data):

    try:
        emailObject = validate_email(data)
        return True

    except :
        return False
        
     
def number_validator(data):
    if data.isdecimal() and len(data) == 9:
        return True




def user_exist_check(parser,User):
        if bool(User.query.filter_by(email = parser["email"]).first()):
            return "This mail is already redgistered", 400

        if bool(User.query.filter_by(number = parser["number"]).first()):
            return "This number is already redgistered", 400

        if bool(User.query.filter_by(personal_id = parser["personal_id"]).first()):
            return "This personal_id is already redgistered", 400






def check_validators(parser, User, user_check = True):

        if not name_validator(parser["name"]):
            return "Invalid name", 400

        if not name_validator(parser["lastname"]):
            return "Invalid lastname", 400

        if not mail_validator(parser["email"]):
            return "Invalid email",   400

        if not number_validator(parser["number"]):
            return "Invalid number",   400     

        if not id_validator(parser["personal_id"]):
            return "Invalid personal_id", 400

        if parser["role"] == "მოსწავლე" and not name_validator(parser["parent_name"]):
            return "Invalid parent_name", 400

        if parser["role"] == "მოსწავლე" and not name_validator(parser["parent_lastname"]):
            return "Invalid parent_lastname", 400

        if parser["role"] == "მოსწავლე" and not number_validator(parser["parent_number"]):
            return "Invalid parent_number", 400

        if not parser["terms"]:
            return "Not accepted terms of service", 400


        if user_check and parser["password"] != parser["conf_password"]:
            return "passwords do not match", 400


    

        # user exist check
        if user_check:
            user_exist_check(parser,User)

