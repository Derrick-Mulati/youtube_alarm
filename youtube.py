import webbrowser
import time
import random
from datetime import datetime, timedelta
import logging
import os
import platform
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Configure logging
logging.basicConfig(filename='alarm_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set multiple wake-up times (24-hour format: HH:MM)
WAKE_UP_TIMES = ["07:00", "07:15", "07:30"]  # Add or modify as needed

# List of YouTube video URLs to play randomly
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=YQHsXMglC9A",
    "https://www.youtube.com/watch?v=fRh_vgS2dFE",
    # Add more URLs as needed
]

# Set the desired volume level (0.0 to 1.0)
VOLUME_LEVEL = 0.8  # 80% volume

def set_system_volume(volume_level):
    """Set the system volume using pycaw (Windows only)."""
    if platform.system() != "Windows":
        logging.warning("Volume control is only supported on Windows.")
        return

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level, None)
    logging.info(f"System volume set to {int(volume_level * 100)}%.")

def wait_until(target_time):
    """Wait until the specified target time."""
    target_dt = datetime.strptime(target_time, "%H:%M").replace(
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day
    )
    
    # If the target time has passed for today, schedule it for tomorrow
    if target_dt < datetime.now():
        target_dt += timedelta(days=1)

    while True:
        now = datetime.now()
        remaining_time = (target_dt - now).total_seconds()
        
        if remaining_time <= 0:
            break
        
        # Sleep for a shorter duration as the target time approaches
        sleep_interval = min(remaining_time, 30)
        logging.info(f"Waiting... {int(remaining_time)} seconds remaining.")
        time.sleep(sleep_interval)

def play_video(url):
    """Open the specified YouTube video in the default web browser."""
    try:
        webbrowser.open(url)
        logging.info(f"YouTube video opened successfully: {url}")
    except Exception as e:
        logging.error(f"Failed to open video: {e}")

def main():
    logging.info("Alarm script started.")
    try:
        for wake_up_time in WAKE_UP_TIMES:
            print(f"Waiting until {wake_up_time}...")
            logging.info(f"Waiting until {wake_up_time}...")
            wait_until(wake_up_time)
            
            # Select a random video from the list
            video_url = random.choice(VIDEO_URLS)
            print(f"It's time! Opening YouTube video: {video_url}")
            logging.info(f"It's time! Opening YouTube video: {video_url}")
            
            # Set system volume
            set_system_volume(VOLUME_LEVEL)
            
            # Play the video
            play_video(video_url)
            
            # Wait for a few minutes before the next alarm
            time.sleep(300)  # 5 minutes delay between alarms

    except KeyboardInterrupt:
        print("\nAlarm script stopped by user.")
        logging.info("Alarm script stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Alarm script finished.")

if __name__ == "__main__":
    main()