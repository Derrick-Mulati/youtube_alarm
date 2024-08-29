import webbrowser
import time
from datetime import datetime

# Set the time you want to wake up (8 AM)
wake_up_time = "07:04"

# URL of the YouTube video you want to play
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your desired video URL

def wait_until(target_time):
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == target_time:
            break
        time.sleep(30)  # Check every 30 seconds

def play_video(url):
    webbrowser.open(url)

if __name__ == "__main__":
    print(f"Waiting until {wake_up_time}...")
    wait_until(wake_up_time)
    print("It's time! Opening YouTube video...")
    play_video(video_url)
