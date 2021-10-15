import constants


def run_main():
    """Runs the main function for this project"""
    teams = balance_teams(clean_data(constants.PLAYERS), constants.TEAMS)
    start_stats_tool(teams)


def start_stats_tool(teams):
    """handle user input and functionality of the stats tool"""
    print("\nBASKETBALL TEAM STATS TOOL \n")
    while True:
        try:
            print_menu()
            next_choice = get_user_input()
            if next_choice == 'a':
                print_team_choices(teams)
                team_stats(teams[letter_parser(get_user_input(), len(teams))])
                if input("Press ENTER to continue... \n"):
                    continue
            elif next_choice == 'b':
                print("Thanks for checking out the team stats! Have a nice day!!!")
                break
            else:
                raise ValueError('Try Again! Please enter a valid choice (a/b)')
        except ValueError as err:
            print(err)


def print_menu():
    """Prints the main menu for the stat tool"""
    print("---- MENU ---- \n")
    print("Here are your choices: \n a) Display Team Stats \n b) Quit")


def get_user_input():
    """Gets the user input with predefined string"""
    user_input = input('\nEnter an option: ')
    return user_input.lower()


def letter_parser(input_letter, num_teams):
    """Parses the letter input into an int a-0, b-1, c-2..."""
    if len(input_letter) != 1 or type(input_letter) != str:
        raise ValueError('Try Again! Make sure to enter a one letter alphanumeric character')
    value = ord(input_letter) - ord('a')
    if value < 0 or value > num_teams - 1:
        raise ValueError('Try Again! Please enter a character option for a valid team')
    else:
        return value


def print_team_choices(teams):
    """Prints the team choices available"""
    print("\nHere are the teams to choose from: ")
    for i in range(len(teams)):
        print(f" {chr(i + ord('a'))}) {teams[i]['team_name']}")


def player_join(team):
    """Returns a string of all of the players on the team joined together"""
    player_names = []
    players = team['team_players']
    players.sort(key=lambda p: p['height'])
    for player in players:
        player_names.append(player['name'])
    player_string = ", "
    player_string = player_string.join(player_names)
    return player_string


def guardian_join(team):
    """Returns a string of all of the parent guardians on the team joined together"""
    guardian_names = []
    for player in team['team_players']:
        guardian_names.extend(player['guardians'])
    guardian_string = ", "
    guardian_string = guardian_string.join(guardian_names)
    return guardian_string


def experience_counter(current_team):
    """Counts the number of experienced/non-experienced players"""
    experienced_players = 0
    inexperienced_players = 0
    for player in current_team['team_players']:
        if player['experience']:
            experienced_players += 1
        else:
            inexperienced_players += 1
    return experienced_players, inexperienced_players


def average_height(team, num_team_players):
    """Calculates the average height(inches) for the team"""
    team_total_height = 0
    for player in team['team_players']:
        team_total_height += player['height']
    return round(team_total_height / num_team_players, 1)


def team_stats(team):
    """Prints out the stats for a particular team"""
    print(f"Team: {team['team_name']} Stats")
    print("----------------")
    total_players = len(team['team_players'])
    print(f"Total players: {total_players}")
    experienced_players, inexperienced_players = experience_counter(team)
    print(f"Total experienced: {experienced_players}")
    print(f"Total inexperienced: {inexperienced_players}")
    print(f"Average height: {average_height(team, total_players)} inches")
    print(f"\nPlayers on Team:\n  {player_join(team)}")
    print(f"\nGuardians:\n  {guardian_join(team)} \n")


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
    """returns whether the current player has experience or not based on the string yes/no"""
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
