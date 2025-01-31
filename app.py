from flask import Flask
from flask_shell_ipython import Shell
 
app = Flask(__name__)
app.config["SHELL_PLUS"] = True
shell = Shell(app)
 
@app.route("/")
def home():
    return "Python Console Running! Go to /shell"
