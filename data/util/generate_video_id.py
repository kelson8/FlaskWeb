import random
import string

def generate_youtube_video_id(length=11):
    characters = string.ascii_letters + string.digits
    video_id = ''.join(random.choice(characters) for _ in range(length))
    return video_id

# Set the amount of videos to generate here
videos_to_generate = 10

for i in list(range(videos_to_generate)):
    video_id = generate_youtube_video_id()
    print(video_id)
