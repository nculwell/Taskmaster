-- vim: ts=2 sts=2 sw=2 et autoindent

create table usr (
  id serial,
  deleted boolean not null default false,
  username varchar(32) not null,
  fullname varchar(128) not null,
  create_ts timestamp not null default current_timestamp,
  primary key (id)
);

create table pwd (
  usr_id int references usr(id),
  method varchar(20) not null,
  salt bytea not null,
  hash bytea not null,
  create_ts timestamp not null default current_timestamp,
  primary key (usr_id, create_ts)
);

create table doc_type (
  id int,
  deleted boolean not null default false,
  name varchar(20) not null,
  primary key (id)
);

create table doc (
  id serial,
  doc_type_id int not null references doc_type(id),
  body text not null,
  create_ts timestamp not null default current_timestamp,
  primary key (id)
);

create table task_type (
  id int,
  deleted boolean not null default false,
  name varchar(20) not null,
  primary key (id)
);

create table tsk (
  id serial,
  deleted boolean not null default false,
  tsk_type_id int not null references task_type(id),
  title varchar(128) not null,
  desc_doc_id int not null references doc(id),
  create_ts timestamp not null default current_timestamp,
  primary key (id)
);

create table tsk_usr_role (
  id int,
  deleted boolean not null default false,
  name varchar(20) not null,
  primary key (id)
);

create table tsk_usr (
  tsk_id int not null references tsk(id),
  tsk_usr_role_id int not null references tsk_usr_role(id),
  usr_id int not null references usr(id),
  primary key (tsk_id, tsk_usr_role_id, usr_id)
);

create view v_tsk as
  select
    t.id tsk_id, t.tsk_type_id, tt.name tsk_type_name
  , t.title, t.desc_doc_id
  from tsk t
  join task_type tt on tt.id = t.tsk_type_id
  where not t.deleted
;

create view v_tsk_usr as
  select t.*
  , tu.tsk_usr_role_id, tur.name tsk_usr_role_name
  , tu.usr_id, u.username, u.fullname
  from v_tsk t
  join tsk_usr tu on tu.tsk_id = t.tsk_id
  join tsk_usr_role tur on tur.id = tu.tsk_usr_role_id
  join usr u on u.id = tu.usr_id
  where not u.deleted
;

insert into task_type (id, name) values (1, 'dev');
insert into task_type (id, name) values (2, 'bug');
insert into doc_type (id, name) values (1, 'task');
insert into tsk_usr_role (id, name) values (1, 'dev');
insert into tsk_usr_role (id, name) values (2, 'pqa');
insert into tsk_usr_role (id, name) values (3, 'qa');

do $$
declare
  usr_id int;
  doc_id int;
  tsk_id int;
  pass_salt bytea := '\x3964d9aa1eabf7685aecdb9cb368b22c';
  pass_hash bytea := -- password is 'xxx'
    '\xc86b27f5a1e71cb82851661ba9e076ec6e310d419080183bef1b7d2173efa96d';
begin
  insert into usr (username, fullname)
    values ('njc', 'Nate C');
  usr_id := currval(pg_get_serial_sequence('usr', 'id'));
  insert into pwd (usr_id, method, salt, hash)
    values (usr_id, 'sha256:200', pass_salt, pass_hash);
  insert into doc (doc_type_id, body)
    values (1, 'My task.');
  doc_id := currval(pg_get_serial_sequence('doc', 'id'));
  insert into tsk (tsk_type_id, title, desc_doc_id)
    values (1, 'First task', doc_id);
  tsk_id := currval(pg_get_serial_sequence('tsk', 'id'));
  raise notice 'tsk_id: %', tsk_id;
  insert into tsk_usr (tsk_id, tsk_usr_role_id, usr_id)
    values (tsk_id, 1, usr_id);
end;
$$

