from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main_view():
    return render_template("index.html")

@app.route("/insert_user", methods=['POST', 'GET'])
def insert_view():
    return render_template("insert.html")

@app.route("/show_users", methods=['GET'])
def show_view():
    return render_template("show.html")

@app.route("/login", methods=['POST', 'GET'])
def login_view():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()
