CREATE TABLE IF NOT EXISTS `role_user` (
    id INTEGER auto_increment,
    user_id INTEGER not null ,
    role_id INTEGER NOT NULL ,
    create_time datetime NOT NULL DEFAULT NOW(),
    update_time datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (id)
);

-- suoyin
CREATE INDEX role_user_user_id_role_id ON role_user (id,user_id,role_id);