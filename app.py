from flask import Flask, render_template, jsonify, request
import src.database.databaseoperations as dbops
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/auth/register", methods=["POST"])
def api_auth_register():
    data = request.get_json()
    print(data)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username or Password is not found in request"}), 400
    
    result = dbops.addUser(username=username, password=password, is_admin=0)
    return jsonify(result)

@app.route("/explore")
def explore():
    return render_template("TODO.html")

if __name__ == "__main__":
    dbops.createTables()
    dbops.addUser("admin", "admin", True) # Creates default user, you should change the password asap
    app.run(debug=True)
