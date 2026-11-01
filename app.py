"""Flask presentation/control layer for the PhishGuard demo."""

from flask import Flask, render_template, request
from facade import PhishingDetectorFacade

app = Flask(__name__)
detector = PhishingDetectorFacade()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    submitted_url = ""

    if request.method == "POST":
        submitted_url = request.form.get("url", "").strip()
        result = detector.analyze_url(submitted_url)

    return render_template(
        "index.html",
        result=result,
        submitted_url=submitted_url,
    )


if __name__ == "__main__":
    # Debug mode is convenient for local college development only.
    app.run(debug=True)
