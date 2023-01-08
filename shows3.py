'''
This program uses a REST API to search popular shows
Author: Kyle
'''
import requests

BASE_URL = "https://api.tvmaze.com/"

def get_shows(query: str) -> list[dict]:
    """
    Search for TV shows using the TV Maze API.
    If the show is not found, return None
    """
    response = requests.get(f'{BASE_URL}search/shows?q={query}')
    if response.status_code == 200:
        data = response.json()
        return data

def format_show_name(show: dict) -> str:
    """
    Format the show name.
    """
    information = [show["premiered"], show["ended"], ", ".join(show["genres"])]
    n_information = []
    
    for i in range(0, len(information)):
        if (information[i] == None) or (information[i] == ""):
            information[i] = "?"
        if information[i] == "?":
            n_information.append("?")
        elif i == 2:
            n_information.append(", ".join(show["genres"]))
        else:
            n_information.append(information[i][:4])
    
    information_string = f'({n_information[0]} - {n_information[1]}, {n_information[2]})'
    return information_string

def get_seasons(show_id: int) -> list[dict]:
    """
    Get the seasons for a given show_id
    """
    response = requests.get(f'{BASE_URL}shows/{show_id}/seasons')
    if response.status_code == 200:
        data = response.json()
        return data

def format_season_name(season: dict) -> str:
    """
    Format the season name
    """
    information = [season["premiereDate"], season["endDate"], season["episodeOrder"]]
    n_information = []

    for i in range(0, len(information)):
        if (information[i] == None) or (information[i] == ""):
            information[i] = "?"
        if information[i] == "?":
            n_information.append("?")
        elif i == 2:
            n_information.append(season["episodeOrder"])
        else:
            n_information.append(information[i][:4])

    information_string = f'({n_information[0]} - {n_information[1]}), {n_information[2]} episodes'
    return information_string    

def main():
    """
    Main function 
    """
    query = input("Search for a show: ")
    results = get_shows(query)
    if not results:
        print("No results found")
    else:
        n = 1
        print("Here are the results:")
        for result in results:
            show = result["show"]
            print(f"{n}. {show['name']} {format_show_name(show)}")
            n += 1

    number = (int(input("Select a show: ")) - 1)
    show_number = results[number]
    show_id = show_number["show"]["id"]
    season = get_seasons(show_id)
    if not season:
        print("No results found")
    else:
        count = 1
        print(f"Seasons of {show_number['show']['name']}:")
        for i in range(0, len(season)):
            print(f"{count}. Season {season[i]['number']} {format_season_name(season[i])}")
            count += 1

if __name__ == '__main__':
    main() 