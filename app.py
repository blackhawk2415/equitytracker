from flask import Flask, render_template
import sqlite3
import os


dbPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'equityData.db'))

app = Flask(__name__) # pass in name to help determine route path
 
threeDayPull = """SELECT 
					ticker, 
					COALESCE(ROUND(price7,2),"na") as price,
					COALESCE(volume7,"na") as volume, 
					COALESCE(ROUND((price7-price4)/ABS(price4),2),"na") as PriceMomentum,
					COALESCE(ROUND((volume7-volume4)/ABS(volume4),2),"na") as VolumeMomentum,
					COALESCE(ROUND(ABS(((price7-price4)/ABS(price4)))+ABS(((volume7-volume4)/ABS(volume4)))/2,2),0) as Weight
				FROM TargetStocks ORDER BY Weight DESC LIMIT 100;"""



 #routing or mapping the process of connecting different pages to a python function

@app.route('/')  #the @ is a decorater, way to wrap up an existing python function and modify it's behavior
def index():
	conn = sqlite3.connect(dbPath)
	c = conn.cursor()
	dataItems = c.execute(threeDayPull)
	return render_template("index.html", items=dataItems.fetchall())


@app.route('/about')
def about():
	return "1300+ Equities: Criteria: 1) 100M < Market Cap < 910B, 2) 300k < volume < MAX, 3) 0% < Rev Growth < Max 4) 1 < Beta < MAX"

@app.route('/profile/<username>')
def profile(username):
	return "hello %s, development on this page is pending" % username


#add 404

# @app.after_request  # anti caching of static files
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r




if __name__ == '__main__':
	app.run(host='0.0.0.0')
