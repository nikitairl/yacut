from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


@app.route("/", methods=["POST", "GET"])
def index() -> str:
    form = URLForm()

    if not form.validate_on_submit():
        return render_template("index.html", form=form)

    if not form.custom_id.data:
        form.custom_id.data = URLMap.get_unique_short_id()

    if not URLMap.available_short(form.custom_id.data):
        flash(f"Имя {form.custom_id.data} уже занято!")
        return render_template("index.html", form=form)

    result_object = URLMap(
        original=form.original_link.data,
        short=form.custom_id.data,
    )
    db.session.add(result_object)
    db.session.commit()
    form.custom_id.data = None
    return render_template(
        "index.html",
        form=form,
        short_link=url_for(
            "redirect_to_url_view",
            short_id=result_object.short,
            _external=True,
        ),
    )


@app.route("/<string:short_id>", strict_slashes=False, methods=["GET"])
def redirect_to_url_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)
