"""
This program uses a REST API to search popular shows
Author: Kyle Chang
July 25 2023
"""

from tkinter import *

import requests

# PROGRAM FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BASE_URL = "https://api.tvmaze.com/"
QUERY = None
RESULTS = None
SEASON = None
SHOW_NUMBER = None


def get_shows(query: str) -> list[dict]:
    """Search for TV shows using the TV Maze API."""
    response = requests.get(f"{BASE_URL}search/shows?q={query}")
    if response.status_code == 200:
        data = response.json()
        return data


def format_show_name(show: dict) -> str:
    """Format the show name."""
    start = show["premiered"] or "?"
    end = show["ended"] or "?"
    genre = ", ".join(show["genres"]) or "?"

    information_string = f"({start} - {end}, {genre})"
    return information_string


def get_seasons(show_id: int) -> list[dict]:
    """Get the seasons for a given show_id"""
    response = requests.get(f"{BASE_URL}shows/{show_id}/seasons")
    if response.status_code == 200:
        data = response.json()
        return data


def format_season_name(season: dict) -> str:
    """Format the season name"""
    start = season["premiereDate"] or "?"
    end = season["endDate"] or "?"
    number_of_episodes = season["episodeOrder"] or "?"

    information_string = f"({start} - {end}), {number_of_episodes} episodes"
    return information_string


def get_episodes_of_season(season_id: int) -> list[dict]:
    """Get the episodes of a given season of a show"""
    response = requests.get(f"{BASE_URL}seasons/{season_id}/episodes")
    if response.status_code == 200:
        data = response.json()
        return data


def format_episode_name(episode: dict) -> str:
    """Format the episode name"""
    rating = episode["rating"]["average"] or "?"
    season = episode["season"] or "?"
    ep = episode["number"] or "?"

    information_string = f"S{season}E{ep} {episode['name']} (rating: {rating})"
    return information_string


# GUI FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def search_enter(event):
    """Searches for a show when <Enter> is pressed on the keyboard"""
    global QUERY
    global RESULTS
    show_text_box.delete("1.0", END)
    season_text_box.delete("1.0", END)
    episode_text_box.delete("1.0", END)
    QUERY = query_box.get()
    RESULTS = get_shows(QUERY)
    if not RESULTS:
        show_text_box.insert(END, "No results found")
    else:
        show_text_box.insert(END, "Here are the results:\n")
        n = 1
        for result in RESULTS:
            show = result["show"]
            display_show_text(show_text_box, show["name"], format_show_name(show), n)
            n += 1


def search_button():
    """Searches for a show when the search button is pressed"""
    global QUERY
    global RESULTS
    show_text_box.delete("1.0", END)
    season_text_box.delete("1.0", END)
    episode_text_box.delete("1.0", END)
    QUERY = query_box.get()
    RESULTS = get_shows(QUERY)
    if not RESULTS:
        show_text_box.insert(END, "No results found")
    else:
        show_text_box.insert(END, "Here are the results:\n")
        n = 1
        for result in RESULTS:
            show = result["show"]
            display_show_text(show_text_box, show["name"], format_show_name(show), n)
            n += 1


def display_show_text(text_box, show, info, index):
    """Helper function for displaying show information"""
    text_box.insert(END, f"{index}. {show} {info}\n")


def select_show_button():
    """Selects a show when the confirm button is pressed"""
    global SEASON
    global SHOW_NUMBER
    season_text_box.delete("1.0", END)
    episode_text_box.delete("1.0", END)
    try:
        show = int(show_selector.get()) - 1
        SHOW_NUMBER = RESULTS[show]
        show_id = SHOW_NUMBER["show"]["id"]
        SEASON = get_seasons(show_id)
        n = 1
        season_text_box.insert(END, f"Seasons of {SHOW_NUMBER['show']['name']}:\n")
        for i in range(0, len(SEASON)):
            display_season_text(
                season_text_box, SEASON[i]["number"], format_season_name(SEASON[i]), n
            )
            n += 1
    except:
        season_text_box.insert(END, "Please select a valid index value")


def display_season_text(text_box, season_number, info, index):
    """Helper function for displaying season information"""
    text_box.insert(END, f"{index}. Season {season_number} {info}\n")


