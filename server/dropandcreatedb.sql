-- vim: ts=2 sts=2 sw=2 et autoindent

drop database if exists taskmaster;
create database taskmaster with encoding 'UTF8';
create user nate;
grant all on database taskmaster to nate;

