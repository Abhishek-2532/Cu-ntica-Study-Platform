import os
import json
from config.database import db

def seed_courses():
    filepath = os.path.join("database", "courses.json")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            courses = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    collection = db["courses"]
    inserted_count = 0
    updated_count = 0

    print("Seeding courses into MongoDB...")
    for course in courses:
        slug = course.get("slug")
        if not slug:
            continue
        
        # Keep datetime fields clean
        course["created_at"] = "datetime.utcnow()"
        course["updated_at"] = "datetime.utcnow()"

        # Upsert by slug
        result = collection.update_one(
            {"slug": slug},
            {"$set": course},
            upsert=True
        )

        if result.matched_count > 0:
            updated_count += 1
        else:
            inserted_count += 1

    print(f"Seeding completed successfully!")
    print(f" - Inserted (New): {inserted_count}")
    print(f" - Updated (Existing): {updated_count}")

if __name__ == "__main__":
    seed_courses()
