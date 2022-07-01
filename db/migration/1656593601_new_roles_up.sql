CREATE TABLE IF NOT EXISTS `roles` (
    id INTEGER auto_increment,
    rolename VARCHAR(20) not null unique ,
    create_time datetime NOT NULL DEFAULT NOW(),
    update_time datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (id)
);

-- suoyin
CREATE INDEX roles_id_rolename ON roles (id,rolename);