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
    start = show["premiered"] or "?"
    end = show["ended"] or "?"
    genre = ", ".join(show["genres"]) or "?"
    
    information_string = f'({start} - {end}, {genre})'
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
    start = season["premiereDate"] or "?"
    end = season["endDate"] or "?"
    number_of_episodes = season["episodeOrder"] or "?"

    information_string = f'({start} - {end}), {number_of_episodes} episodes'
    return information_string    

def get_episodes_of_season(season_id: int) -> list[dict]:
    """
    Get the episodes of a given season of a show
    season_id is the id (not the number!) of the season
    """
    response = requests.get(f"{BASE_URL}seasons/{season_id}/episodes")
    if response.status_code == 200:
        data = response.json()
        return data

def format_episode_name(episode: dict) -> str:
    """
    Format the episode name
    """
    rating = episode['rating']["average"] or "?"
    season = episode["season"] or "?"
    ep = episode["number"] or "?"
    
    information_string = f"S{season}E{ep} {episode['name']} (rating: {rating})"
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

    number1 = (int(input("Select a show: ")) - 1)
    show_number = results[number1]
    show_id = show_number["show"]["id"]
    season = get_seasons(show_id)
    x = 1
    print(f"Seasons of {show_number['show']['name']}:")
    for i in range(0, len(season)):
        print(f"{x}. Season {season[i]['number']} {format_season_name(season[i])}")
        x += 1

    number2 = (int(input("Select a season: ")) - 1)
    season_number = season[number2]
    season_id = season_number['id']
    episode = get_episodes_of_season(season_id)
    y = 1
    print(f"Episodes of {show_number['show']['name']} S{number2 + 1}:")
    for index in range(0, len(episode)):
        print(f"{y}. {format_episode_name(episode[index])}")
        y += 1

if __name__ == '__main__':
    main() 