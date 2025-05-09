from flask import Flask, render_template, jsonify, request, make_response, redirect
import src.database.databaseoperations as dbops
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/auth/register", methods=["POST"])
def api_auth_register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"error": "Username or Password is not found in request"}), 400
    
    result = dbops.addUser(username=username, password=password, is_admin=0)
    if result[0] == True:
        return jsonify(result)
    else:
        return jsonify(result), 400
    
@app.route("/api/auth/login", methods=["POST"])
def api_auth_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"error": "Username or Password is not found in request"}), 400
    
    result = dbops.checkPassword(username=username, password=password)
    if result[0] == True:
        return jsonify({"success": True, "message": "Login successful", "username": username})
    else:
        return jsonify({"success": False, "message": result[1]}), 400
    
@app.route("/api/auth/getcookie", methods=["POST"])
def api_auth_getcookie():
    data = request.get_json()  # Use .get_json() to parse JSON body
    username = data.get("username")
    return jsonify({"usercookie": username})

@app.route("/explore")
def explore():
    return render_template("TODO.html")

@app.route("/auth/login", methods=["GET"])
def auth_login():
    return render_template("login.html")

@app.route("/auth/signup", methods=["GET"])
def auth_register():
    return render_template("register.html")

if __name__ == "__main__":
    dbops.createTables()
    dbops.addUser("admin", "admin", True) # Creates default user, you should change the password asap
    app.run(debug=True)
