# Music Match Headphones

A Python application that recommends headphones based on user music preferences using Spotify audio features.

## Team Members
- Haihan Zhang
- Anish Suresh Saini

## Project Description

Music Match Headphones analyzes a user's music taste (genre preferences, audio features like energy and tempo) and recommends suitable headphones based on their listening habits and use case (workout, casual listening, or studio work).

## Features

### Current Features 
- **Data Management**: Loads and stores 33,000+ Spotify songs with audio features
- **Genre Selection**: Dropdown menu to select favorite music genre
- **Use Case Selection**: Radio buttons for workout, casual, or studio use
- **Recommendations**: Basic algorithm that matches headphones to music preferences
- **Song Browser**: View and filter all songs by genre
- **Interactive GUI**: User-friendly graphical interface built with tkinter

### Planned Features 
- Advanced recommendation algorithm (Tree Model).
- Improving Model accuracy.
- User profile creation and preference saving
- Price range filtering
- Detailed headphone comparisons
- GUI Improvements

---

##  How to Get Started

Choose the method that works best for you (arranged from easiest to most advanced):

###  Option 1: Download and Run (Simplest - *Recommended*)

**Step 1: Download Python**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.12 or newer
3. **IMPORTANT**: During installation, check the box that says "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete

**Step 2: Download the Project**
1. Click the green "Code" button at the top of this page
2. Click "Download ZIP"
3. Extract the ZIP file to a folder on your computer (e.g., Desktop or Documents)
4. Remember where you saved it!

**Step 3: Install Required Packages**
1. **Windows Users:**
   - Press `Windows Key`
   - Type `cmd` and press Enter
   - Type: `cd Desktop\music-match-headphones` (replace with your folder location)
   - Type: `pip install -r requirements.txt`
   - Press Enter and wait

2. **Mac Users:**
   - Press `Command + Space`
   - Type "Terminal" and press Enter
   - Type: `cd Desktop/music-match-headphones` (replace with your folder location)
   - Type: `pip install -r requirements.txt`
   - Press Enter and wait

**Step 4: Run the Program**
- In the same command window/terminal, type: `python main.py`
- Press Enter
- The application window should open!

**Troubleshooting:**
- If you get "python is not recognized": Reinstall Python and make sure to check "Add Python to PATH"
- If you get "No module named pandas": Run `pip install pandas pytest` manually
- If files are not found: Make sure you're in the correct folder (use `cd` command to navigate)

---

### Option 2: Using PyCharm

**Step 1: Install PyCharm**
1. Download PyCharm Community Edition (FREE) from [jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/)
2. Install PyCharm following the installation wizard
3. Open PyCharm

**Step 2: Get the Project**

**Download ZIP**
1. Download the ZIP file (see Option 1, Step 2)
2. Extract it
3. In PyCharm, click `Open`
4. Navigate to the extracted folder
5. Click `OK`

**Step 3: Install Packages**
1. PyCharm will show a notification about missing packages
2. Click "Install requirements" in the notification
3. OR: Open `requirements.txt`, and click the "Install all" banner at the top

**Step 4: Run the Program**
1. Open `main.py` in PyCharm
2. Right-click anywhere in the code
3. Select `Run 'main'`
4. OR: Click the green play button at the top right
5. The application will start!

---

###  Option 3: Using VS Code 

**Step 1: Install Required Software**
1. Download and install Python 3.12+ from [python.org](https://www.python.org/downloads/)
   -  Check "Add Python to PATH" during installation
2. Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
3. Open VS Code

**Step 2: Install Python Extension**
1. Click the Extensions icon (4 squares) on the left sidebar
2. Search for "Python"
3. Install the extension by Microsoft
4. Restart VS Code if prompted

**Step 3: Get the Project**

**Download ZIP**
1. Download and extract the ZIP (see Option 1, Step 2)
2. In VS Code: `File` → `Open Folder`
3. Select the extracted folder

**Step 4: Install Packages**
1. Open the Terminal in VS Code: `View` → `Terminal` (or press `` Ctrl+` ``)
2. Type: `pip install -r requirements.txt`
3. Press Enter

**Step 5: Run the Program**
1. Open `main.py`
2. Click the play button in the top right
3. OR: Right-click in the editor and select "Run Python File in Terminal"
4. The application will start!

---

## How to Use

1. **Select Your Favorite Genre**: Choose from Pop, Rock, EDM, Rap, or Latin in the dropdown menu
2. **Choose Your Use Case**: Select whether you need headphones for:
   - **Workout**: High bass, durable, sweat-resistant
   - **Casual**: Balanced sound, comfortable for daily use
   - **Studio**: Flat frequency response for accurate sound
3. **Get Recommendations**: Click the "Get Recommendations" button to see suggested headphones
4. **Browse Songs**: Click "View All Songs" to explore the music database and filter by genre

## Data Description

### Song Dataset (`spotify_songs.csv`)
Contains ~33,000 songs with Spotify audio features:
- **track_id**: Unique Spotify identifier
- **track_name**: Song title
- **track_artist**: Artist name
- **track_popularity**: Popularity score (0-100)
- **playlist_genre**: Main genre (Pop, Rock, EDM, Rap, Latin)
- **playlist_subgenre**: Specific subgenre
- **danceability**: How suitable for dancing (0-1)
- **energy**: Intensity and power (0-1)
- **valence**: Musical positivity (0-1)
- **tempo**: Beats per minute (BPM)
- **acousticness**: Acoustic confidence measure (0-1)
- **loudness**: Average decibel level (dB)

### Headphone Dataset (`headphones.csv`)
Contains headphone models with specifications:
- **headphone_id**: Unique identifier
- **brand**: Manufacturer
- **model**: Product model
- **price**: Price in USD
- **type**: Form factor (Over-ear, On-ear, In-ear)
- **use_case**: Primary use (Workout, Casual, Studio)
- **bass_level**: Bass intensity (Low, Medium, High)
- **sound_profile**: Sound signature (Balanced, Bass-heavy, Flat)
- **noise_cancellation**: Active noise cancellation (Yes/No)

## Project Structure
```
music-match-headphones/
-/data
    - spotify_songs.csv    # Song dataset
    - headphones.csv       # Headphone dataset
- main.py                  # Main application and GUI
- song.py                  # Song class definition
- headphone.py             # Headphone class definition
- test_song.py             # Unit tests
- requirements.txt         # Python dependencies
- README.md                # This file
```