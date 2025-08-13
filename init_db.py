import psycopg2 

con=psycopg2.connect(database = 'muses', host='localhost', password='    ',user='postgres', port='5432')
cur = con.cursor()

cur.execute(''' create table if not exists muses(idM serial primary key , lib_muse varchar(30) , province_M varchar(40)) ''') 

# creation de la table roles
#
#
cur.execute("""

            create table if not exists roles(
            id_role serial primary key , 
            libelle_role varchar(40))


    """)

#
# information de la table role par defaut
#
#

#cur.execute("insert into roles(libelle_role) values('admin'), ('sous-admin'), ('consultant'),('invite'),('archiviste')") 



# creation de la table users 
cur.execute("""
            create table if not exists users(
            idU bigserial primary key , 
            username varchar(40) , 
            email varchar(30) , 
            password varchar(255) ,
            muse_id serial references muses(idM),
            unique(muse_id))
            
            """)

# cur.execute("alter table users add fonctions varchar(30)")
#cur.execute("alter table users add role_id serial references roles(id_role)")

# inormation par defaut 
# cur.execute("insert into users(username ,email,password) values('admin', 'admin@gmail.com','admin@')") 

## creation de la table collections 

cur.execute(""" 

    create table if not exists collections(
            id_collection serial primary key , 
            nom_collection varchar(255) unique not null,
            desc_collection text , 
            dateCreate_coll timestamp default current_timestamp
            )

""")



# ajout de la cle etrangere

# cur.execute("alter table collections add collection_id bigserial references users(idU)") 

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
## table 
cur.execute(""" 
            create table if not exists artefact_createur(
            id_artefact integer generated always as identity primary key ,
            role varchar(50) ,
            createur_id serial references createurs(id_createur) , 
            artefact_id serial references artefacts(id_atefact), 
            date_register timestamp default current_timestamp
            )

""")

cur.execute(""" 
            create table if not exists ressource_numerique(
            id_ressource serial primary key,
            users_id serial references users(idu),
            artefacts_id serial references artefacts(id_atefact),
            chemin_fichier varchar(255),
            nom_fichier varchar(20),
            type_fichier varchar(50),
            description text,
            date_telechargement timestamp default current_timestamp
            )
""")


con.commit()
cur.close()
con.close()