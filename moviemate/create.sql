-- phpMyAdmin SQL Dump
-- version 2.11.9.6
-- http://www.phpmyadmin.net
--
-- Host: elnux7.cs.umass.edu
-- Generation Time: Dec 02, 2009 at 02:41 PM
-- Server version: 5.1.37
-- PHP Version: 5.1.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `cs445_2_f09`
--

-- --------------------------------------------------------

--
-- Table structure for table `Advertisement`
--

DROP TABLE IF EXISTS `Advertisement`;
CREATE TABLE IF NOT EXISTS `Advertisement` (
  `ad_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product` varchar(255) DEFAULT NULL,
  `imgURL` varchar(255) DEFAULT NULL,
  `refURL` varchar(255) DEFAULT NULL,
  `country` char(40) DEFAULT NULL,
  `state` char(20) DEFAULT NULL,
  `city` char(40) DEFAULT NULL,
  `numClicks` int(10) unsigned DEFAULT NULL,
  `commission` float(5,2) DEFAULT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `targetAge` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`ad_id`),
  UNIQUE KEY `product` (`product`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Advertisor`
--

DROP TABLE IF EXISTS `Advertisor`;
CREATE TABLE IF NOT EXISTS `Advertisor` (
  `adver_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) DEFAULT NULL,
  `address` char(30) DEFAULT NULL,
  `state` char(20) DEFAULT NULL,
  `city` char(40) DEFAULT NULL,
  `country` char(40) DEFAULT NULL,
  `zip` smallint(6) DEFAULT NULL,
  `balance` float(9,2) DEFAULT NULL,
  PRIMARY KEY (`adver_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `address` (`address`,`city`,`state`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `chooseType`
--

DROP TABLE IF EXISTS `chooseType`;
CREATE TABLE IF NOT EXISTS `chooseType` (
  `fmid` int(10) unsigned NOT NULL DEFAULT '0',
  `genre` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`fmid`,`genre`),
  KEY `genre` (`genre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `createFMovie`
--

DROP TABLE IF EXISTS `createFMovie`;
CREATE TABLE IF NOT EXISTS `createFMovie` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `fmid` int(10) unsigned NOT NULL DEFAULT '0',
  `tmstamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`fmid`),
  UNIQUE KEY `fmid` (`fmid`,`tmstamp`),
  UNIQUE KEY `user_id` (`user_id`,`tmstamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `FantasyMovie`
--

DROP TABLE IF EXISTS `FantasyMovie`;
CREATE TABLE IF NOT EXISTS `FantasyMovie` (
  `fmid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) DEFAULT NULL,
  `script` text,
  `avgRating` float(6,4) DEFAULT NULL,
  `numOfRatings` int(10) unsigned DEFAULT NULL,
  `MPAA` enum('G','PG','PG13','NC17','R','NR','Adult') DEFAULT NULL,
  `earnings` float(14,2) DEFAULT NULL,
  `total_cost` float(11,2) DEFAULT NULL,
  PRIMARY KEY (`fmid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Genre`
--

DROP TABLE IF EXISTS `Genre`;
CREATE TABLE IF NOT EXISTS `Genre` (
  `gid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `genre` char(20) DEFAULT NULL,
  PRIMARY KEY (`gid`),
  UNIQUE KEY `genre` (`genre`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=29 ;

-- --------------------------------------------------------

--
-- Table structure for table `hasUpdate`
--

DROP TABLE IF EXISTS `hasUpdate`;
CREATE TABLE IF NOT EXISTS `hasUpdate` (
  `user_id` int(10) unsigned DEFAULT NULL,
  `up_id` int(10) unsigned NOT NULL DEFAULT '0',
  `entity` char(20) DEFAULT NULL,
  `action` enum('friends','not_friends','favorite','not_favorite','likes','hates','not_interested') DEFAULT NULL,
  `tmstamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`up_id`),
  UNIQUE KEY `user_id` (`user_id`,`action`,`entity`),
  KEY `tmstamp` (`tmstamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `hiresCast`
--

DROP TABLE IF EXISTS `hiresCast`;
CREATE TABLE IF NOT EXISTS `hiresCast` (
  `fmid` int(10) unsigned NOT NULL DEFAULT '0',
  `pid` int(10) unsigned NOT NULL DEFAULT '0',
  `salery` float(9,2) DEFAULT NULL,
  PRIMARY KEY (`fmid`,`pid`),
  KEY `pid` (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `hiresDirect`
--

DROP TABLE IF EXISTS `hiresDirect`;
CREATE TABLE IF NOT EXISTS `hiresDirect` (
  `fmid` int(10) unsigned NOT NULL DEFAULT '0',
  `pid` int(10) unsigned DEFAULT NULL,
  `salery` float(9,2) DEFAULT NULL,
  PRIMARY KEY (`fmid`),
  KEY `pid` (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `isFriend`
--

DROP TABLE IF EXISTS `isFriend`;
CREATE TABLE IF NOT EXISTS `isFriend` (
  `uid1` int(10) unsigned NOT NULL DEFAULT '0',
  `uid2` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid1`,`uid2`),
  KEY `uid2` (`uid2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `isInvolved`
--

DROP TABLE IF EXISTS `isInvolved`;
CREATE TABLE IF NOT EXISTS `isInvolved` (
  `pid` int(10) unsigned NOT NULL DEFAULT '0',
  `mid` int(10) unsigned NOT NULL DEFAULT '0',
  `role` enum('Actor','Actress','Director') NOT NULL DEFAULT 'Actor',
  PRIMARY KEY (`pid`,`mid`,`role`),
  KEY `mid` (`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `isType`
--

DROP TABLE IF EXISTS `isType`;
CREATE TABLE IF NOT EXISTS `isType` (
  `mid` int(10) unsigned NOT NULL DEFAULT '0',
  `gid` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`mid`,`gid`),
  KEY `genre` (`gid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `LikesGenre`
--

DROP TABLE IF EXISTS `LikesGenre`;
CREATE TABLE IF NOT EXISTS `LikesGenre` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `genre` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`genre`),
  KEY `genre` (`genre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `LikesMovie`
--

DROP TABLE IF EXISTS `LikesMovie`;
CREATE TABLE IF NOT EXISTS `LikesMovie` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `mid` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`mid`),
  KEY `mid` (`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `LikesPerson`
--

DROP TABLE IF EXISTS `LikesPerson`;
CREATE TABLE IF NOT EXISTS `LikesPerson` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `pid` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`pid`),
  KEY `pid` (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Movie`
--

DROP TABLE IF EXISTS `Movie`;
CREATE TABLE IF NOT EXISTS `Movie` (
  `mid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `year` char(9) NOT NULL DEFAULT '',
  `avgRating` float(3,1) DEFAULT NULL,
  `numOfRatings` int(10) unsigned DEFAULT NULL,
  `MPAA` enum('G','PG','PG-13','NC-17','R','NR','Adult') DEFAULT NULL,
  PRIMARY KEY (`name`,`year`),
  UNIQUE KEY `mid` (`mid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1069145 ;

-- --------------------------------------------------------

--
-- Table structure for table `Person`
--

DROP TABLE IF EXISTS `Person`;
CREATE TABLE IF NOT EXISTS `Person` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `age` tinyint(4) DEFAULT NULL,
  `gender` enum('?','M','F') NOT NULL DEFAULT '?',
  PRIMARY KEY (`name`,`gender`),
  UNIQUE KEY `pid` (`pid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1356872 ;

-- --------------------------------------------------------

--
-- Table structure for table `Rates`
--

DROP TABLE IF EXISTS `Rates`;
CREATE TABLE IF NOT EXISTS `Rates` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `mid` int(10) unsigned NOT NULL DEFAULT '0',
  `rating` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`user_id`,`mid`),
  KEY `mid` (`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `RatesFMovie`
--

DROP TABLE IF EXISTS `RatesFMovie`;
CREATE TABLE IF NOT EXISTS `RatesFMovie` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `fmid` int(10) unsigned NOT NULL DEFAULT '0',
  `rating` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`user_id`,`fmid`),
  KEY `fmid` (`fmid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Review`
--

DROP TABLE IF EXISTS `Review`;
CREATE TABLE IF NOT EXISTS `Review` (
  `review_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned DEFAULT NULL,
  `mid` int(10) unsigned DEFAULT NULL,
  `summary` text,
  PRIMARY KEY (`review_id`),
  KEY `user_id` (`user_id`),
  KEY `mid` (`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `suppliesAd`
--

DROP TABLE IF EXISTS `suppliesAd`;
CREATE TABLE IF NOT EXISTS `suppliesAd` (
  `adver_id` int(10) unsigned NOT NULL DEFAULT '0',
  `ad_id` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`adver_id`,`ad_id`),
  KEY `ad_id` (`ad_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `targetsGenre`
--

DROP TABLE IF EXISTS `targetsGenre`;
CREATE TABLE IF NOT EXISTS `targetsGenre` (
  `ad_id` int(10) unsigned NOT NULL DEFAULT '0',
  `genre` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`ad_id`,`genre`),
  KEY `genre` (`genre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Updates`
--

DROP TABLE IF EXISTS `Updates`;
CREATE TABLE IF NOT EXISTS `Updates` (
  `up_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `entity` char(20) DEFAULT NULL,
  `action` enum('friends','not_friends','favorite','not_favorite','likes','hates','not_interested') DEFAULT NULL,
  `tmstamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`up_id`),
  UNIQUE KEY `entity` (`entity`,`action`,`tmstamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
CREATE TABLE IF NOT EXISTS `Users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `isAdmin` tinyint(4) DEFAULT NULL,
  `login` varchar(255) NOT NULL DEFAULT '',
  `psword` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `age` tinyint(4) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `gender` enum('?','M','F') DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `fantasyBudget` float(11,2) DEFAULT NULL,
  PRIMARY KEY (`login`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `IUserNames` (`name`(10)) USING BTREE
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=489510 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `UserView`
--
DROP VIEW IF EXISTS `UserView`;
CREATE TABLE IF NOT EXISTS `UserView` (
`user_id` int(10) unsigned
,`login` varchar(255)
,`name` varchar(255)
,`age` tinyint(4)
,`country` varchar(255)
,`state` varchar(255)
,`city` varchar(255)
,`gender` enum('?','M','F')
,`school` varchar(255)
,`fantasyBudget` float(11,2)
);
-- --------------------------------------------------------

--
-- Structure for view `UserView`
--
DROP TABLE IF EXISTS `UserView`;
-- in use(#1142 - SHOW VIEW command denied to user 'cs445_2_f09'@'elsrv1.cs.umass.edu' for table 'UserView')

