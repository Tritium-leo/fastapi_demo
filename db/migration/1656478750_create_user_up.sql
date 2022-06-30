CREATE TABLE IF NOT EXISTS `user` (
    id INTEGER ,
    uuid INTEGER,
    username VARCHAR(20) not null unique ,
    _password_hash_ VARCHAR(256) not null,
    create_time datetime NOT NULL DEFAULT NOW(),
    update_time datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (uuid)
);
-- zhushi
-- pg or oracle
-- COMMENT ON TABLE user IS  'user';
-- COMMENT ON COLUMN user.id IS 'auto_id';
-- COMMENT ON COLUMN user.uuid IS 'PK_snowflower';
-- COMMENT ON COLUMN user.username IS 'username';
-- COMMENT ON COLUMN user._password_hash_ IS 'hash_password';

-- mysql
-- alter table test
-- change column id id int not null default 0 comment '测试表id'

-- suoyin
CREATE INDEX user_uuid_username ON user (uuid,username);