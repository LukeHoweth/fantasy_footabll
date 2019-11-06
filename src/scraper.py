"""
This script will parse and scrape the same API that the Fantasy Premier League
website uses to receive its data. The player stats are then exported into a CSV
file, displayed in a table (as requested).
"""
import requests
import csv


def get_api_data():
    """
    1) Connects and pulls data from API.
    2) Creates a dictionary of players, where each value is another dictionary.
    3) Output -> { 'Player name' : {Player info} }
    """
    print('Data scrape: In Progress...')

    url = f'https://fantasy.premierleague.com/api/bootstrap-static/'        # This is the API link that the Fantasy
    live_data = requests.get(url=url).json()                                # Premier League website uses to recieve
    players_data = live_data['elements']                                    # the data shown on its website.
    player_list = {}

    for player in players_data:
        player_data = {
            'first'         :   player['first_name'],
            'last'          :   player['second_name'],
            'cost'          :   f"{str(player['now_cost'])[:-1]}.{str(player['now_cost'])[-1:]}",
            'position'      :   live_data['element_types'][player['element_type']-1]['singular_name'],
            'team'          :   live_data['teams'][player['team']-1]['name'],
            'selected by %' :   player['selected_by_percent'],
            'form'          :   player['form'],
            'pts'           :   player['total_points']
            }
        
        full_name = f"{player['first_name']} {player['second_name']}"       # Creates & assigns a new dictionary for
        player_list[f'{full_name}'] = player_data                           # every player. The outer dictionary is
    print('Data scape: Completed')                                          # then returned by the function.
    return player_list


def write_to_CSV(api_data):
    """
    1) Takes in the dictrionary returned by get_api_data() as an argument.
    2) Creates a new CSV file.
    3) Write the dictionary into the new CSV file called 'player_data.csv'.
       
       (NOTE - if you want to change the name of the created file, simply
       replace 'player_data.csv'. Be sure to inlude the '.csv' file extension.)
    """

    with open("player_data.csv", 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=['first', 'last', 'cost', 'position', 'team', 'selected by %', 'form', 'pts'])
        writer.writeheader()
        for player_name, player_info in api_data.items():                    
            writer.writerow((player_info))                                      
    print("Data exported to CSV.")


player_list = get_api_data()        # 1) The returned Dict is stored in a variable named 'player_list'.
write_to_CSV(player_list)           # 2) The variable 'player_list' is then exported to a CSV file
