from flask import Response, render_template, request

from app import app
from app.utils.constants import days, months, years
from app.utils.post_to_csv import create_csv
from app.utils.times import pack_date_string
from app.vk_parsing import fetch_posts_after_start_date, get_all_posts


@app.route("/")
def input_form():
    return render_template("input_form.html", days=days, months=months, years=years)


@app.route("/stats")
def eval_stats():
    url = request.args.get("url")
    request_days = request.args.get("days")
    request_months = request.args.get("months")
    request_years = request.args.get("years")

    date_row = pack_date_string(request_days, request_months, request_years)

    fetch_posts_after_start_date(url, date_row)
    print(get_all_posts())
    return render_template("stats.html")


@app.route("/csv")
def get_csv():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = create_csv(get_all_posts())
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=my_csv.csv"},
    )
