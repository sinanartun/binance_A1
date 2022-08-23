create table BTCUSDT
(
    bid       int         null,
    parameter char(7)     null,
    price     float(7, 2) null,
    quantity  float(7, 5) null,
    time      datetime    null,
    maker     tinyint     null
);