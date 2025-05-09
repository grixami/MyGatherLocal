from flask import Flask, render_template, json
import src.database.databaseoperations as dbops
app = Flask(__name__)

if __name__ == "__main__":
    dbops.createTables()
    dbops.addUser("admin", "admin", True)
    app.run(debug=True)
