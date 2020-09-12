from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# domain.tk


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///moviesntv.db"

db.create_all()	

class moviesntv(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	ismovie = db.Column(db.Boolean, nullable=False)
	iswatched = db.Column(db.Boolean, nullable=False, default=False)

	def __repr__(self):
		return "movie or show " + str(self.id)


@app.route("/")
@app.route("/towatch", methods=['get', 'POST'])
def index():
	titles = moviesntv.query.all()
	return render_template("towatch.html", titles=titles)


@app.route("/add/<bool_>", methods=['GET', 'POST'])
def add(bool_):
	if request.method == "POST":
		title = request.form['title'].title()
		if str(bool_) == "movie":
			new_title = moviesntv(title=title, ismovie=True, iswatched=False)
		elif str(bool_) == "show":
			new_title = moviesntv(title=title, ismovie=False, iswatched=False)
		db.session.add(new_title)
		db.session.commit()
		return redirect('/towatch')


@app.route("/add/watched/<bool_>", methods=['GET', "POST"])
def addwatched(bool_):
	if request.method == "POST":
		title = request.form['title'].title()
		if str(bool_) == "movie":
			new_title = moviesntv(title=title, ismovie=True, iswatched=True)
		elif str(bool_) == "show":
			new_title = moviesntv(title=title, ismovie=False, iswatched=True)
		db.session.add(new_title)
		db.session.commit()
		return redirect('/watched')


@app.route("/watched")
def watched():
	titles = moviesntv.query.all()
	return render_template("watched.html", titles=titles)


@app.route("/towatch/delete/<int:id>")
def delete(id):
	title = moviesntv.query.get_or_404(id)
	position = title.iswatched
	db.session.delete(title)
	db.session.commit()
	if position:
		return redirect("/watched")
	return redirect("/towatch")


@app.route("/towatch/finised/<int:id>")
def watch(id):
	title = moviesntv.query.get_or_404(id)
	title.iswatched = True
	db.session.commit()
	return redirect("/towatch")


@app.route("/search", methods=['GET', "POST"])
def search():
	if request.method == "POST":
		tag = request.form['title'].title()
		tag = "%{}%".format(tag)
		names = moviesntv.query.filter(moviesntv.title.like(tag)).all()
		return render_template("search.html", names=names)
	else:
		return render_template("search.html", names="")
# ADD EDIT


if __name__ == "__main__":
	app.run(debug=True)