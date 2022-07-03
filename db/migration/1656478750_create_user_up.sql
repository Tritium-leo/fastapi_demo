CREATE TABLE IF NOT EXISTS `users`
(
    id              INTEGER auto_increment,
    uuid            bigint       not null unique,
    username        VARCHAR(20)  not null unique,
    _password_hash_ VARCHAR(256) not null,
    state           smallint     not null,
    create_time     datetime     NOT NULL DEFAULT NOW(),
    update_time     datetime     NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (id)
);
-- zhushi
-- pg or oracle
-- COMMENT ON TABLE users IS  'user';
-- COMMENT ON COLUMN users.id IS 'auto_id';
-- COMMENT ON COLUMN users.uuid IS 'PK_snowflower';
-- COMMENT ON COLUMN users.username IS 'username';
-- COMMENT ON COLUMN users._password_hash_ IS 'hash_password';

-- mysql
-- alter table testcase
-- change column id id int not null default 0 comment '测试表id'

-- suoyin
CREATE INDEX user_uuid_username ON users (uuid, username);