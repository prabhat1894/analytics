from app import db


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<{}-{}>".format(self.id, self.name)


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<{}-{}>".format(self.id, self.name)
    

class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<{}-{}>".format(self.id, self.name)

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    releaseid = db.Column(db.Integer, db.ForeignKey(Release.id))
    componentid = db.Column(db.Integer, db.ForeignKey(Component.id))
    buildid = db.Column(db.Integer, db.ForeignKey(Component.id))
    hps = db.Column(db.Integer) 
    cps = db.Column(db.Integer) 
    throughput = db.Column(db.Integer)

    def __init__(self, releaseid, buildid, componentid, hps, cps, throughput):
        self.releaseid = releaseid
        self.buildid = buildid 
        self.componentid = componentid
        self.hps = hps
        self.cps = cps
        self.throughput = throughput

    def __repr__(self):
        return "<{} - {} - {}>".format(self.hps, self.cps, self.throughput)

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    releaseid = db.Column(db.Integer, db.ForeignKey(Release.id))
    buildid = db.Column(db.Integer, db.ForeignKey(Component.id))
    componentid = db.Column(db.Integer, db.ForeignKey(Component.id))
    status = db.Column(db.String(4))
    description = db.Column(db.String(128))

    def __init__(self, name, releaseid, buildid, componentid, status, description):
       self.name = name 
       self.releaseid = releaseid
       self.buildid = buildid
       self.componentid = componentid
       self.status = status
       self.description = description

    def __repr__(self):
        return "<{} - {}>".format(self.name, self.status)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(16))
    privilege = db.Column(db.String, default="standard")
    active = db.Column(db.String, default="false")

    def __init__(self, username, password, privilege, active):
        self.username = username 
        self.password = password
        self.privilege = privilege
        self.active = active 

    def __repr__(self):
        return "<{} is a {} user and is currently {}>".format(self.username, self.privilege, self.active)

