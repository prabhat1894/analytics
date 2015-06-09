from flask import (
        g,
        flash,
        session,
        url_for,
        request,
        render_template
)

from app.util import (
        count,
        validate,
        isLoggedIn,
        redirectTo,
        getConnection,
        loginRequired,
        authenticate
)

import sqlite3
from app import app
from datetime import timedelta 
import config 

@app.route("/")
@app.route("/index")
@app.route("/home")
@loginRequired
def home():
    return render_template('index.html', page="home")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html') ,404

@app.before_request
def persist():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=config.SESSION_TIMEOUT)

@app.route("/about")
def about():
    return render_template('about.html', page="about")

@app.route("/help")
def help():
    return render_template('help.html')

@app.route('/results/<rel>')
@app.route('/results/<rel>/<ver>')
@app.route('/results/<rel>/status/<flag>')
@app.route('/results/<rel>/<ver>/status/<flag>')
@app.route('/results/<rel>/comp/<component>')
@app.route('/results/<rel>/<ver>/comp/<component>')
@app.route('/results/<rel>/comp/<component>/status/<flag>')
@loginRequired
def show_results_per_rel_ver(rel=None, ver=None, flag=None, component=None):

    con = getConnection()
    cursor = con.cursor()
    total, failed, passed = 0,0,0
    if rel and ver and not flag and not component:
        data = cursor.execute("""SELECT * FROM regression  
                WHERE release = ?  
                AND version = ?""" 
                ,(rel,ver))

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND version=?"""
                ,(rel,ver))
        total = count(rows)

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND version = ? 
                AND status='FAIL'"""
                ,(rel,ver))
        failed = count(rows)

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND version = ? 
                AND status='PASS'"""
                ,(rel,ver))
        passed = count(rows)

    if rel and not ver and not flag:
        data = cursor.execute("""SELECT * 
                FROM regression 
                WHERE release = ? 
                ORDER BY version DESC""",(rel,))

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ?""",(rel,))
        total = count(rows)

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND status = 'FAIL'"""
                ,(rel,))
        failed = count(rows)

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND status = 'PASS'"""
                ,(rel,))
        passed = count(rows)

    if rel and ver and flag:
        data = cursor.execute("""SELECT * 
                FROM regression 
                WHERE release = ? 
                AND version = ? 
                AND status = ?
                ORDER BY release,version DESC"""
                ,(rel, ver,flag.upper()))

        rows = con.execute("""SELECT count(*) 
                FROM regression
                WHERE release = ? 
                AND version = ?
                ORDER BY release,version DESC"""
                ,(rel,ver))

        total = count(rows)
        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND version = ? 
                AND status = 'FAIL'
                ORDER BY release,version DESC"""
                ,(rel,ver))
        failed = count(rows)

        rows = con.execute("""SELECT count(*) 
                FROM regression 
                WHERE release = ? 
                AND version = ? 
                AND status = 'PASS'
                ORDER BY release,version DESC""",(rel,ver))
        passed = count(rows)


    if rel and not ver and flag:
        data = cursor.execute("""SELECT * 
                FROM regression 
                WHERE release = ? 
                AND status = ?
                ORDER BY release,version DESC""",(rel,flag.upper()))

    if rel and component:
        data = cursor.execute("""SELECT * 
                FROM regression 
                WHERE release = ? 
                AND component = ?
                ORDER BY release,version DESC""", (rel, component))
    
    if rel and component and ver:
        data = cursor.execute("""SELECT * 
                FROM regression 
                WHERE release = ? 
                AND version = ? 
                AND component = ?
                ORDER BY release,version DESC""", (rel,ver, component))

    if rel and component and flag:
        data = cursor.execute("""SELECT * 
                FROM regression 
                WHERE release = ? 
                AND status = ? 
                AND component = ? 
                ORDER BY release,version DESC""", (rel,flag.upper(), component))

    summary = dict(total=total, failed=failed, passed=passed)
    results = [dict(r=row[0], v=row[1], 
        c=row[2], id=row[3], 
        tr=row[4], status=row[5], 
        desc=row[6]) for row in data.fetchall()]

    cursor.close()
    con.close()
    
    return render_template('results.html', results=results, summary=summary)

@app.route('/reports/')
@loginRequired
def reports():

    con = getConnection()
    cursor = con.cursor()
    data = cursor.execute("""SELECT release, version,
            component, status, count(status) 
            FROM regression 
            GROUP BY status, 
            release, 
            version, 
            component 
            ORDER BY release, version DESC""")
    
    results = [dict(r=row[0], 
        v=row[1],
        c=row[2],
        s=row[3],
        count=row[4])
        for row in data.fetchall()]
    
    cursor.close()
    con.close()
    
    return render_template('reports.html', results=results, page="reports")

@app.route('/reports/executive')
@loginRequired
def view():
    con = getConnection()
    cursor = con.cursor()

    data = con.execute("""SELECT release, component 
            FROM regression 
            GROUP BY release, component 
            ORDER BY release DESC""")

    rows = con.execute("""SELECT release, component, count(status) 
            FROM regression 
            WHERE status='PASS' 
            GROUP BY release, component 
            ORDER BY release DESC""")
    
    passed=[dict(r=row[0], c=row[1], count=row[2]) for row in rows]

    rows = con.execute("""SELECT release, component, count(status) 
            FROM regression 
            GROUP BY release, component  
            ORDER BY release DESC""")

    total=[dict(r=row[0], c=row[1], count=row[2]) for row in rows]
    results = [dict(r=row[0], c=row[1]) for row in data.fetchall()]
    
    cursor.close()
    con.close()
    
    return render_template('view.html', results=results, 
            page="view", passed=passed, total=total)

@app.route('/account/login')
def login():
    return render_template('login.html')

@app.route('/account/controller', methods=['GET', 'POST'])
def controller():
    if request.method != "POST":
        return redirectTo('login')

    username = request.form['username']
    password = request.form['password']

    #if not validate(username, password):
    if not authenticate(username, password):
        flash('Invalid username or password')
        return redirectTo('login')

    session['logged_in'] = True
    session['username'] = username 
    return redirectTo('view')

@app.route('/account/update', methods=['GET','POST'])
@loginRequired
def update():
    oldpasswd = request.form['oldpasswd']
    newpasswd = request.form['newpasswd']
    flash("Updating password for %s" %(session['username']))
    return  redirectTo('view')

@app.route('/account/logout')
@loginRequired
def logout():
    '''Logouts and clears all session variables'''
    session.clear()
    flash("You've been logged out")
    
    return render_template('login.html', success=True)

