DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

--table game for handling games/Matches
create table Matches(
    match_id serial primary key,
    victor integer,
    defeated integer
);


--table player for creating list of Players

create table Players(
    player_id serial primary key,
    name text	
); 



create view result as select player_id,name, (select count(*) from Matches where Players.player_id = Matches.victor) as wins, 
	(select count(*) from Matches where Players.player_id in (Matches.defeated,Matches.victor)) as played from Players order by wins desc;
