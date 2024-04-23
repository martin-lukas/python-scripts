#!/Users/martin/code/python/venv/bin/python
import os
import signal
import subprocess
import sys

# Setup
# 1. Make pomo.py executable: chmod +x pomo.py
# 2. Create a symbolic link: cd ~/.bin ; ln -s ~/code/mac-scripts/pomo.py pomo
# 3. Add ~/.bin to your PATH: export PATH="$PATH:$HOME/.bin"


GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_welcome(minutes):
    print(GREEN + "The screen will lock in " + str(minutes) + " minutes. " +
          "Press CTRL+C to cancel." + RESET)


def start_wait(minutes):
    return subprocess.Popen(["sleep", str(minutes * 60)], preexec_fn=os.setsid)


def handle_interrupt():
    print(YELLOW + "Interrupting the planned screen lock..." + RESET)
    os.killpg(os.getpgid(wait_x_minutes.pid), signal.SIGTERM)
    sys.exit(1)


def lock_screen():
    subprocess.run([
        "osascript", "-e",
        'tell application "System Events" to tell process "SystemUIServer" ' +
        'to keystroke "q" using {control down, command down}'
    ])
    subprocess.run(["open", "-a", "ScreenSaverEngine"])


try:
    if len(sys.argv) < 2:
        print("Please provide a delay time in minutes.")
        sys.exit(1)
    minutes = int(sys.argv[1])
    signal.signal(signal.SIGINT, lambda signal, frame: handle_interrupt())
    wait_x_minutes = start_wait(minutes)
    print_welcome(minutes)
    wait_x_minutes.wait()
    lock_screen()
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
