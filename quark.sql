create table account (
  id int not null primary key auto_increment
  ,user_id int not null
  ,`name` varchar(255) not null
  ,`type` tinyint not null comment '1 Asset, 2 Liability'
  ,initial_balance decimal(20, 2) default 0
  ,balance decimal(20, 2) default 0
  ,order_num int not null default 0
  ,created_at datetime not null
  ,updated_at timestamp not null default current_timestamp on update current_timestamp
  ,index idx_user_name (user_id, `name`)
);
