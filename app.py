from flask import Flask ,  render_template , session , request , flash ,redirect   

import pymysql


db=pymysql.connect(user='root', host='localhost',password='',db='muse')

app = Flask(__name__)
app.secret_key = "museEquipeDev@@"



#
# acceuil (gracia)

@app.route('/home')

def home():
    return render_template('front-end/index.html')


## login (arthur)
@app.route('/login', methods=['POST','GET'])
def login():

    if request.method == 'POST':

        noms = request.form['noms']
        password = request.form['password']
        fonction =request.form['fonction']

        cur=db.cursor()
        cur.execute("select * from users where noms=%s and password=%s",[noms,password])
        data =cur.fetchone()

        if data:

            session['session']=True
            session['noms']= db[1]

            return redirect('/home')
        else:
            return render_template('back-end/auth-login.html')


## register
@app.route('/', methods=['POST','GET'])
@app.route('/register', methods=['POST','GET'])
def register():

    if request.method == 'POST':

        noms = request.form['noms']
        pwd = request.form['pwd']
        fonction = request.form['fonction']
        conf = request.form['conf']

        cur = db.cursor()
        cur.execute("insert into users(noms,pwd,fonction) values(%s,%s,%s)",[noms,pwd,fonction])
        aff=cur.fetchone()

        if aff:
            flash('mot de passe existe')

        elif pwd == conf:

            return redirect('/login')

        else:
            return render_template('auth-register.html')

    

    return render_template('back-end/auth-register.html')










## boucle 

if __name__ == '__main__':
    app.run(debug=True)