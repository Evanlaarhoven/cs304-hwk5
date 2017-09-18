## Emily Van Laarhoven and Jacki Hom
## Flask HWK5 due 3/23/17 at 12am

from evanlaardsn import DSN
import dbconn2, sys, MySQLdb
from flask import Flask, render_template, request, url_for, flash
app = Flask(__name__)
app.secret_key = 'wushuaksjegbalkrjb'

def getConn():
# """returns database connection; this function contains the line that gets changed from to wmdb"""
    DSN['db']='evanlaar_db'
    return dbconn2.connect(DSN)

def handle_form():
# """invokes the medhods which take info from form and check if it's missing,
#   check if it already exits, and inserts it into database"""
    if request.method == 'POST':
        formDict = request.form
        if checkMissingInput(formDict):
            if checkAlreadyInserted(formDict['actornm']):
                insertActor(formDict['actornm'],formDict['actorname'],formDict['actorbirthday'])

def isNumeric(s):
# """helper method to make sure nm is numeric"""
    try:
        int(s)
        return True
    except ValueError:
        return False

def checkMissingInput(formDict):
# """checks if each of the components of the form are filled in and that the nm
#   is an integer.  If any of these are false, flashes error message and returns False"""
    okToInsert = True
    actornm = formDict['actornm']
    actorname = formDict['actorname']
    actorbirthday = formDict['actorbirthday']
    if not actornm.strip():
        okToInsert = False
        flash("missing input: actor nm")
    if not actorname.strip():
        okToInsert = False
        flash("missing input: actor name")
    if not actorbirthday.strip():
        okToInsert = False  
        flash("missing input: actor birthday")
 ## check that actornm is an integer
    if not isNumeric(actornm):
        okToInsert = False
        flash("actornm needs to be integer")
    return okToInsert

def checkAlreadyInserted(nm):
# """checks whether nm is already in the db and returns False if so"""
    okToInsert = True
    conn = getConn()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select count(*) from person where nm=%s',[nm])
    results = curs.fetchall()
    count = results[0]['count(*)'] 
    if count >=1:
        okToInsert = False
        flash("error: actor exists") 
    else:
        print "actor not in db already"
    return okToInsert

def insertActor(actornm,actorname,actorbirthday):
# """connects to db and inserts actor into person table, flashes success message"""
    conn = getConn()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into person values (%s,%s,%s,%s)',[actornm,actorname,actorbirthday, 1261])
    ## flash success
    flash("actor successfully inserted")

@app.route('/insertActor/',methods=['GET','POST'])
def controller():
    handle_form()
    return render_template('form.html')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',6849) #using Emily uid port #
