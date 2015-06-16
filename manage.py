from flask.ext.script import Manager, Shell, Server
from app import app
from app import db
from app.models import Release, Build, Component, TestCase, Performance, Users, Category

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell())


@manager.command
def syncdb():
    '''Syncs db. drops and creates all tables'''
    print "Syncing db tables..."
    db.drop_all()
    db.create_all()
    print "Adding release information" 
    db.session.add(Release('4.1.1'))
    db.session.add(Release('4.1.2'))
    db.session.add(Release('4.1.3'))
    db.session.add(Release('4.1.4'))


    print "adding categories"
    db.session.add(Category('smoke'))
    db.session.add(Category('regression'))

    print "Adding components"
    db.session.add(Component('NetStorm'))
    db.session.add(Component('NetDiagnostics'))
    db.session.add(Component('NetCloud'))


    print "Adding build version"
    db.session.add(Build('B1'))
    db.session.add(Build('B2'))
    db.session.add(Build('B3'))
    db.session.add(Build('B4'))
    db.session.add(Build('B5'))
    db.session.add(Build('B6'))
    db.session.add(Build('B7'))
    db.session.add(Build('B8'))
    db.session.add(Build('B9'))
    db.session.add(Build('B10'))

    print "Creating users"
    db.session.add(Users("admin", "admin", "admin", "true"))
    db.session.add(Users("regression", "regression", "standard", "false"))

    db.session.add(TestCase('REG-001-001', 1, 1, 1, 2, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 1, 1, 2, 'pass', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 1, 1, 2, 'pass', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 1, 1, 2, 2, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 1, 2, 2, 'fail', 'No backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 1, 2, 2, 'pass', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 1, 2, 1, 2, 'fail', 'No business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 1, 2, 'pass', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 1, 2, 'pass', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 1, 2, 2, 2, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 2, 2, 'pass', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 2, 2, 'pass', 'Discovered db queries'))
    
    db.session.add(TestCase('REG-001-001', 2, 1, 2, 2, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 2, 1, 2, 2, 'fail', 'No backends detected'))
    db.session.add(TestCase('REG-001-003', 2, 1, 2, 2, 'pass', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 2, 2, 1, 2, 'fail', 'No business transactions working'))
    db.session.add(TestCase('REG-001-002', 2, 2, 1, 2, 'pass', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 2, 2, 1, 2, 'pass', 'Discovered db queries'))
   
    # regression netstorm
    db.session.add(TestCase('REG-001-001', 2, 1, 2, 1, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 2, 1, 2, 1, 'fail', 'No backends detected'))
    db.session.add(TestCase('REG-001-003', 2, 1, 2, 1, 'fail', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 2, 2, 1, 1, 'fail', 'No business transactions working'))
    db.session.add(TestCase('REG-001-002', 2, 2, 1, 1, 'fail', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 2, 2, 1, 1, 'fail', 'Discovered db queries'))
  
    # smoke netstorm
    db.session.add(TestCase('REG-001-001', 1, 1, 2, 1, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 1, 2, 1, 'pass', 'No backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 1, 2, 1, 'pass', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 1, 2, 1, 1, 'pass', 'No business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 1, 1, 'pass', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 1, 1, 'pass', 'Discovered db queries'))
    
    db.session.add(TestCase('REG-001-001', 1, 2, 3, 1, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 3, 1, 'fail', 'No backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 3, 1, 'fail', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 1, 2, 4, 1, 'pass', 'No business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 4, 1, 'fail', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 4, 1, 'pass', 'Discovered db queries'))
    
    db.session.add(TestCase('REG-001-001', 1, 2, 4, 1, 'pass', 'All business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 4, 1, 'fail', 'No backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 5, 1, 'fail', 'Discovered db queries'))
    db.session.add(TestCase('REG-001-001', 1, 2, 5, 1, 'pass', 'No business transactions working'))
    db.session.add(TestCase('REG-001-002', 1, 2, 6, 1, 'fail', 'All backends detected'))
    db.session.add(TestCase('REG-001-003', 1, 2, 6, 1, 'pass', 'Discovered db queries'))
  
    #Performance data
    db.session.add(Performance(2, 1, 1, 1000, 550, 930))
    db.session.add(Performance(2, 2, 1, 900, 560, 950))
    db.session.add(Performance(2, 3, 1, 980, 570, 940))
    db.session.add(Performance(2, 4, 1, 930, 520, 940))
    db.session.add(Performance(2, 5, 1, 890, 530, 960))
    db.session.add(Performance(2, 6, 1, 950, 560, 930))
    print "Saving to database"
    db.session.commit()

@manager.command
def debug():
    '''starts the server in debug mode'''
    app.run(debug=True, host="0.0.0.0")

manager.run()

