from database.MongoDB import MongoDB

MAIL_SENDER = ""
MAIL_PASSWORD = ""
CURRENT_DB = MongoDB(host="localhost", port=27017)


'''MONGODB = MongoDB(host="localhost", port=27017)

from repositories import UserRepository

USER_REPOSITORY = UserRepository(MONGODB)
'''
