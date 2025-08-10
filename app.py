from flask import Flask ,  render_template , session , request , flash ,redirect   
import psycopg2

import pymysql


# db=pymysql.connect(user='root', host='localhost',password='',db='muse')

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
@app.route('/')
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
@app.route('/lstU', methods=['POST','GET'])
def lstU():
    #liste des utilisteurs du systemes
    us = data()
    all = us.cursor()
    all.execute("select * , idm , lib_muse,province_m from users inner join muses on users.muse_id = muses.idm") 
    da = all.fetchall()

    return render_template('back-end/export-table.html' , aff = da)

## enregistrement de la collection 
#
#
#
#
@app.route('/collectionAdd', methods = ['POST','GET']) 
def collectionAdd():
    if 'session' in session:
        if request.method == 'POST':
            collection  = request.form['collection'] 
            description = request.form['desc'] 

            ##
            ##
            ## verification  du collection 
            #
            coll = data()
            ver = coll.cursor()
            ver.execute("select * from collections where nom_collection = %s" , [collection])
            dataVer = ver.fetchone()

            if dataVer:
                flash("la collection existe deja !!!!")
            else:
                dbd = data()
                cur = dbd.cursor()
                cur.execute('insert into collections(nom_collection,desc_collection,collection_id) values(%s,%s,%s)',[collection,description,session['id']])
                dbd.commit()
                cur.close()
                dbd.close()   

                flash(f"{collection} enregistre ")
                return redirect('/collectionAdd') 
            
        return render_template('back-end/collectionAdd.html')
    else:
        return  redirect('/login')
     
# affichage contenue table collection
#
#
#
@app.route('/lstcoll')
def lstcoll():

    if 'session' in session :
        #liste des informations dans la table collections
        #
        #
        #
        coll = data()
        cur = coll.cursor()
        cur.execute("select * , username from collections inner join users on collections.collection_id = users.idu") 
        aff = cur.fetchall()

        return render_template('back-end/collection-table.html', aff  = aff )

    else:
        return redirect('/login')
#
#
#
# creation d'artefact 
# 
@app.route('/artefactAdd', methods =['POST','GET']) 
def artefactAdd():
    if 'session' in session:
        if request.method == 'POST':
            numero = request.form['numero']
            titre = request.form['titre']
            desc = request.form['desc']
            date = request.form['date']
            materiau = request.form['materiau']
            dimension = request.form['dimension']
            provenance = request.form['provenance']
            collection = request.form['collection']

            #
            # le numero_accession
            #
            acc = data()
            accc = acc.cursor()
            accc.execute("select * from artefacts where numero_accession = %s", [numero])
            ver = accc.fetchone()

            if ver:
                flash("le numero_accession existe deja")
            else:

             
                    

                artef = data()
                cur = artef.cursor()
                cur.execute("insert into artefacts(numero_accession,tire,description,date_creation,materiau,dimensions,provenance,collection_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",[numero,titre,desc,date,materiau,dimension,provenance,collection])
                artef.commit() 
                cur.close()
                artef.close()

                flash("donnee enregistre")
                return redirect('/artefactAdd') 


        #collection dans la table artect
        coll = data()
        cur = coll.cursor()
        cur.execute("select * from collections ")
        aff = cur.fetchall()

        return render_template('back-end/form-artefact.html', aff = aff)
    else:
        return redirect('/login')
    
# affichage contenue table artefact
@app.route('/artfvue')
def artfvue():

   if 'session' in session:
       
        art = data()
        cur = art.cursor()
        cur.execute("select * from artefacts")
        dt = cur.fetchall()

        return render_template('back-end/artefact-table.html', artfaff = dt)
   else:
       return redirect('/login') 

 #affichage table artefact
@app.route('/lstArtf', methods =['POST','GET'])
def lstArtf():

    if 'session' in session:
            pass
        
    else:

        return redirect('/login')   
     
#affichage contenue createur
@app.route('/lstcreat', methods=['POST','GET'])
def lstcreat():

    if 'session' in session:

        pass

    else:
        return redirect('/login') 


#enregistrement createurs
@app.route('/creatform', methods = ['POST','GET'])
def creatform():

    if 'session' in session:

        if request.method == 'POST':

            nom = request.form['nom']
            prenom = request.form['prenom'] 
            dateN  = request.form['dateN']
            dateD  = request.form['dateD']
            Nat    = request.form['Nat']

            crt = data()
            cur = crt.cursor()
            cur.execute("insert into createurs(nom,prenom,date_nai,date_deces,nationalite,user_id) values(%s,%s,%s,%s,%s,%s)",[nom,prenom,dateN,dateD,Nat,session['id']])
            crt.commit() 
            cur.close()
            crt.close()
            flash("information enregistre !!!") 

        return render_template('back-end/form-createurs.html')
                   
    else:
        return redirect('/login')
    
# affichage contenue table createur

@app.route('/crtaff')
def crtaff():

    if 'session' in session:

            crtaf = data()
            cur = crtaf.cursor()
            cur.execute("select * from createurs")
            view = cur.fetchall()
            return render_template('back-end/create-table.html', crt = view)

    else:
        return redirect('/login')
        

    
# affichage contenue table artefact et createurs
@app.route('/lstart_creat', methods=['POST','GET'])
def lsart_creat():

    if 'session' in session:
        pass

    else:
        return redirect('/login')

## boucle 

if __name__ == '__main__':
    app.run(debug=True)