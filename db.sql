#
-- creation du data
create schema muse ;

use muse ;

-- creaton de la table muse 

create table if not exists muses(
    idM tinyint auto_increment not null ,
    lib_Muse varchar(30) , 
    constraint pk_muse primary key(idM)
) ; 

-- add province 
alter table muses add province varchar(30)
;
-- informations de la table muse par defaut 
insert into muses(lib_Muse) values('muse nationale') ; 

-- creation de la table users 
create table if not exists users(
    id_users int auto_increment not null ,
    username varchar(40) , 
    first_name varchar(30), 
    function_user varchar(30) , 
    muse_id tinyint , 
    constraint fk_muse foreign key(muse_id) references muses(idM) on delete set null on update no action ,
    constraint pk_users primary key(id_users) 
);

-- ajout de klk informations par defaut
alter table users add password_user varchar(80) , add email_user varchar(80) ;

-- information par defaut 

insert into users(username,first_name,function_user,muse_id,email_user,password_user) values('admin', 'admin','administrataire' , 1, 'admin@gmail.com','admin@');