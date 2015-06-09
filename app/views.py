from flask import render_template, flash, session, url_for, request, g
from app import app
from app.util import validate, isLoggedIn, redirectTo, getConnection

import sqlite3

@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    if not isLoggedIn():
        return redirectTo('login')

    return render_template('index.html', page="home")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html') ,404


@app.route("/about")
def about():
    return render_template('about.html', page="about")

@app.route('/results/<rel>')
@app.route('/results/<rel>/<ver>')
@app.route('/results/<rel>/status/<flag>')
@app.route('/results/<rel>/<ver>/status/<flag>')
@app.route('/results/<rel>/comp/<component>')
@app.route('/results/<rel>/<ver>/comp/<component>')
@app.route('/results/<rel>/comp/<component>/status/<flag>')
def show_results_per_rel_ver(rel=None, ver=None, flag=None, component=None):
    if not isLoggedIn():
        return redirectTo('login')

    con = getConnection()
    cursor = con.cursor()
    total, failed, passed = 0,0,0
    if rel and ver and not flag and not component:
        data = cursor.execute("SELECT * FROM regression where release=? and version = ?",(rel,ver))
        rows = con.execute("SELECT count(*) from regression where release=? and version=?",(rel,ver))
        for row in rows:
            total = row[0]
        rows = con.execute("SELECT count(*) from regression where release=? and version = ? and status='FAIL'",(rel,ver))
        for row in rows:
            failed = row[0]
        rows = con.execute("SELECT count(*) from regression where release=? and version = ? and status='PASS'",(rel,ver))
        for row in rows:
            passed = row[0]

    if rel and not ver and not flag:
        data = cursor.execute("SELECT * FROM regression where release=?",(rel,))
        rows = con.execute("SELECT count(*) from regression where release=?",(rel,))
        for row in rows:
            total = row[0]
        rows = con.execute("SELECT count(*) from regression where release=? and status='FAIL'",(rel,))
        for row in rows:
            failed = row[0]
        rows = con.execute("SELECT count(*) from regression where release=? and status='PASS'",(rel,))
        for row in rows:
            passed = row[0]
    if rel and ver and flag:
        data = cursor.execute("SELECT * FROM regression where release=? and version=? and status=?",(rel, ver,flag.upper()))
        rows = con.execute("SELECT count(*) from regression where release=? and version = ?",(rel,ver))
        for row in rows:
            total = row[0]
        rows = con.execute("SELECT count(*) from regression where release=? and version = ? and status='FAIL'",(rel,ver))
        for row in rows:
            failed = row[0]
        rows = con.execute("SELECT count(*) from regression where release=? and version = ? and status='PASS'",(rel,ver))
        for row in rows:
            passed = row[0]
    if rel and not ver and flag:
        data = cursor.execute("SELECT * FROM regression where release=? and status=?",(rel,flag.upper()))
    if rel and component:
        data = cursor.execute("SELECT * FROM regression where release=? and component=?", (rel, component))
    if rel and component and ver:
        data = cursor.execute("SELECT * FROM regression where release=? and version = ? and component=?", (rel,ver, component))

    if rel and component and flag:
        data = cursor.execute("SELECT * FROM regression where release=? and status = ? and component=?", (rel,flag.upper(), component))

    summary = dict(total=total, failed=failed, passed=passed)

    results = [dict(r=row[0], v=row[1],c=row[2], id=row[3], tr=row[4], status=row[5], desc=row[6]) for row in data.fetchall()]
    cursor.close()
    con.close()
    return render_template('results.html', results=results, summary=summary)

@app.route('/reports/')
def reports():
    if not isLoggedIn():
        return redirectTo('login')

    con = getConnection()
    cursor = con.cursor()

    data = cursor.execute("SELECT release, version,component, status, count(status) FROM regression group by status, release, version, component order by release")
    results = [dict(r=row[0], v=row[1],c=row[2],s=row[3], count=row[4]) for row in data.fetchall()]
    cursor.close()
    con.close()
    return render_template('reports.html', results=results, page="reports")

@app.route('/reports/executive')
def view():
    if not isLoggedIn():
        return redirectTo('login')

    con = getConnection()
    cursor = con.cursor()

    data = con.execute("SELECT release, component FROM regression group by release,component order by release")

    rows = con.execute("SELECT release, component, count(status) FROM regression where status='PASS' group by release,component order by release")
    passed=[dict(r=row[0], c=row[1], count=row[2]) for row in rows]

    rows = con.execute("SELECT release, component, count(status) FROM regression group by release,component  order by release")

    total=[dict(r=row[0], c=row[1], count=row[2]) for row in rows]

    results = [dict(r=row[0], c=row[1]) for row in data.fetchall()]
    cursor.close()
    con.close()
    return render_template('view.html', results=results, page="view", passed=passed, total=total)

@app.route('/account/login')
def login():
    return render_template('login.html')

@app.route('/account/controller', methods=['GET', 'POST'])
def controller():
    if request.method != "POST":
        return redirecTo(('login'))

    username = request.form['username']
    password = request.form['password']

    if not validate(username, password):
        flash('Invalid username or password')
        return redirectTo('login')

    session['logged_in'] = True
    return (redirectTo('view'))

@app.route('/account/logout')
def logout():
    session.clear()
    flash("You've been logged out")
    return render_template('login.html', success=True)