def select_season_button():
    """Selects a season when the confirm button is pressed"""
    episode_text_box.delete("1.0", END)
    try:
        season = int(season_selector.get()) - 1
        season_number = SEASON[season]
        season_id = season_number["id"]
        episode = get_episodes_of_season(season_id)
        n = 1
        episode_text_box.insert(
            END, f"Episodes of {SHOW_NUMBER['show']['name']} S{season + 1}:\n"
        )
        for i in range(0, len(episode)):
            display_episode_text(episode_text_box, format_episode_name(episode[i]), n)
            n += 1
    except:
        episode_text_box.insert(END, "Please select a valid index value")


def display_episode_text(text_box, info, index):
    """Helper function for displaying episode information"""
    text_box.insert(END, f"{index}. {info}\n")


# GUI DISPLAY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# INITIALIZES THE GUI
window = Tk()
window.title("Show Finder")

frame = Frame(window)
frame.pack()

# ------------------------------------------------------------------

# CREATE THE SEARCH BOX FOR THE APPLICATION
search_box_frame = LabelFrame(frame)
search_box_frame.grid(row=0, column=0)

# CREATE THE LABEL AND SEARCHBOX
search_label = Label(search_box_frame, text="Search for a Show:")
search_label.grid(row=0, column=0)
query_box = Entry(search_box_frame, width=53, borderwidth=3)
query_box.grid(row=1, column=0, padx=9, pady=2, columnspan=1)

# CREATE THE SEARCH BUTTON
search_button = Button(search_box_frame, text="Search", command=search_button)
search_button.grid(row=1, column=1)
# OR PRESS ENTER
window.bind("<Return>", search_enter)

# ------------------------------------------------------------------

# CREATE THE SHOW RESULTS BOX FOR THE APPLICATION
show_results_frame = LabelFrame(frame, text="Show Results:")
show_results_frame.grid(row=1, column=0)

# CREATE TEXTBOX AND SCROLLBAR
show_scrollbar = Scrollbar(show_results_frame, orient="vertical")
show_scrollbar.pack(side=RIGHT, fill=Y)
show_text_box = Text(
    show_results_frame, width=80, height=20, yscrollcommand=show_scrollbar.set
)
show_text_box.pack(padx=2)
show_scrollbar.config(command=show_text_box.yview)

# ------------------------------------------------------------------

# CREATE THE SHOW SELECTOR SPINBOX
select_show_label = Label(frame, text="Select a Show:")
select_show_label.grid(row=2, column=0)
show_selector = Spinbox(frame, from_=1, to=100)
show_selector.grid(row=3, column=0)

show_confirm_button = Button(frame, text="Confirm", command=select_show_button)
show_confirm_button.grid(row=4, column=0)

# ------------------------------------------------------------------

# CREATE THE SEASON RESULTS BOX FOR THE APPLICATION
season_results_frame = LabelFrame(frame, text="Season Results:")
season_results_frame.grid(row=5, column=0)

# CREATE THE TEXTBOX AND SCROLLBAR
season_scrollbar = Scrollbar(season_results_frame, orient="vertical")
season_scrollbar.pack(side=RIGHT, fill=Y)
season_text_box = Text(
    season_results_frame, width=80, height=20, yscrollcommand=season_scrollbar.set
)
season_text_box.pack(padx=2)
season_scrollbar.config(command=season_text_box.yview)

# CREATE THE SEASON SELECTOR SPINBOX
select_season_label = Label(frame, text="Select a Season:")
select_season_label.grid(row=6, column=0)
season_selector = Spinbox(frame, from_=1, to=100)
season_selector.grid(row=7, column=0)

season_confirm_button = Button(frame, text="Confirm", command=select_season_button)
season_confirm_button.grid(row=8, column=0)

# ------------------------------------------------------------------

# CREATE THE EPISODE RESULTS BOX FOR THE APPLICATION
episode_results_frame = LabelFrame(frame, text="Episodes:")
episode_results_frame.grid(row=9, column=0)

# CREATE THE TEXTBOX AND SCROLL BAR
episode_scrollbar = Scrollbar(episode_results_frame, orient="vertical")
episode_scrollbar.pack(side=RIGHT, fill=Y)
episode_text_box = Text(
    episode_results_frame, width=80, height=20, yscrollcommand=episode_scrollbar.set
)
episode_text_box.pack(padx=2)
episode_scrollbar.config(command=episode_text_box.yview)

if __name__ == "__main__":
    window.mainloop()
