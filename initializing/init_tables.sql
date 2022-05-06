DROP TABLE IF EXISTS Active_substance CASCADE;
DROP TABLE IF EXISTS Ingredient CASCADE;
DROP TABLE IF EXISTS Medicine CASCADE;

create table Active_substance (
    id integer primary key,
    name text not null
);

create table Ingredient (
    id integer primary key,
    form text not null,
    dose text not null,
    active_substance integer not null references Active_substance
);

create table Medicine (
    id integer primary key,
    name text not null,
    ingredient integer not null references Ingredient,
    quantity integer not null,
    id_code text not null,
    refund_scope text not null,
    refund text not null,
    surcharge real not null
);