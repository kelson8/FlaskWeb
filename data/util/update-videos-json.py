import json
import os

# This is a script that can modify the ../json/videos.json file, adds new content into ../json/new_videos.json

videos_json_file = os.path.join('..', 'json', 'videos.json')
# For now, this script saves to a new file until I'm ready to use this
new_videos_json_file = os.path.join('..', 'json', 'new_videos.json')

def add_entry(data, new_id, title, description, file, restricted):
    data[new_id] = {
        "title": title,
        "description": description,
        "file": file,
        "restricted": restricted
    }

# Remove values from json file
def remove_entry(data, entry_id):
    if entry_id in data:
        del data[entry_id]

# Load the existing JSON data from a file, first check if the file exists
if os.path.exists(videos_json_file):
    with open(videos_json_file, 'r') as file:
        data = json.load(file)
        # Adding a new entry to videos.json
        new_id = "2"
        add_entry(data, new_id, "ReVC Spinning Cars", "I coded this function using C++ to mess around with, the game crashes at the end.",
                  "ReVC-SpinningCars.mp4",
                  False)

        # Use this to remove values from the videos.json
        # remove_entry(data, "2")  # Removes the entry with ID "2"

        # Save the modified JSON back to the file
        # with open('data.json', 'w') as file:
        with open(new_videos_json_file, 'w') as file:
            json.dump(data, file, indent=4)
else:
    print("The file {} does not exist.".format(videos_json_file))

