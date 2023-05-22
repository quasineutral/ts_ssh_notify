import json
import os
import requests
import time
from base64 import b64decode
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TAILSCALE_STATEFILE = "/data/state/tailscaled.state"
RECORDINGS_DIR = "/data/recordings"


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # only process files, in a subdirectory, that end in .cast
        if event.is_directory or not event.src_path.count("/") == 4 or not event.src_path.endswith(".cast"):
            return
        print(f"New file created: {event.src_path}")
        # Sleep for a moment so text is written to file
        time.sleep(0.5)
        # Read first line of file, this contains a JSON object with the details of the SSH login
        try:
            with open(event.src_path, "r") as f:
                first_line = f.readline()
            jd = json.loads(first_line)
        except Exception as e:
            print(e)
            return
        # Generate an Url from the filename and the tailscale machine name
        idname = "/".join(event.src_path.split("/")[-2:])
        url = f"https://{machine_name}/view?id={idname}"
        print(url)
        print(jd)
        # TODO: Add nicer formatting to the payload
        payload = (
            f"[{jd['dstNode']}] New SSH login as {jd['sshUser']} from {jd['srcNode']} by {jd['srcNodeUser']}\n{url}"
        )
        try:
            requests.post(DISCORD_WEBHOOK_URL, data={"content": payload})
        except Exception as e:
            print(e)
            return


def get_machine_name(statefile):
    # Try to get the machine name from the tailscale statefile
    try:
        with open(statefile, "r") as f:
            tailscalestate = json.load(f)
        # convert from base64 and extract machine name
        current_profile = b64decode(tailscalestate["_current-profile"]).decode("utf-8")
        profiles = b64decode(tailscalestate["_profiles"]).decode("utf-8")
        profiles = json.loads(profiles)
        profile = current_profile.split("-", 1)[1]
        machine_name = profiles[profile]["Name"]
        return machine_name
    except Exception as e:
        return False


if __name__ == "__main__":
    # Wait until tailscale state file is initialised
    # Get machine name from tailscale state file
    print("Finding tailsacle machine name..")
    while not (machine_name := get_machine_name(TAILSCALE_STATEFILE)):
        time.sleep(1)
    print(f"Machine name: {machine_name}")

    # Check if webhook url is set
    if DISCORD_WEBHOOK_URL is None:
        raise Exception("DISCORD_WEBHOOK_URL environmental variable is not set")

    # Create observer to monitor for file changes
    observer = Observer()
    event_handler = NewFileHandler()
    observer.schedule(event_handler, RECORDINGS_DIR, recursive=True)
    observer.start()
    print("Ready, waiting for incoming ssh sessions...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
