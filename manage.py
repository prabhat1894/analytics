from app import db
from app.models import Release, Build, Component, Performance, TestCase, Users


# Drop all
db.drop_all()
# Create db
print "Creating database tables"
db.create_all()

print "Adding releases.." 
db.session.add(Release('4.1.1'))
db.session.add(Release('4.1.2'))
db.session.add(Release('4.1.3'))
db.session.add(Release('4.1.4'))


print "Adding components.."
db.session.add(Component('NS'))
db.session.add(Component('ND'))
db.session.add(Component('NC'))


print "Adding build version.."
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

print "adding users.."
db.session.add(Users("admin", "admin", "admin", "true"))
db.session.add(Users("regression", "regression", "standard", "false"))

print "Saving to database"
db.session.commit()
