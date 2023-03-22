from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, constants, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import custom_id_validation, validation


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage(constants.SHORT_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": link.original})


@app.route("/api/id/", methods=["POST"])
def add_url_map():
    data = request.get_json(silent=True)
    if not validation(data):
        url = data.get("url")
        custom_id = custom_id_validation(data)
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
