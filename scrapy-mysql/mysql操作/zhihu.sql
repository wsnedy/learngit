CREATE DATABASE zhihudb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE TABLE zhihuinfo (
	url  			text,
    nickname		text,
    agree_count 	int,
    thanks_count	int,
    fans_count  	int,
    province		text
)ENGINE=MyISAM DEFAULT CHARSET=utf8;