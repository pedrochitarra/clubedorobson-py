# TODO: Start the classes with minimum information and create methods to
# populate the rest of the information to avoid many arguments in the
# constructor.

# class Club:
#     def __init__(self, club_id, name, region_id, team_id, created_at,
#                  updated_at, stadium, is_custom, standard_crest_id,
#                  custom_crest_id, kit_color_1, kit_color_2, kit_color_3,
#                  kitacolor1, kitacolor2, kitacolor3) -> None:
#         pass

# class Match:
#     def __init__(self, match_id, timestamp, home_team: Club, away_team: Club,
#                  home_goals, away_goals, created_at, updated_at) -> None:
#         pass

# class Player:
#     def __init__(self, name, games_played, win_rate, goals, assists,
#                  clean_sheets_def, clean_sheets_gk, shot_success_rate,
#                  passes_made, pass_success_rate, pro_name, pro_position,
#                  pro_style, pro_height, pro_nationality, pro_overall,
#                  man_of_the_match, red_cards, favorite_position,
#                  created_at, updated_at, club: Club) -> None:
#         pass

# class ClubMatch(Club, Match):
#     def team_info()

class Club:
    def __init__(self, club_id, club_name, is_custom_team,
                 crest_id, stad_name, standard_crest_id,
                 kit_colors) -> None:
        self.club_id = club_id
        self.club_name = club_name
        self.is_custom_team = is_custom_team
        self.crest_id = crest_id
        self.stad_name = stad_name
        self.standard_crest_id = standard_crest_id
        self.kit_colors = kit_colors

class Match():
    def __init__(self, home_club: Club, away_club: Club) -> None:
        self.home_club = home_club
        self.away_club = away_club