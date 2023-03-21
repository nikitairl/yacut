import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, constants, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage(constants.SHORT_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": link.original})


@app.route("/api/id/", methods=["POST"])
def add_url_map():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(constants.MISSING_REQUEST_BODY)
    custom_id = data.get("custom_id")
    url = data.get("url")
    if "url" not in data:
        raise InvalidAPIUsage(constants.URL_IS_REQUIRED_FIELD)
    try:
        if custom_id is None:
            custom_id = URLMap.get_unique_short_id()
        if len(custom_id) > 6:
            raise InvalidAPIUsage(constants.INVALID_SHORT_LINK)
        if re.match(constants.REGEX, custom_id) is None:
            raise InvalidAPIUsage(constants.INVALID_SHORT_LINK)
        if not URLMap.available_short(custom_id):
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
        urlmap = URLMap(
            original=url,
            short=custom_id,
        )
        db.session.add(urlmap)
        db.session.commit()
        response = {
            "url": urlmap.original,
            "short_link": url_for(
                "redirect_to_url_view",
                short_id=urlmap.short,
                _external=True,
            ),
        }
        return jsonify(response), HTTPStatus.CREATED

    except ValueError:
        raise InvalidAPIUsage(constants.INVALID_SHORT_LINK)
