from bson import ObjectId
from config.database import db

class CourseModel:

    collection = db["courses"]

    @staticmethod
    def get_all_courses():
        return list(
            CourseModel.collection.find(
                {},
                {
                    "html_content": 0
                }
            )
        )

    @staticmethod
    def get_course(course_id):

        return CourseModel.collection.find_one({

            "_id": ObjectId(course_id)

        })

    @staticmethod
    def get_completed_courses(user_id,email):

        user=db["users"].find_one({

            "_id":ObjectId(user_id),

            "email":email

        })

        if not user:
            return []

        return user.get("completed_courses",[])