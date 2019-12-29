use MusicBot ;

drop table IF EXISTS MusicBot.tracks ;

SET NAMES 'utf8mb4';

CREATE TABLE `tracks` (
  `tra_id` int(11) NOT NULL,
  `tra_deleted` tinyint(4) NOT NULL DEFAULT '0',
  `tra_deletion_date` datetime DEFAULT NULL,
  `tra_url` varchar(512) NOT NULL,
  `tra_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tra_author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tra_album` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tra_duration` int(11) NOT NULL,
  `tra_genres` varchar(2048) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tra_free` tinyint(4) NOT NULL DEFAULT '0',
  `tra_start_time` double DEFAULT NULL,
  `tra_finish_time` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Holding tracks information';

ALTER TABLE `tracks`
  ADD PRIMARY KEY (`tra_id`),
  ADD UNIQUE KEY `tra_url` (`tra_url`),
  ADD KEY `tra_genres` (`tra_genres`(767)),
  ADD KEY `tra_free` (`tra_free`),
  ADD KEY `tra_album` (`tra_album`),
  ADD KEY `tra_author` (`tra_author`),
  ADD KEY `tra_title` (`tra_title`),
  ADD KEY `tra_deleted` (`tra_deleted`);

ALTER TABLE `tracks`
  MODIFY `tra_id` int(11) NOT NULL AUTO_INCREMENT;