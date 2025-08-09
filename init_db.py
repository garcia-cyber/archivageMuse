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

con.commit()
cur.close()
con.close()