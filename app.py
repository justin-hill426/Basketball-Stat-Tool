import constants


def run_main():
    """Runs the main function for this project"""
    teams = balance_teams(clean_data(constants.PLAYERS), constants.TEAMS)
    start_stats_tool(teams)


def start_stats_tool(teams):
    """handle user input and functionality of the stats tool"""
    print("BASKETBALL TEAM STATS TOOL \n\n ---- MENU ---- \n")
    while True:
        for team in teams:
            print(team['team_name'])
        break
    # team_stats(teams['team_name'])


def team_stats(team):
    print(f"Team: {team['team_name']} Stats")
    print("----------------")


def clean_data(players):
    """Cleans the data to a more helpful format for displaying team stats"""
    player_list = []
    num_experienced_players = 0
    num_inexperienced_players = 0
    for player in players:
        player_stats = {
            'name': player['name'],
            'guardians': format_guardians(player['guardians']),
            'experience': has_experience(player['experience']),
            'height': parse_height(player['height'])
        }
        if player_stats['experience']:
            num_experienced_players += 1
        else:
            num_inexperienced_players += 1
        player_list.append(player_stats)
    return player_list, num_experienced_players, num_inexperienced_players


def balance_teams(player_tuple, teams):
    """balances the teams into three equally-sized teams"""
    player_data, experienced_players, inexperienced_players = player_tuple
    num_experienced_players_team = experienced_players / len(constants.TEAMS)
    num_inexperienced_players_team = inexperienced_players / len(constants.TEAMS)
    teams = []
    print(len(player_data))
    for team in constants.TEAMS:
        teams.append({
            'team_name': team,
            'team_players': generate_balanced_team_help(player_data, int(num_experienced_players_team),
                                                        int(num_inexperienced_players_team))
        })
    return teams


def generate_balanced_team_help(player_data, num_experienced_players_team, num_inexperienced_players_team):
    """helps to balance the teams - specifically by returning one team with the same number of experienced
    inexperienced players on each team
    """
    current_team = []
    experienced_players_on_team = 0
    inexperienced_players_on_team = 0
    print(len(player_data))
    for player in player_data.copy():
        if len(current_team) == int(num_experienced_players_team + num_inexperienced_players_team):
            break
        else:
            if player['experience'] and experienced_players_on_team < 3:
                current_team.append(player)
                experienced_players_on_team += 1
                player_data.remove(player)
            elif not player['experience'] and inexperienced_players_on_team < 3:
                current_team.append(player)
                inexperienced_players_on_team += 1
                player_data.remove(player)
    return current_team


def has_experience(experience_string):
    "returns whether the current player has experience or not based on the string yes/no"
    if experience_string == 'YES':
        return True
    else:
        return False


def format_guardians(guardian_string):
    """returns a list of guardians split using the keyword ' and ' """
    return guardian_string.split(' and ')


def parse_height(height_string):
    """parses the height - first two characters of the players height string"""
    return int(height_string[0:2])


if __name__ == "__main__":
    run_main()
