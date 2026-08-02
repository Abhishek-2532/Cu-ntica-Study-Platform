from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from config.database import db


class UserCourseModel:

    users = db["users"]

    @staticmethod
    def update_course_progress(user_id, course_id, progress, last_lesson):

        # Bug #7 Fix: ObjectId(user_id) raises bson.errors.InvalidId if user_id
        # is not a valid 24-character hex string. Guard it here so the model
        # returns a clean (False, message) tuple instead of throwing.
        try:
            user = UserCourseModel.users.find_one({
                "_id": ObjectId(user_id)
            })
        except InvalidId:
            return False, f"Invalid user_id format: '{user_id}' is not a valid MongoDB ObjectId."

        if not user:
            return False, "User Not Found"

        completed_lessons = user.get("completed_lessons", [])
        completed_courses = user.get("completed_courses", [])

        found = False

        for lesson in completed_lessons:

            if lesson["course_id"] == course_id:

                lesson["progress"] = progress
                lesson["last_lesson"] = last_lesson
                lesson["updated_at"] = datetime.utcnow()

                found = True
                break

        if not found:

            completed_lessons.append({

                "course_id": course_id,
                "progress": progress,
                "last_lesson": last_lesson,
                "updated_at": datetime.utcnow()

            })

        if progress >= 100:

            already = False

            for c in completed_courses:

                if c == course_id:
                    already = True
                    break

            if not already:
                completed_courses.append(course_id)

        UserCourseModel.users.update_one(

            {
                "_id": ObjectId(user_id)
            },

            {
                "$set": {

                    "completed_lessons": completed_lessons,

                    "completed_courses": completed_courses,

                    "updated_at": datetime.utcnow()

                }

            }

        )

        return True, "Progress Updated"