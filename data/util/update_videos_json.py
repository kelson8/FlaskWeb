import json
import os

from generate_video_id import generate_youtube_video_id

# This is a script that can modify the ../json/videos.json file, adds new content into ../json/new_videos.json

videos_json_file = os.path.join('..', 'json', 'videos.json')
# For now, this script saves to a new file until I'm ready to use this
new_videos_json_file = os.path.join('..', 'json', 'new_videos.json')
# new_videos_json_file = 'json/new_videos.json'

# TODO Setup this to automatically generate a json with:
#  random video id, set title, description, video filename, and lastly if it is restricted or not.
# Currently this write_video_to_json function below doesn't seem to work and most likely needs fixed.

# TODO Fix this to work.
def write_video_to_json(video_data, json_file):
    """
        Write video data to json file, with random generated ID below.
    """
    try:
        with open(json_file, 'r') as f:
            existing_videos = json.load(f)

    except FileNotFoundError:
        print('Video data file not found.')
        existing_videos = {}
    except json.JSONDecodeError:
        print('Video data file not valid JSON.')
        existing_videos = {}

        # Add the new video data
        existing_videos[video_data['id']] = {
            'title': video_data['title'],
            'description': video_data['description'],
            'file': video_data['file'],
            'restricted': video_data.get('restricted', False)  # Default to False if not provided
        }

        # Write updated data back to the JSON file
        with open(json_file, 'w') as fjson:
            json.dump(existing_videos, fjson, indent=4)
            print(f"Wrote to {json_file}")

# TODO Set this up, generate random video IDs to add into videos.json
video_id_random = generate_youtube_video_id()  # Generate the random ID

video_data_new = {
    'title': 'Sample Video',
    'description': 'This is a sample video.',
    'file': 'sample_video.mp4',
    'restricted': False  # Example status
}

# videos[video_id] = video_data  # Assume videos is a dictionary storing your video data

# Write to the JSON file
# TODO Fix to work later.
# print(video_data_new)
# write_video_to_json(video_data_new, new_videos_json_file)

######

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
# if os.path.exists(videos_json_file):
#     with open(videos_json_file, 'r') as file:
#         data = json.load(file)
#         # Adding a new entry to videos.json
#         new_id = "2"
#         add_entry(data, new_id, "ReVC Spinning Cars", "I coded this function using C++ to mess around with, the game crashes at the end.",
#                   "ReVC-SpinningCars.mp4",
#                   False)
#
#         # Use this to remove values from the videos.json
#         # remove_entry(data, "2")  # Removes the entry with ID "2"
#
#         # Save the modified JSON back to the file
#         # with open('data.json', 'w') as file:
#         with open(new_videos_json_file, 'w') as file:
#             json.dump(data, file, indent=4)
# else:
#     print("The file {} does not exist.".format(videos_json_file))

