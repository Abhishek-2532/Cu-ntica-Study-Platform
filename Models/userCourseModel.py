from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from config.database import db


# Badge definitions: (badge_id, title, description, icon, condition_check)
BADGE_DEFINITIONS = [
    {
        "id": "first_module",
        "title": "Quantum Novice",
        "description": "Completed your first module",
        "icon": "fa-solid fa-seedling",
        "condition": lambda completed_courses, **_: len(completed_courses) >= 1
    },
    {
        "id": "three_modules",
        "title": "Knowledge Seeker",
        "description": "Completed 3 modules",
        "icon": "fa-solid fa-book-open",
        "condition": lambda completed_courses, **_: len(completed_courses) >= 3
    },
    {
        "id": "five_modules",
        "title": "Quantum Explorer",
        "description": "Completed 5 modules",
        "icon": "fa-solid fa-compass",
        "condition": lambda completed_courses, **_: len(completed_courses) >= 5
    },
    {
        "id": "all_modules",
        "title": "Quantum Master",
        "description": "Completed all 10 modules",
        "icon": "fa-solid fa-crown",
        "condition": lambda completed_courses, **_: len(completed_courses) >= 10
    },
    {
        "id": "xp_500",
        "title": "Rising Star",
        "description": "Earned 500+ Experience Points",
        "icon": "fa-solid fa-star",
        "condition": lambda xp=0, **_: xp >= 500
    },
    {
        "id": "xp_2000",
        "title": "Quantum Prodigy",
        "description": "Earned 2000+ Experience Points",
        "icon": "fa-solid fa-trophy",
        "condition": lambda xp=0, **_: xp >= 2000
    },
]


class UserCourseModel:

    users = db["users"]
    courses_col = db["courses"]

    @staticmethod
    def update_course_progress(user_id, course_id, progress, last_lesson):

        try:
            user = UserCourseModel.users.find_one({
                "_id": ObjectId(user_id)
            })
        except InvalidId:
            return False, "Invalid user_id format.", {}

        if not user:
            return False, "User Not Found", {}

        completed_lessons = user.get("completed_lessons", [])
        completed_courses = user.get("completed_courses", [])
        current_xp = user.get("xp", 0) or 0
        current_coins = user.get("coins", 0) or 0
        current_badges = user.get("badges", []) or []
        current_certificates = user.get("certificates", []) or []

        # Track old progress to calculate delta
        old_progress = 0
        found = False

        for lesson in completed_lessons:
            if lesson["course_id"] == course_id:
                old_progress = lesson.get("progress", 0)
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

        # ─── GAMIFICATION: Calculate XP and Coins from progress delta ───
        delta_progress = max(0, progress - old_progress)
        xp_gained = delta_progress * 5        # 5 XP per 1% progress
        coins_gained = delta_progress * 1     # 1 coin per 1% progress

        # ─── COURSE COMPLETION BONUS ───
        is_new_completion = False
        if progress >= 100:
            already = course_id in completed_courses
            if not already:
                completed_courses.append(course_id)
                is_new_completion = True
                xp_gained += 500      # Completion bonus
                coins_gained += 100   # Completion bonus

        new_xp = current_xp + xp_gained
        new_coins = current_coins + coins_gained

        # ─── CERTIFICATE GENERATION on first completion ───
        new_certificates = list(current_certificates)
        if is_new_completion:
            # Get course title from database
            course_title = course_id  # fallback
            try:
                course_doc = UserCourseModel.courses_col.find_one(
                    {"slug": course_id}
                )
                if course_doc:
                    course_title = course_doc.get("title", course_id)
            except Exception:
                pass

            # Check if certificate already exists
            cert_exists = any(
                c.get("course_id") == course_id for c in new_certificates
            )
            if not cert_exists:
                new_certificates.append({
                    "course_id": course_id,
                    "title": course_title,
                    "issued_at": datetime.utcnow().isoformat(),
                    "type": "completion"
                })

        # ─── BADGE EVALUATION ───
        new_badges = list(current_badges)
        existing_badge_ids = {b.get("id") for b in new_badges}

        for badge_def in BADGE_DEFINITIONS:
            if badge_def["id"] not in existing_badge_ids:
                try:
                    earned = badge_def["condition"](
                        completed_courses=completed_courses,
                        xp=new_xp
                    )
                except Exception:
                    earned = False

                if earned:
                    new_badges.append({
                        "id": badge_def["id"],
                        "title": badge_def["title"],
                        "description": badge_def["description"],
                        "icon": badge_def["icon"],
                        "earned_at": datetime.utcnow().isoformat()
                    })

        # ─── PERSIST ALL UPDATES ───
        UserCourseModel.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "completed_lessons": completed_lessons,
                    "completed_courses": completed_courses,
                    "xp": new_xp,
                    "coins": new_coins,
                    "badges": new_badges,
                    "certificates": new_certificates,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        # Build rewards summary for frontend
        rewards = {
            "xp_gained": xp_gained,
            "coins_gained": coins_gained,
            "total_xp": new_xp,
            "total_coins": new_coins,
            "is_new_completion": is_new_completion,
            "badges_count": len(new_badges),
            "certificates_count": len(new_certificates),
        }

        return True, "Progress Updated", rewards