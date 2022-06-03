DROP TABLE IF EXISTS Active_substance CASCADE;
DROP TABLE IF EXISTS Way CASCADE;
DROP TABLE IF EXISTS Form CASCADE;
DROP TABLE IF EXISTS Ingredient CASCADE;
DROP TABLE IF EXISTS Medicine CASCADE;

create table Active_substance (
    id integer primary key,
    name text unique not null 
);

create table Way (
    id integer primary key,
    name text unique not null
);

create table Form (
    id integer primary key,
    name text unique not null,
    way integer not null references Way
);

create table Ingredient (
    id integer primary key,
    active_substance integer not null references Active_substance,
    form integer not null references Form,
    dose text not null
);

create table Medicine (
    id integer primary key,
    name text not null,
    ingredient integer not null references Ingredient,
    quantity real not null,
    contents text not null,
    id_code text not null,
    refund_scope text not null,
    refund text not null,
    surcharge real not null
);