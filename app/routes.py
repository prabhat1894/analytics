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
from app.queries import (
        get_results, 
        get_results_by_build, 
        get_performance_data, 
        get_products, 
        get_categories,
        get_releases,
        get_builds,
        get_navbar_data,
        get_graph_data,
        get_tabular_failure_report)

@app.route("/")
@loginRequired
def home():
    #return render_template('index.html', page="home")
    return show_dashboard()


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

    if not validate(username, password):
        flash('Invalid username or password')
        return redirectTo('login')

    session['logged_in'] = True
    session['username'] = username 
    return redirectTo('show_dashboard')

@app.route('/account/update', methods=['GET','POST'])
@loginRequired
def update():
    oldpasswd = request.form['oldpasswd']
    newpasswd = request.form['newpasswd']
    flash("Updating password for %s" %(session['username']))
    return  redirectTo('show_dashboard')

@app.route('/account/logout')
@loginRequired
def logout():
    '''Logouts and clears all session variables'''
    session.clear()
    flash("You've been logged out")
    
    return render_template('login.html', success=True)


@app.route('/reports/v1/executive')
def show_executive_report():
    categories, json_data = get_navbar_data()
    category_smoke_pass = get_results('smoke', 'pass').all()
    category_smoke_total = get_results('smoke').all()
    category_reg_pass = get_results('regression', 'pass').all()
    category_reg_total = get_results('regression' ).all()
    smoke = []
    regression = []
    fmt = "%-15s %-10s %-18s %10s %10s %10s"
    header = fmt % ("Category", "Release", "Component","Total", "Passed", "Failed")
    print "Smoke results"
    print "-" * 79
    print header 
    for (x, y) in zip(category_smoke_pass, category_smoke_total):
        category, release, component, passed = x
        category, release, component, total = y
        failed = total - passed
        
        print fmt % (category, release, component, total, passed, failed)
        smoke.append(dict(category=category, 
                          release=release, 
                          component=component, 
                          total=total, 
                          passed=passed, 
                          failed=failed))
    
    print "-" * 79
    print "Regression results"
    print "-" * 79
    print header

    for (x, y) in zip(category_reg_pass, category_reg_total):
        category, release, component, passed = x
        category, release, component, total = y
        failed = total - passed 
        
        print fmt % (category, release, component, total, passed, failed)
        regression.append(dict(category=category, 
                               release=release, 
                               component=component, 
                               total=total, 
                               passed=passed, 
                               failed=failed))
    
    print "-" * 79
    smoke_last_five_total = get_results_by_build(category="smoke", release="4.1.2").limit(5)
    smoke_last_five_pass = get_results_by_build(category="smoke", release="4.1.2", status="pass").limit(5)

    smoke_results = []
    print "%10s %10s %10s %10s" % ("Build", "Total", "Passed" , "Failed")
    for dataset_total, dataset_pass in zip(smoke_last_five_total, smoke_last_five_pass):
        build_name, total = dataset_total
        build_name, passed = dataset_pass

        failed = total - passed
        print "%10s %10s %10s %10s" % (build_name, total, passed, failed)

    return render_template('executive.html', categories=categories,
                            smoke=smoke, regression=regression,
                            json_data=json_data) 


@app.route('/reports/dashboard')
@loginRequired
def show_dashboard():
    categories, json_data = get_navbar_data()
    results = get_performance_data(release="4.1.2").limit(5)
    cps = []
    hps = []
    throughput = []
    build = []
    for row in results:
         build_name, perf = row
         build.append(dict(name=build_name))
         cps.append(dict(cps=perf.cps))
         hps.append(dict(hps=perf.hps))
         throughput.append(dict(throughput=perf.throughput))
    smoke_last_five_total = get_results_by_build(category="smoke", release="4.1.2").limit(5)
    smoke_last_five_pass = get_results_by_build(category="smoke", release="4.1.2", status="pass").limit(5)

    smoke_results = []
    for dataset_total, dataset_pass in zip(smoke_last_five_total, smoke_last_five_pass):
        build_name, total = dataset_total
        build_name, passed = dataset_pass
        failed = total - passed
        smoke_results.append(dict(name=build_name, total=total, passed=passed, failed=failed))

    reg_last_five_total = get_results_by_build(category="regression", release="4.1.2").limit(5) 
    reg_last_five_pass = get_results_by_build(category="regression", release="4.1.2", status="pass").limit(5)
    reg_results = []
    for dataset_total, dataset_pass in zip(reg_last_five_total, reg_last_five_pass):
        build_name, total = dataset_total
        build_name, passed = dataset_pass
        failed = total - passed
        reg_results.append(dict(name=build_name, total=total, passed=passed, failed=failed))

    return render_template('dashboard.html',
            build=build, cps=cps, hps=hps, 
            throughput=throughput, categories=categories, 
            json_data=json_data,
            smoke_results=smoke_results,
            reg_results=reg_results)


@app.route('/reports/graphs/<product>')
@app.route('/reports/graphs/<product>/<category>')
@app.route('/reports/graphs/<product>/<category>/<release>')
@app.route('/reports/graphs/<product>/<category>/<release>/<build>')
@loginRequired
def show_graphs(product=None, category=None, release=None, build=None):
    label = ""
    breadcrumb = "Filter> "
    result = []
    if product is not None and category is None and release is None and build is None:
        # only product flag
        total = get_graph_data(product=product)
        passed = get_graph_data(product=product, status='pass')
        label += "Overall {} tests report".format(product)
        breadcrumb += "Product: {}".format(product)
        result = get_tabular_failure_report(component=product)

    elif product is not None and category is not None and release is None and build is None:
        total = get_graph_data(product=product, category=category)
        passed = get_graph_data(product=product, category=category, status='pass')
        label += "{} {} tests report".format(product, category)
        breadcrumb += "Product: {}, category: {}".format(product, category)
        result = get_tabular_failure_report(component=product, category=category)
        # product and category flag
    elif product is not None and category is not None and release is not None and build is None:
        # Product category and release flag
        total = get_graph_data(product=product, category=category, release=release)
        passed = get_graph_data(product=product, category=category, release=release, status='pass')
        label += "{} {} tests report for {}".format(product, category, release)
        breadcrumb += "Product: {}, category: {}, release: {}".format(product, category, release)
        result = get_tabular_failure_report(component=product, category=category, release=release)
    elif product is not None and category is not None and release is not None and build is not None:
        # Product, category, release and build
        total = get_graph_data(product=product, category=category, release=release, build=build)
        passed = get_graph_data(product=product, category=category, release=release, build=build, status='pass')
        label += "{} {} tests report for release: {} and build: {}".format(product, category, release, build)
        breadcrumb += "Product: {}, Rategory: {}, Release: {}, Build: {}".format(product, category, release, build)
        result = get_tabular_failure_report(component=product, category=category, release=release, build=build)
    else:
        return "Invalid path"

    failed = total - passed 
    categories, json_data = get_navbar_data()
    print result
    return render_template('single_graph.html', categories=categories, json_data=json_data, total=total, passed=passed, 
            failed=failed, label=label, breadcrumb=breadcrumb, tabledata=result)
