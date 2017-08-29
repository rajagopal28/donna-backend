from flask import jsonify
import datetime

from app.models.chores import Announcement


def validate_and_add_announcement(form):
    now = datetime.datetime.now()
    title = form.get("title", None)
    description = form.get("description", None)
    e_start = form.get("validFrom", now.timestamp())
    e_end = form.get("validTill", now.timestamp())
    category = form.get("category", None)
    # datetime.fromtimestamp(your_timestamp / 1e3)
    start = datetime.datetime.fromtimestamp(float(e_start))
    end = datetime.datetime.fromtimestamp(float(e_end))
    if title and description and category:
        ancmt = Announcement(title=title, description=description, category=category, valid_from=start, valid_till=start)
        ancmt.save()
        return True, ancmt
    else:
        return False, None

def fetch_all_announcement():
    announcements = Announcement.query.all()
    return [a.to_dict() for a in announcements]
