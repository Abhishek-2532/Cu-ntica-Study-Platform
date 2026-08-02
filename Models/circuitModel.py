from bson import ObjectId
from datetime import datetime
from config.database import db

class CircuitModel:
    circuits = db["circuits"]

    @staticmethod
    def create_circuit(user_id, name, qubits, gates):
        circuit_data = {
            "user_id": user_id,
            "name": name,
            "qubits": int(qubits),
            "gates": gates,
            "updated_at": datetime.utcnow()
        }
        res = CircuitModel.circuits.insert_one(circuit_data)
        return str(res.inserted_id)

    @staticmethod
    def get_circuits_by_user(user_id):
        cursor = CircuitModel.circuits.find({"user_id": user_id}).sort("updated_at", -1)
        res = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            res.append(doc)
        return res

    @staticmethod
    def get_circuit(circuit_id, user_id):
        from bson.errors import InvalidId
        try:
            doc = CircuitModel.circuits.find_one({
                "_id": ObjectId(circuit_id),
                "user_id": user_id
            })
            if doc:
                doc["_id"] = str(doc["_id"])
                return doc
            return None
        except (InvalidId, TypeError):
            return None

    @staticmethod
    def update_circuit(circuit_id, user_id, name, qubits, gates):
        from bson.errors import InvalidId
        try:
            res = CircuitModel.circuits.update_one(
                {"_id": ObjectId(circuit_id), "user_id": user_id},
                {
                    "$set": {
                        "name": name,
                        "qubits": int(qubits),
                        "gates": gates,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return res.modified_count > 0 or res.matched_count > 0
        except (InvalidId, TypeError):
            return False

    @staticmethod
    def delete_circuit(circuit_id, user_id):
        from bson.errors import InvalidId
        try:
            res = CircuitModel.circuits.delete_one({
                "_id": ObjectId(circuit_id),
                "user_id": user_id
            })
            return res.deleted_count > 0
        except (InvalidId, TypeError):
            return False
