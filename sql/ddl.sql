CREATE TABLE store_types (
    type_id   int PRIMARY KEY,
    type_name varchar(50) NOT NULL;
);

CREATE TABLE employees (
    employee_id int PRIMARY KEY,
    title       varchar(50) not null,
    first_name  varchar(50) not null,
    last_name   varchar(50) not null,
);

CREATE TABLE stores (
    store_id    int PRIMARY KEY,
    type_id     int         NOT NULL FOREIGN KEY REFERENCES store_types(type_id),
    contact_id  int         NOT NULL FOREIGN KEY REFERENCES employees(employee_id),
    store_name  varchar(50) NOT NULL,
    store_name2 varchar(50),
    address1    varchar(50),
    address2    varchar(50),
    city        varchar(50),
    state       char(2),
    country     varchar(50),
    latitude decimal(9,6),
    longitude decimal(9,6),
);

CREATE TABLE store_hours (
    store_id int PRIMARY KEY,
    day_of_week varchar(10) PRIMARY KEY ,
    open_time time,
    close_time time()
);

