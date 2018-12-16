-- vim: ts=2 sts=2 sw=2 et autoindent

create table usr (
  id serial,
  deleted boolean not null default false,
  username varchar(32) not null,
  fullname varchar(128) not null,
  primary key (id)
);

create table DocType (
  id int,
  deleted boolean not null default false,
  name varchar(20) not null,
  primary key (id)
);

create table Doc (
  id serial,
  docTypeId int not null references DocType(id),
  body text not null,
  primary key (id)
);

create table TaskType (
  id int,
  deleted boolean not null default false,
  name varchar(20) not null,
  primary key (id)
);

create table Task (
  id serial,
  deleted boolean not null default false,
  taskTypeId int not null references TaskType(id),
  title varchar(128) not null,
  descDocId int not null references Doc(id),
  primary key (id)
);

create table TaskUsrRole (
  id int,
  deleted boolean not null default false,
  name varchar(20) not null,
  primary key (id)
);

create table TaskUsr (
  taskId int not null references Task(id),
  taskUsrRoleId int not null references TaskUsrRole(id),
  userId int not null references usr(id),
  primary key (taskId, taskUsrRoleId, userId)
);

create view VTask as
  select
    t.id taskId, t.taskTypeId, tt.name taskTypeName
  , t.title, t.descDocId
  from Task t
  join TaskType tt on tt.id = t.taskTypeId
  where not t.deleted
;

create view VTaskUsr as
  select t.*
  , tu.taskUsrRoleId, tur.name taskUsrRoleName
  , tu.userId, u.username, u.fullname
  from VTask t
  join TaskUsr tu on tu.taskId = t.taskId
  join TaskUsrRole tur on tur.id = tu.taskUsrRoleId
  join usr u on u.id = tu.userId
  where not u.deleted
;

insert into TaskType (id, name) values (1, 'dev');
insert into TaskType (id, name) values (2, 'bug');
insert into DocType (id, name) values (1, 'task');
insert into TaskUsrRole (id, name) values (1, 'dev');
insert into TaskUsrRole (id, name) values (2, 'pqa');
insert into TaskUsrRole (id, name) values (3, 'qa');

do $$
declare
  userId int;
  docId int;
  taskId int;
begin
  insert into usr (username, fullname)
    values ('njc', 'Nate C');
  userId := currval(pg_get_serial_sequence('usr', 'id'));
  insert into Doc (docTypeId, body)
    values (1, 'My task.');
  docId := currval(pg_get_serial_sequence('Doc', 'id'));
  insert into Task (taskTypeId, title, descDocId)
    values (1, 'First task', docId);
  taskId := currval(pg_get_serial_sequence('Task', 'id'));
  raise notice 'taskId: %', taskId;
  insert into TaskUsr (taskId, taskUsrRoleId, userId)
    values (taskId, 1, userId);
end;
$$

