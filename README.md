# Music Match Headphones

A Python application that recommends headphones based on user music preferences using Spotify audio features.

## Team Members
- Haihan Zhang
- Anish Suresh Saini

## Project Description

Music Match Headphones analyzes a user's music taste (genre preferences, audio features like energy and tempo) and recommends suitable headphones based on their listening habits and use case (workout, casual listening, or studio work).

## Features

### Current Features (Milestone Submission)
- **Data Management**: Loads and stores 33,000+ Spotify songs with audio features
- **Genre Selection**: Dropdown menu to select favorite music genre
- **Use Case Selection**: Radio buttons for workout, casual, or studio use
- **Recommendations**: Basic algorithm that matches headphones to music preferences
- **Song Browser**: View and filter all songs by genre
- **Interactive GUI**: User-friendly graphical interface built with tkinter

### Planned Features (Final Submission)
- Advanced recommendation algorithm using machine learning
- User profile creation and preference saving
- Audio feature visualization
- Price range filtering
- Detailed headphone comparisons

## Installation

### Prerequisites
- Python 3.12.0 or later
- pip (Python package manager)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/music-match-headphones.git
cd music-match-headphones
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure data files are present in 'data' folder:
   - `spotify_songs.csv` - Spotify songs dataset
   - `headphones.csv` - Headphone specifications

## How to Run
```bash
python main.py
```

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
─ main.py              # Main application and GUI
─ song.py              # Song class definition
─ headphone.py         # Headphone class definition
─ test_song.py         # Unit tests
─ spotify_songs.csv    # Song dataset
─ headphones.csv       # Headphone dataset
─ requirements.txt     # Python dependencies
─ README.md            # This file
```


## Future Enhancements

- Implement scikit-learn for machine learning-based recommendations
- Add data visualization with matplotlib/plotly
- Create user profiles with preference history
- Add audio feature analysis and comparison charts
- Implement collaborative filtering
- Add budget constraints and price filtering
- Include user reviews and ratings
