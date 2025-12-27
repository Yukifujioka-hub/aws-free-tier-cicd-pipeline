from flask import Flask, render_template_string
import requests

app = Flask(__name__)

API_URL = "https://zenquotes.io/api/random"

TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Quote of the Day</title>
  </head>
  <body>
    <h1>Quote of the Day</h1>
    {% if quote and author %}
      <p>“{{ quote }}”</p>
      <p>— {{ author }}</p>
    {% else %}
      <p>Failed to load quote.</p>
    {% endif %}
  </body>
</html>
"""


def fetch_quote():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        quote = data[0].get("q")
        author = data[0].get("a")

        return {"quote": quote, "author": author}
    except Exception:
        return None


@app.route("/")
def index():
    data = fetch_quote()
    if data:
        return render_template_string(
            TEMPLATE,
            quote=data["quote"],
            author=data["author"]
        )
    return render_template_string(TEMPLATE, quote=None, author=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
