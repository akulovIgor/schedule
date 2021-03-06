create table workers(
    id integer GENERATED BY DEFAULT AS IDENTITY primary key,
    name varchar(255),
    surname varchar(255),
    id_dialog integer,
    id_role integer,
    FOREIGN KEY(id_role) REFERENCES roles(id)
);

create table roles(
    id integer GENERATED BY DEFAULT AS IDENTITY primary key,
    role varchar(255)
);

create table role_shift(
    id integer GENERATED BY DEFAULT AS IDENTITY primary key,
    id_role integer,
    id_shift integer,
    id_color integer,
    FOREIGN KEY(roles) REFERENCES roles(id),
    FOREIGN KEY(shifts) REFERENCES shifts(id),
    FOREIGN KEY(colors) REFERENCES colors(id)
);

create table shifts(
    id integer GENERATED BY DEFAULT AS IDENTITY primary key,
    shift varchar(255)
);

create table colors(
    id integer GENERATED BY DEFAULT AS IDENTITY primary key,
    red numeric(10),
    green numeric(10),
    blue numeric(10)
);

insert into shifts (shift)
values
    ("09.00 -- 18.00"),
    ("10.00 -- 19.00"),
    ("11.00 -- 20.00"),
    ("15.00 -- 24.00"),
    ("выходной"),
    ("отпуск");

insert into roles (role)
values
    ("chater"),
    ("caller"),
    ("gibrid");

insert into colors (red, green, blue)
values
    (0.6, 0.0, 1.0),
    (0.40784314, 0.0, 0.78039217),
    (0.6, 0.0, 1.0),
    (1.0, 1.0, 1.0),
    (0.91764706, 0.81960785, 0.8627451),
    (0.7411765,0.9019608, 0.88235295),
    (0.0, 1.0, 1.0),
    (1.0, 0.8, 0.6),
    (1.0, 1.0, 0.0);

insert into role_shift (id_role, id_shift, id_color)
values
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 3),
    (1, 5, 8),
    (1, 6, 9),
    (2, 1, 4),
    (2, 2, 5),
    (2, 3, 6),
    (2, 4, 7),
    (2, 5, 8),
    (2, 6, 9),
    (3, 1, 1),
    (3, 2, 2),
    (3, 3, 3),
    (3, 5, 8),
    (3, 6, 9),
    (3, 1, 4),
    (3, 2, 5),
    (3, 3, 6),
    (3, 4, 7),
    (3, 5, 8),
    (3, 6, 9);
