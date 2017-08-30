from flask import jsonify
import datetime

from app.models.chores import Announcement


def validate_and_add_announcement(form):
    now = datetime.datetime.now()
    title = form.get("title", None)
    description = form.get("description", None)
    e_start = form.get("validFrom", now.timestamp()*1e3)
    e_end = form.get("validTill", now.timestamp()*1e3)
    category = form.get("category", None)
    # datetime.fromtimestamp(your_timestamp / 1e3)
    start = datetime.datetime.fromtimestamp(float(e_start)/1e3)
    end = datetime.datetime.fromtimestamp(float(e_end)/1e3)
    if title and description and category:
        ancmt = Announcement(title=title, description=description, category=category, valid_from=start, valid_till=end)
        ancmt.save()
        return jsonify(success=True, item=ancmt.to_dict()), 200
    else:
        return jsonify(success=False, message="Missing Fields!!!"), 401

def fetch_all_announcement():
    announcements = Announcement.query.all()
    response = [a.to_dict() for a in announcements]
    return jsonify(items=response, success=True)
