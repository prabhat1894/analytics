from app import db
from app.models import (Component, 
    TestCase, 
    Build, 
    Category, 
    Release, 
    Users, 
    Performance
)


def get_results(category, status=None):
    # select category.name, release.name, component.name, count(testcase.status) 
    # from component, release, category, testcase where testcase.releaseid=release.id 
    # and testcase.categoryid=category.id and category.name='regression' 
    # and testcase.status='pass' and testcase.componentid=component.id 
    # group by release.name,component.name;

    q = db.session.query(Category.name.label('category'), 
            Release.name.label('release'), 
            Component.name.label('component'), 
            db.func.count(TestCase.status.label('count')))
    
    q = q.filter(TestCase.categoryid==Category.id).\
          filter(TestCase.releaseid==Release.id).\
          filter(TestCase.componentid==Component.id).\
          filter(Category.name==category)

    if status is not None:
        q = q.filter(TestCase.status==status)

    q = q.group_by(Release.name).group_by(Component.name)
    q = q.order_by(Release.name.desc())
    return q

def get_results_by_build(category, release=None, status=None, orderby_flag=True):
    q = db.session.query(Build.name, db.func.count(TestCase.status.label("count")))
    q = q.filter(TestCase.categoryid==Category.id).\
          filter(TestCase.releaseid==Release.id).\
          filter(TestCase.buildid==Build.id)
          
    if category is not None:
        q = q.filter(Category.name==category)
    if release is not None:
        q = q.filter(Release.name==release)
    if status is not None:
        q = q.filter(TestCase.status==status)

    q = q.group_by(Build.name)
    if orderby_flag:
        q = q.order_by(Build.name.desc())
    return q

def get_performance_data(release=None, order_by=True):
    q = db.session.query(Build.name, Performance)
    q = q.filter(Performance.releaseid==Release.id).\
            filter(Performance.buildid==Build.id).\
            filter(Performance.componentid==Component.id).\
            filter(Component.name=='NetStorm')
    if release is not None:
        q = q.filter(Release.name==release)

    q = q.group_by(Build.name)
    if order_by:
        q = q.order_by(Build.name.desc())

    return q

def get_products():
    q = db.session.query(Component).filter(TestCase.componentid==Component.id).all()
    return q

def get_categories():
    q = db.session.query(Category).all()
    return q

def get_releases(product=None):
    q = db.session.query(Release).filter(TestCase.releaseid==Release.id)
    if product is not None:
        q = q.filter(Release.name==product)
    q = q.order_by(Release.name.desc()).all()
    return q

def get_builds(release=None, limit=5, product=None):
    q = db.session.query(Build).filter(TestCase.buildid==Build.id)
    if release is not None:
        q = q.filter(Release.name==release).filter(TestCase.releaseid==Release.id)
    if product is not None:
        q = q.filter(TestCase.componentid==Component.id).filter(Component.name==product)
    q = q.order_by(Build.name.desc()).limit(limit)
    return q
    
def get_navbar_data():
    products = [ product.name for product in get_products() ]
    categories = [ category.name.capitalize() for category in get_categories()] 

    releases = [ release.name for release in get_releases()]

    builds = []
    json_data = {}
    for product in products:
        release_list = []
        for release in releases:
            builds = [build.name for build in get_builds(release, product=product)]
            release_list.append({
                release: builds
            })
        json_data[product] = release_list
    
    return (categories, json_data)

def get_graph_data(product=None, category=None, release=None, build=None, status=None):
    q = db.session.query(db.func.count(TestCase.status))
    q = q.filter(TestCase.releaseid==Release.id).\
            filter(TestCase.categoryid==Category.id).\
            filter(TestCase.buildid==Build.id).\
            filter(TestCase.componentid==Component.id)

    if product is not None and category is None and release is None and build is None:
        q = q.filter(Component.name==product)
    if product is not None and category is not None and release is None and build is None:
        q = q.filter(Component.name==product).\
                filter(Category.name==category.lower())
    if product is not None and category is not None and release is not None and build is None:
        q = q.filter(Component.name==product).\
                filter(Category.name==category.lower()).\
                filter(Release.name==release)
    if product is not None and category is not None and release is not None and build is not None:
        q = q.filter(Component.name==product).\
                filter(Category.name==category.lower()).\
                filter(Release.name==release).\
                filter(Build.name==build)
    if status is not None:
        q = q.filter(TestCase.status==status.lower())

    return q.one()[0]


def get_tabular_failure_report(component=None, category=None, release=None, build=None):
    q = db.session.query(Component.name, Release.name, Build.name, Category.name, TestCase.status, TestCase.description)
    q = q.filter(TestCase.categoryid==Category.id).\
            filter(TestCase.releaseid==Release.id).\
            filter(TestCase.buildid==Build.id).\
            filter(TestCase.componentid==Component.id)

    if component is not None and category is None and release is None and build is None:
        q = q.filter(Component.name==component)
    if component is not None and category is not None and release is None and build is None:
        q = q.filter(Component.name==component).\
              filter(Category.name==category.lower())
    if component is not None and category is not None and release is not None and build is None:
        q = q.filter(Component.name==component).\
              filter(Category.name==category.lower()).\
              filter(Release.name==release)
    if component is not None and category is not None and release is not None and build is not None:
        q = q.filter(Component.name==component).\
              filter(Category.name==category.lower()).\
              filter(Release.name==release).\
              filter(Build.name==build)

    q = q.filter(TestCase.status=='fail') 
    result  = [dict(product=row[0], release=row[1], build=row[2], category=row[3], status=row[4].upper(), desc=row[5]) for row in q.all()]
    return result 




