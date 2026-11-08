import argparse
import json
import time
from datetime import datetime

import requests

DATE_FORMAT = "%d-%m-%Y %H_%M_%S"
API_URL = "https://proclubs.ea.com/api/fifa/clubs/info"
SAVE_EVERY = 100


def save_last_id(club_id):
    with open("last_id.txt", "w") as file:
        file.write(str(club_id))


def save_teams(teams):
    if not teams:
        return
    dt_string = datetime.now().strftime(DATE_FORMAT)
    with open(f"teams/teams_{dt_string}.txt", "w") as file:
        file.write(str(teams))


def scan(session, headers, platform, term, end_id, delay):
    with open("last_id.txt", "r") as file:
        club_id = int(file.read())

    found = []
    try:
        for club_id in range(club_id, end_id):
            response = session.get(
                API_URL,
                params={"platform": platform, "clubIds": club_id},
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            team = response.json().get(str(club_id))
            if team and term in team["name"].lower():
                print(f"Found team {club_id}: {team['name']}")
                found.append(club_id)
            if club_id % SAVE_EVERY == 0:
                print(f"Checked up to {club_id}")
                save_last_id(club_id)
            time.sleep(delay)
    finally:
        # Resume from the last id that was not confirmed as checked
        save_last_id(club_id)
        save_teams(found)


def main():
    parser = argparse.ArgumentParser(description="Busca clubes na API do EA Pro Clubs.")
    parser.add_argument("--term", default="rage", help="trecho do nome do clube")
    parser.add_argument("--platform", default="ps5")
    parser.add_argument("--end", type=int, default=10_000_000, help="último id (exclusivo)")
    parser.add_argument("--delay", type=float, default=0.2, help="segundos entre requisições")
    parser.add_argument("--max-tries", type=int, default=50)
    args = parser.parse_args()

    with open("headers.json", "r") as file:
        headers = json.load(file)
    session = requests.Session()

    for attempt in range(1, args.max_tries + 1):
        try:
            scan(session, headers, args.platform, args.term.lower(), args.end, args.delay)
            return
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error on try {attempt}: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
