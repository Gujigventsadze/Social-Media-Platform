from datetime import datetime
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

app = Flask(__name__)

users = []
posts_arr = []
user_id = 1


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


# Registering new user
@app.route("/add-user", methods=["POST", "GET"])
def new_user():
    global user_id
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            error = "Passwords do not match"
            return render_template("register.html", error=error)
        else:
            users.append({
                "id": user_id,
                "email": email,
                "password": password
            })
            user_id += 1
            print(users)
            return redirect(url_for('home'))
    return render_template("register.html")


@app.route("/login-user", methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_found = False

        for user in users:
            if user["email"] == email:
                user_found = True
                if user["password"] == password:
                    return redirect(f"/content-page/{email.split('@')[0]}")
                else:
                    error = "Wrong Password"
                    return render_template("index.html", error=error)

        if not user_found:
            error = "No email found"
            return render_template("index.html", error=error)

    return redirect(url_for("home"))

@app.route("/content-page/<user>")
def content_page(user):
    return render_template("user.html", user=user, posts=posts_arr[::-1])

@app.route("/create-post/<user>", methods=["POST"])
def create_post(user):
    if request.method == "POST":
        body = request.form["post"]
        time = datetime.now()
        posts_arr.append({
            "user": user,
            "body": body,
            "time": time.strftime("%H:%M  %d-%m")
        })
        return redirect(url_for("content_page", user=user))

    return redirect(url_for("home"))

@app.route("/log-out")
def log_out():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
