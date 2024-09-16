/* domain table to hold different types of stores */
CREATE TABLE store_types (
    type_id   int PRIMARY KEY,
    type_name varchar(50) NOT NULL;
);

/* table to hold employees at a specific store (manager, etc.) */
/* if employees can work at multiple stores, this table can be further normalized */
CREATE TABLE employees (
    employee_id int PRIMARY KEY,
    title       varchar(50) NOT NULL,
    first_name  varchar(50) NOT NULL,
    last_name   varchar(50) NOT NULL,
);

/* table to hold store data */
CREATE TABLE stores (
    store_id             int PRIMARY KEY,
    type_id              int         NOT NULL FOREIGN KEY REFERENCES store_types(type_id),
    contact_id           int         NOT NULL FOREIGN KEY REFERENCES employees(employee_id),
    store_name           varchar(50) NOT NULL,
    store_name2          varchar(50),
    phone                varchar(20),
    email                varchar(255),
    address1             varchar(50),
    address2             varchar(50),
    city                 varchar(50),
    `state`              char(2),
    country              varchar(50),
    latitude             decimal(9, 6),
    longitude            decimal(9, 6),
    facebook_url         varchar(50),
    video_url            varchar(50),
    main_image_url       varchar(50),
    view_store_url       varchar(50),
    alternate_image_url1 varchar(50),
    alternate_image_url2 varchar(50)
);

/* table to hold store hours */
CREATE TABLE store_hours (
    store_id    int,
    day_of_week varchar(10) PRIMARY KEY,
    open_time   time,
    close_time  time,
    PRIMARY KEY (store_id, day_of_week)
);

/* table to hold store's seasonal hours */
CREATE TABLE store_seasonal_hours (
    store_id   int,
    day_num    tinyint NOT NULL,
    month_num  tinyint NOT NULL,
    open_time  time,
    close_time time,
    PRIMARY KEY (store_id, day_num, month_num)
);
