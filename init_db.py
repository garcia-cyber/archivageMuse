import psycopg2 

con=psycopg2.connect(database = 'muses', host='localhost', password='    ',user='postgres', port='5432')
cur = con.cursor()

cur.execute(''' create table if not exists muses(idM serial primary key , lib_muse varchar(30) , province_M varchar(40)) ''') 


# creation de la table users 
cur.execute("""
            create table if not exists users(
            idU bigserial primary key , 
            username varchar(40) , 
            email varchar(30) , 
            password varchar(40) ,
            muse_id serial references muses(idM),
            unique(muse_id))
            
            """)

# cur.execute("alter table users add fonctions varchar(30)")

# inormation par defaut 
# cur.execute("insert into users(username ,email,password) values('admin', 'admin@gmail.com','admin@')") 

## creation de la table collections 

cur.execute(""" 

    create table if not exists collections(
            id_collection serial primary key , 
            nom_collection varchar(255) unique not null,
            desc_collection text
            )

""")


# creation de la table artefact
cur.execute("""
               create table if not exists artefacts(
             id_atefact serial primary key , 
             numero_accession varchar(50),
             tire varchar(50),
             description text,
             date_creation date ,
             materiau varchar(100),
             dimensions varchar(100),
             provenance text,
             collection_id serial references collections(id_collection)
            
             )


  """)


# creation de la table createurs 
cur.execute("""
            create table if not exists createurs(
            id_createur serial primary key ,
            nom varchar(100), 
            prenom varchar(100) ,
            date_nai date , 
            date_deces date ,
            nationalite varchar(50), 
            user_id bigserial references users(idu))
            
            """)

con.commit()
cur.close()
con.close()