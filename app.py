from flask import Flask, render_template, request
from datetime import date
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	r = requests.get('https://api.github.com/rate_limit')
	data = r.json()
	# Get limit of requests
	limit = data['resources']['core']['remaining']
	

	if request.method == 'POST':
		if (limit == 0):
			error = "Se ha llegado al limite de peticiones a GitHub, intentalo más tarde."
			return render_template('index.html', error=error)
		else:
			username = request.form['usrname']
			r = requests.get(f'https://api.github.com/users/{username}')
			data = r.json()
			# Get account old time
			today = date.today()
			actual_year = int(today.strftime("%Y"))
			how_old_account = data['created_at']
			how_old_account = how_old_account[0:4]
			how_old_account = int(how_old_account)
			how_old_account = actual_year - how_old_account
			# Get repos information
			r = requests.get(f'http://api.github.com/users/{username}/repos')
			repos = r.json()
			repos_count = len(repos)
			
			return render_template('user.html', data=data, how_old_account=how_old_account, repos=repos, repos_count=repos_count)
	else:
		return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=True)