-- vim: ts=2 sts=2 sw=2 et autoindent

drop database if exists taskmaster;
create database taskmaster with encoding 'UTF8';

create table User (
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
  docType int not null references DocType(id),
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
  taskType int not null references TaskType(id),
  title varchar(128) not null,
  descDoc int not null references Doc(id),
  primary key (id)
);

insert into TaskType (id, name) values (1, 'dev');
insert into TaskType (id, name) values (2, 'bug');
insert into DocType (id, name) values (1, 'task');

declare
  userId int;
  docId int;
begin
  insert into User (username, fullname) values ('njc', 'Nate C') returning userId;
  insert into Doc (docType, body) values (1, 'My task.') returning docId;
  insert into Task (taskType, title, descDoc) value (1, 'First task', docId);
end;

