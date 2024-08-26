create database flask_app;

create table messages(
    id bigserial not null primary key,
    title varchar(50) not null,
    content text not null
);

create table tasks(
    id bigserial not null primary key,
    content varchar(50) not null,
    checked boolean
);

