from config.database import db
from bson import ObjectId
from datetime import datetime

class UserModel:

    collection = db["users"]

    @staticmethod
    def create_user(data):
        return UserModel.collection.insert_one(data)

    @staticmethod
    def get_all_users():
        return list(UserModel.collection.find())

    @staticmethod
    def get_user_by_email(email):
        return UserModel.collection.find_one({"email": email})

    @staticmethod
    def is_email_exists(email):
        return UserModel.collection.find_one({"email": email})


    @staticmethod
    def get_user_by_id(user_id):
        return UserModel.collection.find_one(
            {"_id": ObjectId(user_id)}
        )

    @staticmethod
    def update_user(user_id, data):
        return UserModel.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )

    @staticmethod
    def delete_user(user_id):
        return UserModel.collection.delete_one(
            {"_id": ObjectId(user_id)}
        )
    @staticmethod
    def update_last_login(user_id):
        return UserModel.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "last_login": datetime.utcnow()
                }
            }
        )

    @staticmethod
    def get_profile(user_id, email):

        return UserModel.collection.find_one({

            "_id": ObjectId(user_id),

            "email": email

        })

        