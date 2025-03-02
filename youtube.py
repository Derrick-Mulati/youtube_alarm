import webbrowser
import time
import random
import logging
import os
import platform
from datetime import datetime, timedelta

# Import Windows volume control module
if platform.system() == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Configure logging
logging.basicConfig(filename='alarm_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# User-defined wake-up times (HH:MM format)
WAKE_UP_TIMES = ["07:00", "07:15", "07:30"]

# List of YouTube video URLs to play randomly
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=YQHsXMglC9A",
    "https://www.youtube.com/watch?v=fRh_vgS2dFE",
]

# Desired volume level (0.0 to 1.0)
VOLUME_LEVEL = 0.8

def set_system_volume(volume_level):
    """Set system volume based on OS."""
    try:
        if platform.system() == "Windows":
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(volume_level, None)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"osascript -e 'set volume output volume {int(volume_level * 100)}' ")
        elif platform.system() == "Linux":
            os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {int(volume_level * 100)}%")
        logging.info(f"System volume set to {int(volume_level * 100)}%.")
    except Exception as e:
        logging.error(f"Failed to set volume: {e}")

def wait_until(target_time):
    """Wait until the specified target time."""
    now = datetime.now()
    target_dt = datetime.strptime(target_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    if target_dt < now:
        target_dt += timedelta(days=1)
    remaining_time = (target_dt - now).total_seconds()
    logging.info(f"Waiting {int(remaining_time)} seconds until {target_time}...")
    time.sleep(remaining_time)

def play_video(url):
    """Open a YouTube video in the default web browser."""
    if not url:
        logging.error("No video URL provided.")
        return
    try:
        webbrowser.open(url)
        logging.info(f"Playing video: {url}")
    except Exception as e:
        logging.error(f"Error playing video: {e}")

def alarm_cycle():
    """Runs the alarm cycle for all scheduled wake-up times."""
    for wake_up_time in WAKE_UP_TIMES:
        print(f"Next alarm set for {wake_up_time}...")
        logging.info(f"Next alarm set for {wake_up_time}...")
        wait_until(wake_up_time)
        video_url = random.choice(VIDEO_URLS) if VIDEO_URLS else None
        set_system_volume(VOLUME_LEVEL)
        play_video(video_url)
        time.sleep(300)  # Wait 5 minutes before the next alarm

def main():
    logging.info("Alarm script started.")
    try:
        alarm_cycle()
    except KeyboardInterrupt:
        logging.info("Alarm script stopped by user.")
        print("Alarm script stopped.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info("Alarm script finished.")

if __name__ == "__main__":
    main()