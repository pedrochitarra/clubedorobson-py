CREATE TABLE ClubesPartidas (
    "clubMatchId" TEXT NOT NULL,
    "clubId" INTEGER NOT NULL,
    "matchId" TEXT NOT NULL,
    passattempts INTEGER NOT NULL,
    passesmade INTEGER NOT NULL,
    rating TEXT NOT NULL,
    shots INTEGER NOT NULL,
    goals INTEGER NOT NULL,
    goalsConceded INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    tackleattempts INTEGER NOT NULL,
    tacklesmade INTEGER NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    seasonid INTEGER
);