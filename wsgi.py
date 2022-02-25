from flask import Flask, redirect, url_for, render_template, flash
import os, re, subprocess
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
reg_name = re.compile('^[a-zA-Z0-9\-]+$')
reg_key = re.compile('^KEY_[A-Z0-9]+$')
reg_state = re.compile('^OFF$|^ON$')
states = {'lichterkette': {'state' : 'OFF', "ON": "KEY_POWER", "OFF": "KEY_POWER2"}}


@app.route("/")
def welcome():
	return render_template('welcome.html')

@app.route("/state/<name>")
def getState(name):
	if(reg_name.match(name)) and states[name]:
		return {"state": states[name]["state"]}
	else:
		return "Not found", 404


@app.route("/state/<name>/<state>")
def setState(name:str, state: str):
	if(reg_name.match(name) and states[name] and reg_state.match(state)):
		subprocess.run(["irsend", "SEND_ONCE", name, states[name][state]])
		states[name]["state"] = state
		return {"state": states[name]["state"]}
	else:
		return "Not found", 404


@app.route("/ir/<string:name>/<string:key>")
def dynIR(name, key):
	if reg_name.match(name) and reg_key.match(key):
		subprocess.run(["irsend", "SEND_ONCE", name, key])
		flash(f"Send {key} to {name}.", "success")
		return redirect(url_for('welcome'))
	else:
		return "Forbidden", 403



if __name__ == "__main__":
	app.run()

