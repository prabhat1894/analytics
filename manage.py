#!/usr/bin/env python
'''
  For creating automation bench
  usage: python manage.py --project [projectname]
                          --testcase [testcasename]
                          --testsuite [suitename]
                          --create [flag for first time]
                          --delete [flag for first time]

  Example:
            python manage.py --project NDCore --create
            python manage.py --project NDCore --testcase Regression01
            python manage.py --project NDCore --testsuite regression
            python manage.py --project NDCore --delete
            python manage.py --project NDCore --target perf --add
            python manage.py --project NDCore --target regression
'''
import os
import sys
import stat
import shutil
import argparse

def xprint(level, msg):
    print "[%s] %s" %(level, msg)

BENCH_DIRS = [ 'scripts', 'scenarios',
             'lib', 'logs',
             'results', 'testcases',
             'testsuites'
]

FILES = [ 're_ts_run', 're_set_env', 'build.xml' ]

templ ='''<?xml version="1.0"?>
<project name="%s" default="%s">
    <!--Set properties here -->
    <property name="reg.shell" value="./re_ts_run"/>
    <property name="reg.init.shell" value="./re_set_env"/>
    <!-- End of property defination -->

    <!-- Target defination -->
    <target name="%s" depends="init-clean">
        <exec executable="${reg.shell}" taskname="info">
            <arg value="%s"/>
            <arg value="--nodebug"/>
            <arg value="--email"/>
            <arg value="true"/>
        </exec>
    </target>

    <target name="init">
        <exec executable="${reg.init.shell}" taskname="copy"/>
    </target>

    <target name="init-clean">
        <exec executable="${reg.init.shell}" taskname="init">
            <arg value="--clean" />
        </exec>
    </target>
</project>
'''

target_templ = '''    <target name="%s">
          <exec executable="${reg.shell}" taskname="info">
              <arg value="%s"/>
              <arg value="--nodebug"/>
              <arg value="--email"/>
              <arg value="true"/>
          </exec>
    </target>
</project>
'''
def create_dirs(p, d):
    for folder in d:
        try:
            os.makedirs("%s/%s" %(p, folder),0755)
        except OSError:
            pass

def create_files(p, f):
    for file in f:
        try:
            touch("%s/%s" %(p,file))
            if file in [ "re_set_env", "re_ts_run" ]:
                os.system("chmod +x %s/%s" %(p,file))
        except Exception, e:
            print e

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new',
            help='Create flag',
            required=False,
            action='store_true')

    parser.add_argument('-p', '--project',
            help='Project name',
            required=True)

    parser.add_argument('-c', '--testcase',
            help='The TestCase',
            required=False)

    parser.add_argument('-s', '--testsuite',
            help='Testsuite name',
            required=False)

    parser.add_argument('-t', '--target',
            help='The ant target',
            required=False)

    parser.add_argument('-r', '--remove',
            help='Delete project',
            required=False,
            action='store_true')

    parser.add_argument('-a', '--add',
            help='Add Target in build.xml',
            required=False,
            action='store_true')

    return parser


def create_testcase(project, testcase):
    p, t = project, testcase
    d = "%s/testcases/%s" %(p,t)

    files = ['iteration.spec', 'testcase.conf', 
             'pre_test_setup', 'post_test_setup', 
             'check_status'
    ]
    try:
        os.makedirs(d, 0755)
    except OSError: #Fails if directory exists. Need not to worry
        pass

    try:
        for f in files:
            executable = "%s/%s" %(d,f)
            touch(executable)

            if f in files[2:]:
                os.system('chmod +x %s' %(executable))
    except Exception,e:
        print e

def touch(f):
    open(f, 'a').close()

def create_testsuite(project, testsuite):
    s = "%s/testsuites/%s.conf" %(project, testsuite)
    touch(s)

def getOffset(f):
    offset = 0
    tag = "</project>"
    with open(f,'r') as handle:
        for line in handle:
            pass
        offset = handle.tell()
        offset = offset - len(tag) - 1

    return offset

def update_build(project, target, flag=False):
    buildFile = "%s/build.xml" %(project)
    if not flag:
        xprint("info", "Creating Skeleton and adding target '%s' to %s" %(target, buildFile))
        with open(buildFile, 'w') as f:
            f.write(templ %(project, target, target, target))
    else:
            offset = getOffset(buildFile)
            xprint("info", "Updating build.xml, adding target '%s'" %(target))
            with open(buildFile, 'r+') as f:
                f.seek(offset,0)
                f.write(target_templ %(target, target))

if __name__ == "__main__":
    parser = parse()
    opts = parser.parse_args()

    project     = opts.project
    testcase    = opts.testcase
    testsuite   = opts.testsuite
    createFlag  = opts.new
    deleteFlag  = opts.remove
    target      = opts.target
    addFlag     = opts.add

    if project and not createFlag and not testcase \
            and not testsuite and not deleteFlag \
            and not target and not addFlag:

        parser.print_help()
        sys.exit(255)
        pass

    if project and createFlag:
        xprint ("info","Creating project %s" %(project))
        try:
            os.makedirs(project, 0755)
        except OSError:
            pass
        create_dirs(project, BENCH_DIRS)
        create_files(project, FILES)

    if testcase and project and not createFlag:
        xprint ("info", "Creating testcases")
        create_testcase(project, testcase)

    if testsuite and project and not createFlag:
        xprint ("info", "Creating testsuite")
        create_testsuite(project, testsuite)

    if project and deleteFlag:
        if project == ".":
            xprint("warn", "Can't delete current directory")
        else:
            try:
                shutil.rmtree(project, False)
                xprint ("info", "Deleting project '%s'" %project)
            except Exception as e:
                print e

    if project and target:
        update_build(project, target, addFlag)


