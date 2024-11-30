from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')

def index():
   return render_template("home.html", data = "")


@app.route('/login')
def login():
   return render_template("login.html", data = "")

@app.route('/signup')

def signup():
   return render_template("signup.html", data = "")

@app.route('/about')

def about():
   return render_template("about.html", data = "")

@app.route('/mood')
def mood():
   return render_template("mood.html", data = "")

if __name__=='__main__':
   app.run(debug=True, host='0.0.0.0', port=8000)