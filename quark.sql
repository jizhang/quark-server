create table `user` (
  id int not null primary key auto_increment
  ,username varchar(255) not null
  ,password varchar(255) not null
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,index idx_username (username)
);

insert into `user` values
(1, 'test', 'pbkdf2:sha256:150000$RQEmXgTI$39b2c288c2af0cc6380add124254364a910483acd0b8d1dc81260aa1649e99d5', now(), now());

create table account (
  id int not null primary key auto_increment
  ,user_id int not null
  ,`name` varchar(255) not null
  ,`type` tinyint not null comment '1 Asset, 2 Liability'
  ,initial_balance decimal(20, 2) default 0
  ,balance decimal(20, 2) default 0
  ,order_num int not null default 0
  ,is_hidden tinyint not null default 0
  ,is_deleted tinyint not null default 0
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,index idx_user_name (user_id, `name`)
);

create table category (
  id int not null primary key auto_increment
  ,user_id int not null
  ,`type` tinyint not null comment '1 Expense, 2 Income'
  ,`name` varchar(255) not null
  ,is_deleted tinyint not null default 0
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,index idx_user (user_id)
);

create table record (
  id bigint not null primary key auto_increment
  ,user_id int not null
  ,record_type tinyint not null comment '1 Expense, 2 Income, 3 Transfer'
  ,category_id int not null default 0
  ,account_id int not null
  ,target_account_id int not null default 0
  ,record_time datetime not null
  ,amount decimal(20, 2) not null
  ,remark varchar(255) not null default ''
  ,is_deleted tinyint not null default 0
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,index idx_user_time (user_id, record_time)
);

create table user_setting (
  id int not null primary key auto_increment
  ,user_id int not null
  ,setting_key varchar(255) not null
  ,setting_value_json varchar(255) not null
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,unique key uk_user_setting (user_id, setting_key)
);
