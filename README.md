# bookit
Read ebooks one word at a time for better focus, retention, and speed.

# Installation

- Install Python 3.10 if you haven't already. You can download it from the official Python website: https://www.python.org/downloads/
- Create a virtual environment for the project:
  ```
  python -m venv venv
  ```
- Activate the virtual environment:
  - On Windows: 
  ```
  venv\Scripts\activate
  ```
  - On macOS and Linux: 
  ```
  source venv/bin/activate
  ```
- Install the required packages using the requirements.txt file: 
  ```
  pip install -r requirements.txt
  ```
  - For macOS users, you might need to install Tcl/Tk to run the Tkinter GUI. You can use Homebrew to install it: 
  ```
  brew install tcl-tk
  ```
  - If you are using WSL (Windows Subsystem for Linux) or running the script on a Linux machine without a graphical interface, you will need to install an X server on your Windows machine. One popular option is VcXsrv. Download and install VcXsrv, and then start it with the "XLaunch" shortcut.
  - For WSL users, you need to set the DISPLAY environment variable to connect the script to VcXsrv. Run this command in the WSL terminal before starting the script:
  ```
  echo "export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0" >> ~/.bashrc
  source ~/.bashrc
  ```
- Run the script with:
  ```
  python reader.py
  ```

# Using the App
- When prompted, navigate to your saved epub file and open it
- The segments of the book will appear as selectable chapters.  Titles come from the file references, so they are usually only partial.
- The Words Per Minute and Syllables Per Minute sliders allow you to control the playback speed, with the syllables variation taking into account the additional time it may take to read longer or more complicated words.  Set your desired speed and choose the appropriate radio button to match
- Click on a chapter and it will open in a new window, immediately playing back the text in a stream at the speed you've selected.  The system will close the window when the chapter has concluded or you can close it at any time and select a different chapter.

# Known Bugs
- Formatting: text is simple, and there are some formatting issues for start-of-chapter variations that may be able to be handled
- `invalid command name` notices while running for an unexpected variation on the call to update_word

# Intended Improvements
- Play/Pause/Stop/Go-back-X-Words menu
- Cleaner interface
  - Font choices
  - Light/Dark Mode
  - Single-window application
- Bookmarks
- Intelligent pauses in playback (paragraph breaks, commas, etc)
- Portable version(s)
