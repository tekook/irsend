from flask import Flask, redirect, url_for, render_template, flash
import os, re, subprocess
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
reg_name = re.compile('^[a-zA-Z0-9\-]+$')
reg_key = re.compile('^KEY_[A-Z0-9]+$')



@app.route("/")
def welcome():
	return render_template('welcome.html')
@app.route("/lk/on")
def lichton():
	os.system("irsend SEND_ONCE lichterkette KEY_POWER")
	return redirect(url_for('welcome'))

@app.route("/lk/off")
def lichtoff():
	os.system("irsend SEND_ONCE lichterkette KEY_POWER2")
	return redirect(url_for('welcome'))


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

