#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def deleteMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    #query = "TRUNCATE " + 'Matches'
    cursor.execute("TRUNCATE TABLE Matches")
    db.commit()
    db.close()
    
def deletePlayers():
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    #query = "TRUNCATE " + 'Players'
    cursor.execute("TRUNCATE TABLE Players")
    db.commit()
    db.close()
    

def countPlayers():
    """Returns the number of players currently registered."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    #query = "SELECT count(*) FROM Players"
    cursor.execute("SELECT count(*) FROM Players")
    val = cursor.fetchall()
    db.close()
    return int(val[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    if name:
        #query = "INSERT into Players(name) values(%s)"
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        cursor.execute("INSERT into Players(name) values(%s)", (name, ))
        db.commit()
        db.close()
    else:
        return false

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("SELECT player_id, name , wins, played FROM result")
    val = cursor.fetchall()
    db.close()
    return val

def reportMatch(victor, defeated):
    """Records the result of a match between two players
      victor:  the id of the winner
      defeated:  the id of the loser
    """
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    cursor.execute("INSERT INTO Matches(victor, defeated) VALUES (%s,%s)", (victor,defeated))
    db.commit()
    db.close()




def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    """
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    positions = playerStandings()
    limit = int(countPlayers())
    pairings = []
    if (limit > 0): 
        for i in range (limit):
            if (i % 2 == 0):
                first_id = positions[i][0] 
                first_name = positions[i][1]
                second_id = positions[i + 1][0] 
                second_name = positions[i + 1][1]
                pair = (first_id, first_name, second_id, second_name)
                pairings.append(pair)
    return pairings


