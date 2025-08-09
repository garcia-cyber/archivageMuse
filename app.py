from flask import Flask ,  render_template , session , request , flash ,redirect   
import psycopg2

import pymysql


db=pymysql.connect(user='root', host='localhost',password='',db='muse')

app = Flask(__name__)
app.secret_key = "museEquipeDev@@"

##
## appel du data 

def data():
    con=psycopg2.connect(database = 'muses', host='localhost', password='    ',user='postgres', port='5432')
    return con 



#
# acceuil (gracia)

@app.route('/home')

def home():
    return render_template('back-end/index.html')


## login (arthur)
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        dt = data()
        cur = dt.cursor()
        cur.execute('select * from users where email=%s and password=%s',[email,password])
        dat= cur.fetchone()
        if dat:

            session['session']=True
            session['id']= dat[0]
            session['fonction'] = dat[5] 
            return redirect('/home')
        else:
            flash("mot de passe incorrecte")
            return redirect('/login')

    return render_template('back-end/auth-login.html') 

## deconnexion
@app.route('/deco')
def deco():
    session.clear()
    return redirect('/login')


## creation des muse 
@app.route('/muse', methods =['POST','GET'])
def muse():
    if 'session' in session:
        return render_template('back-end/forms-validation.html')
    else:
        return redirect('/login')


## register
@app.route('/register', methods=['POST','GET'])
def register():
    pass


@app.route('/Enreg', methods=['POST','GET'])
def Enreg():
        if 'session' in session :
            if request.method == 'POST':
                nomM = request.form['nomM']
                province = request.form['province'] 

                # condition pour verifier si le nom du muse existe deja
                con = data()
                cur = con.cursor()
                cur.execute("insert into muses(lib_muse , province_M) values(%s , %s)",[nomM , province]) 
                con.commit()
                cur.close()
                con.close()
                flash("information enregistre !!!")

            return render_template('back-end/forms-validation.html')
        else:
            return redirect('/login')
    
##
#
# ajout des utilisateurs du systeme par muse

@app.route('/adduser', methods=['POST','GET'])
def adduser():

    #post 
    if request.method == 'POST':
        user = request.form['user'] 
        email = request.form['email'] 
        muse  = request.form['muse']
        fonction = 'sous-admin' 
        password = '12345'

        #verification du mail
        dd = data() 
        mail = dd.cursor()
        mail.execute("select * from users where email = %s", [email])
        ver = mail.fetchone()

        ## !!!! VERIFICATION DU NOM DU MUSE 

        if ver:
            flash("l'email existe deja dans le systeme ")
        else:
            dbs = data()
            cur = dbs.cursor()
            cur.execute("insert into users(username,email,password,muse_id,fonctions) values(%s,%s,%s,%s,%s)",[user,email,password,muse,fonction]) 
            dbs.commit()
            cur.close()
            dbs.close()
            flash(f"{user} enregistre dans le systeme ")  


    # appel des information dans la table muses
    call = data()
    cur = call.cursor()
    cur.execute("select * from muses")
    fetch = cur.fetchall()

    return render_template('back-end/forms-users.html' ,fetch = fetch)

#
#
# liste des muses 
@app.route('/lstM', methods=['POST','GET'])
def lstM():
    return render_template('back-end/export-table.html')







## boucle 

if __name__ == '__main__':
    app.run(debug=True)