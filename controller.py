from bot_script import app
from rss_parser import parse_planetpy_rss  # Import the RSS parsing function

@app.route("/user/signup")
def user_signup():
    return "User Signup Page"

@app.route("/rss")
def rss_feed():
    items = parse_planetpy_rss()
    return {"rss_feed": items}
