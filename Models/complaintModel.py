from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from config.database import db


class ComplaintModel:

    complaints_col = db["complaints"]

    @staticmethod
    def create_complaint(user_id, name, email, category, priority, title, description):
        """
        Creates and stores a new complaint in MongoDB.
        """
        if not user_id or not category or not title or not description:
            return False, "Required fields are missing: category, title, description.", None

        complaint_doc = {
            "user_id": str(user_id),
            "name": name or "Anonymous User",
            "email": email or "",
            "category": category,
            "priority": priority or "Normal",
            "title": title,
            "description": description,
            "status": "Pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            result = ComplaintModel.complaints_col.insert_one(complaint_doc)
            complaint_id = str(result.inserted_id)
            return True, "Complaint submitted successfully.", complaint_id
        except Exception as e:
            return False, f"Failed to submit complaint: {str(e)}", None

    @staticmethod
    def get_user_complaints(user_id):
        """
        Retrieves all complaints submitted by a given user_id.
        """
        if not user_id:
            return []

        try:
            cursor = ComplaintModel.complaints_col.find(
                {"user_id": str(user_id)}
            ).sort("created_at", -1)

            complaints = []
            for doc in cursor:
                complaints.append({
                    "id": str(doc["_id"]),
                    "user_id": doc.get("user_id"),
                    "name": doc.get("name"),
                    "email": doc.get("email"),
                    "category": doc.get("category"),
                    "priority": doc.get("priority"),
                    "title": doc.get("title"),
                    "description": doc.get("description"),
                    "status": doc.get("status", "Pending"),
                    "created_at": doc.get("created_at")
                })

            return complaints
        except Exception:
            return []

    @staticmethod
    def get_all_complaints():
        """
        Retrieves all complaints (for admin review).
        """
        try:
            cursor = ComplaintModel.complaints_col.find().sort("created_at", -1)
            complaints = []
            for doc in cursor:
                complaints.append({
                    "id": str(doc["_id"]),
                    "user_id": doc.get("user_id"),
                    "name": doc.get("name"),
                    "email": doc.get("email"),
                    "category": doc.get("category"),
                    "priority": doc.get("priority"),
                    "title": doc.get("title"),
                    "description": doc.get("description"),
                    "status": doc.get("status", "Pending"),
                    "created_at": doc.get("created_at")
                })
            return complaints
        except Exception:
            return []
