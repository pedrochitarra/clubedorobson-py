"""Create a database to emulate the original data. We do this here to show
how the scrapping works, since the original data is from 2021."""
import sqlite3
import os

def main():
    """Read the documentation to understand each table and its columns.
    The database is documented in a diagram, the API in a Swagger file and
    the data in a Notion page."""
    database_file = "data/raw/mock.db"
    # Delete file if exists
    if os.path.exists(database_file):
        os.remove(database_file)
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    # Clubs table =============================================================
    create_clubs_query = """
        CREATE TABLE Clubs (
            clubId INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            regionId TEXT NOT NULL,
            teamId TEXT NOT NULL,
            stadName TEXT,
            kitId TEXT,
            isCustomTeam TEXT,
            customKitId TEXT,
            customAwayKitId TEXT,
            customKeeperKitId TEXT,
            kitColor1 TEXT,
            kitColor2 TEXT,
            kitColor3 TEXT,
            kitColor4 TEXT,
            kitAColor1 TEXT,
            kitAColor2 TEXT,
            kitAColor3 TEXT,
            kitAColor4 TEXT,
            dCustomKit TEXT,
            crestColor TEXT,
            crestAssetId TEXT
        );
    """
    cursor.execute(create_clubs_query)

    # Players table ===========================================================
    create_players_query = """
        CREATE TABLE Players (
            name TEXT PRIMARY KEY,
            gamesPlayed TEXT,
            winRate TEXT,
            goals TEXT,
            assists TEXT,
            cleanSheetsDef TEXT,
            cleanSheetsGK TEXT,
            shotSuccessRate TEXT,
            passesMade TEXT,
            passSuccessRate TEXT,
            tacklesMade TEXT,
            tackleSuccessRate TEXT,
            proName TEXT,
            proPos TEXT,
            proStyle TEXT,
            proHeight TEXT,
            proNationality TEXT,
            proOverall TEXT,
            manOfTheMatch TEXT,
            redCards TEXT,
            prevGoals TEXT,
            favoritePosition TEXT,
            clubId TEXT,
            FOREIGN KEY (clubId) REFERENCES Clubs (clubId)
        );
    """
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute(create_players_query)

    # Matches table ===========================================================
    create_matches_query = """
        CREATE TABLE Matches (
            matchId TEXT PRIMARY KEY,
            timestamp TEXT
        );
    """
    cursor.execute(create_matches_query)

    # ClubsMatches table ======================================================
    # Information about each club in each match
    create_clubs_matches_query = """
        CREATE TABLE ClubsMatches (
            clubId TEXT,
            matchId TEXT,
            gameNumber TEXT,
            goals TEXT,
            goalsAgainst TEXT,
            losses TEXT,
            result TEXT,
            score TEXT,
            season_id TEXT,
            TEAM TEXT,
            ties TEXT,
            winnerByDnf TEXT,
            wins TEXT,
            PRIMARY KEY (clubId, matchId),
            FOREIGN KEY (clubId) REFERENCES Clubs (clubId),
            FOREIGN KEY (matchId) REFERENCES Matches (matchId)
        );
    """
    cursor.execute(create_clubs_matches_query)

    # PlayersMatches table ====================================================
    # Information about each player in each match
    players_matches_query = """
        CREATE TABLE PlayersMatches (
            playerId TEXT,
            assists TEXT,
            cleansheetsany TEXT,
            cleansheetsdef TEXT,
            cleansheetsgk TEXT,
            goals TEXT,
            goalsconceded TEXT,
            losses TEXT,
            mom TEXT,
            namespace TEXT,
            passattempts TEXT,
            passesmade TEXT,
            pos TEXT,
            rating TEXT,
            realtimegame TEXT,
            realtimeidle TEXT,
            redcards TEXT,
            saves TEXT,
            SCORE TEXT,
            shots TEXT,
            tackleattempts TEXT,
            tacklesmade TEXT,
            vproattr TEXT,
            vprohackreason TEXT,
            wins TEXT,
            playername TEXT,
            matchId TEXT,
            clubId TEXT,
            PRIMARY KEY (playername, matchId, clubId),
            FOREIGN KEY (playername) REFERENCES Players (name),
            FOREIGN KEY (matchId) REFERENCES Matches (matchId),
            FOREIGN KEY (clubId) REFERENCES Clubs (clubId)
        );
    """
    cursor.execute(players_matches_query)

    # ClubsMatchesAgg table ===================================================
    # Aggregated information about each club in each match
    create_clubs_matches_agg_query = """
        CREATE TABLE ClubsMatchesAgg (
            clubId TEXT,
            matchId TEXT,
            assists TEXT,
            cleansheetsany TEXT,
            cleansheetsdef TEXT,
            cleansheetsgk TEXT,
            goals TEXT,
            goalsconceded TEXT,
            losses TEXT,
            mom TEXT,
            namespace TEXT,
            passattempts TEXT,
            passesmade TEXT,
            pos TEXT,
            rating TEXT,
            realtimegame TEXT,
            realtimeidle TEXT,
            redcards TEXT,
            saves TEXT,
            SCORE TEXT,
            shots TEXT,
            tackleattempts TEXT,
            tacklesmade TEXT,
            vproattr TEXT,
            vprohackreason TEXT,
            wins TEXT,
            PRIMARY KEY (clubId, matchId),
            FOREIGN KEY (clubId) REFERENCES Clubs (clubId),
            FOREIGN KEY (matchId) REFERENCES Matches (matchId)
        );
    """
    cursor.execute(create_clubs_matches_agg_query)

    # Seasonals table ===================================================
    # Aggregated information about each club in seasons
    create_seasonals_query = """
        CREATE TABLE Seasonals (
            clubId TEXT PRIMARY KEY,
            seasons TEXT,
            titlesWon TEXT,
            leaguesWon TEXT,
            divsWon1 TEXT,
            divsWon2 TEXT,
            divsWon3 TEXT,
            divsWon4 TEXT,
            cupsWon0 TEXT,
            cupsWon1 TEXT,
            cupsWon2 TEXT,
            cupsWon3 TEXT,
            cupsWon4 TEXT,
            cupsWon5 TEXT,
            cupsWon6 TEXT,
            cupsElim0 TEXT,
            cupsElim0R1 TEXT,
            cupsElim0R2 TEXT,
            cupsElim0R3 TEXT,
            cupsElim0R4 TEXT,
            cupsElim1 TEXT,
            cupsElim1R1 TEXT,
            cupsElim1R2 TEXT,
            cupsElim1R3 TEXT,
            cupsElim1R4 TEXT,
            cupsElim2 TEXT,
            cupsElim2R1 TEXT,
            cupsElim2R2 TEXT,
            cupsElim2R3 TEXT,
            cupsElim2R4 TEXT,
            cupsElim3 TEXT,
            cupsElim3R1 TEXT,
            cupsElim3R2 TEXT,
            cupsElim3R3 TEXT,
            cupsElim3R4 TEXT,
            cupsElim4 TEXT,
            cupsElim4R1 TEXT,
            cupsElim4R2 TEXT,
            cupsElim4R3 TEXT,
            cupsElim4R4 TEXT,
            cupsElim5 TEXT,
            cupsElim5R1 TEXT,
            cupsElim5R2 TEXT,
            cupsElim5R3 TEXT,
            cupsElim5R4 TEXT,
            cupsElim6 TEXT,
            cupsElim6R1 TEXT,
            cupsElim6R2 TEXT,
            cupsElim6R3 TEXT,
            cupsElim6R4 TEXT,
            promotions TEXT,
            holds TEXT,
            relegations TEXT,
            rankingPoints TEXT,
            prevDivision TEXT,
            maxDivision TEXT,
            bestDivision TEXT,
            bestPoints TEXT,
            curSeasonMov TEXT,
            lastMatch0 TEXT,
            lastMatch1 TEXT,
            lastMatch2 TEXT,
            lastMatch3 TEXT,
            lastMatch4 TEXT,
            lastMatch5 TEXT,
            lastMatch6 TEXT,
            lastMatch7 TEXT,
            lastMatch8 TEXT,
            lastMatch9 TEXT,
            lastOpponent0 TEXT,
            lastOpponent1 TEXT,
            lastOpponent2 TEXT,
            lastOpponent3 TEXT,
            lastOpponent4 TEXT,
            lastOpponent5 TEXT,
            lastOpponent6 TEXT,
            lastOpponent7 TEXT,
            lastOpponent8 TEXT,
            lastOpponent9 TEXT,
            starLevel TEXT,
            cupRankingPoints TEXT,
            overallRankingPoints TEXT,
            alltimeGoals TEXT,
            alltimeGoalsAgainst TEXT,
            seasonWins TEXT,
            seasonTies TEXT,
            seasonLosses TEXT,
            gamesPlayed TEXT,
            goals TEXT,
            goalsAgainst TEXT,
            points TEXT,
            prevSeasonWins TEXT,
            prevSeasonTies TEXT,
            prevSeasonLosses TEXT,
            prevPoints TEXT,
            prevProjectedPts TEXT,
            skill TEXT,
            wins TEXT,
            ties TEXT,
            losses TEXT,
            currentDivision TEXT,
            projectedPoints TEXT,
            totalCupsWon TEXT,
            recentResults TEXT,
            totalGames TEXT,
            FOREIGN KEY (clubId) REFERENCES Clubs (clubId)
        );
    """
    cursor.execute(create_seasonals_query)


if __name__ == '__main__':
    main()
