"""
Music Match Headphones - Final Submission
Main GUI Application with Enhanced User Experience
Date: December 2024
Authors: Haihan Zhang, Anish Suresh Saini
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import pandas as pd
from song import Song
from headphone import Headphone

class MusicMatchApp:
    def __init__(self, root):
        """Initialize the Music Match Headphones application"""
        self.root = root
        self.root.title("Music Match Headphones")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # User selection data
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None

        # Load data
        self.songs = []
        self.headphones = []
        self.load_data()

        # Current screen tracker
        self.current_screen = 0

        # Create main container
        self.main_container = tk.Frame(self.root, bg="#f0f0f0")
        self.main_container.pack(fill="both", expand=True)

        # Show welcome screen
        self.show_welcome_screen()

    def load_data(self):
        """Load song and headphone data from CSV files"""
        try:
            # Load songs from spotify_songs.csv
            print("Loading spotify_songs.csv...")
            songs_df = pd.read_csv('data/spotify_songs.csv')

            # Strip whitespace from column names
            songs_df.columns = songs_df.columns.str.strip()

            print(f"Total rows in CSV: {len(songs_df)}")

            # Check if required columns exist
            required_columns = ['track_id', 'track_name', 'track_artist',
                              'track_popularity', 'playlist_genre', 'playlist_subgenre',
                              'danceability', 'energy', 'valence', 'tempo',
                              'acousticness', 'loudness']

            missing_columns = [col for col in required_columns if col not in songs_df.columns]
            if missing_columns:
                messagebox.showerror("Error",
                                   f"Missing columns in spotify_songs.csv: {missing_columns}\n\n"
                                   f"Available columns: {songs_df.columns.tolist()}")
                return

            # Get unique genres
            unique_genres = songs_df['playlist_genre'].unique()
            print(f"Found {len(unique_genres)} unique genres: {unique_genres}")

            # Count songs per genre
            for genre in unique_genres:
                count = len(songs_df[songs_df['playlist_genre'] == genre])
                print(f"  {genre}: {count} songs")

            # Sample songs evenly from each genre
            songs_per_genre = 300
            sampled_songs = []

            for genre in unique_genres:
                genre_songs = songs_df[songs_df['playlist_genre'] == genre]
                sample_size = min(songs_per_genre, len(genre_songs))
                sampled_genre_songs = genre_songs.sample(n=sample_size, random_state=42)
                sampled_songs.append(sampled_genre_songs)

            # Combine all sampled songs
            songs_df_sampled = pd.concat(sampled_songs, ignore_index=True)
            print(f"Sampled {len(songs_df_sampled)} songs total")

            # Load each song into Song objects
            for _, row in songs_df_sampled.iterrows():
                try:
                    song = Song(
                        row['track_id'],
                        row['track_name'],
                        row['track_artist'],
                        row['track_popularity'],
                        row['playlist_genre'],
                        row['playlist_subgenre'],
                        row['danceability'],
                        row['energy'],
                        row['valence'],
                        row['tempo'],
                        row['acousticness'],
                        row['loudness']
                    )
                    self.songs.append(song)
                except Exception as e:
                    print(f"Error loading song: {e}")
                    continue

            # Count songs per genre in loaded data
            print("\nLoaded songs by genre:")
            for genre in unique_genres:
                count = len([s for s in self.songs if s.playlist_genre == genre])
                print(f"  {genre}: {count} songs")

            print(f"\nTotal loaded: {len(self.songs)} songs")

            # Load headphones
            print("\nLoading headphones.csv...")
            headphones_df = pd.read_csv('data/headphones.csv')

            # Strip whitespace from column names
            headphones_df.columns = headphones_df.columns.str.strip()

            for _, row in headphones_df.iterrows():
                try:
                    headphone = Headphone(
                        row['headphone_id'],
                        row['brand'],
                        row['model'],
                        row['price'],
                        row['type'],
                        row['use_case'],
                        row['bass_level'],
                        row['sound_profile'],
                        row['noise_cancellation'],
                        row['user_rating'],
                        row['user_reviews']
                    )
                    self.headphones.append(headphone)
                except Exception as e:
                    print(f"Error loading headphone: {e}")
                    continue

            print(f"Loaded {len(self.headphones)} headphones")

        except FileNotFoundError as e:
            messagebox.showerror("Error",
                               f"Data file not found: {e}\n\n"
                               f"Make sure spotify_songs.csv and headphones.csv are in the data/ folder")
        except KeyError as e:
            messagebox.showerror("Error",
                               f"Column not found in CSV: {e}\n\n"
                               f"Please check your CSV file structure.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

    def clear_screen(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        """Show the welcome/landing screen"""
        self.clear_screen()

        # Welcome frame
        welcome_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        welcome_frame.pack(expand=True)

        # Title
        title_font = font.Font(family="Arial", size=36, weight="bold")
        title_label = tk.Label(welcome_frame, text="🎧 Music Match Headphones",
                              font=title_font, bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=30)

        # Subtitle
        subtitle_font = font.Font(family="Arial", size=14)
        subtitle_label = tk.Label(welcome_frame,
                                 text="Find Your Perfect Headphones Based on Your Music Taste",
                                 font=subtitle_font, bg="#f0f0f0", fg="#7f8c8d")
        subtitle_label.pack(pady=10)

        # Description
        desc_text = ("We'll analyze your music preferences and recommend\n"
                    "the perfect headphones tailored just for you!")
        desc_label = tk.Label(welcome_frame, text=desc_text,
                             font=("Arial", 12), bg="#f0f0f0", fg="#34495e",
                             justify="center")
        desc_label.pack(pady=20)

        # Start button
        start_btn = tk.Button(welcome_frame, text="Get Started",
                             command=self.show_genre_selection,
                             font=("Arial", 16, "bold"),
                             bg="#3498db", fg="white",
                             padx=40, pady=15,
                             relief="flat", cursor="hand2")
        start_btn.pack(pady=30)

        # Stats
        stats_frame = tk.Frame(welcome_frame, bg="#f0f0f0")
        stats_frame.pack(pady=20)

        stats = [
            (f"{len(self.songs)}", "Songs Analyzed"),
            (f"{len(self.headphones)}", "Headphones"),
            (f"{len(set([s.playlist_genre for s in self.songs]))}", "Genres")
        ]

        for value, label in stats:
            stat_frame = tk.Frame(stats_frame, bg="#ecf0f1", relief="flat", bd=2)
            stat_frame.pack(side="left", padx=20)

            tk.Label(stat_frame, text=value, font=("Arial", 24, "bold"),
                    bg="#ecf0f1", fg="#2980b9").pack(padx=20, pady=(10, 0))
            tk.Label(stat_frame, text=label, font=("Arial", 11),
                    bg="#ecf0f1", fg="#7f8c8d").pack(padx=20, pady=(0, 10))

    def show_genre_selection(self):
        """Show genre selection screen with card view"""
        self.clear_screen()
        self.current_screen = 1

        # Header
        header_frame = tk.Frame(self.main_container, bg="#3498db", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Step 1: Select Your Favorite Genre",
                font=("Arial", 20, "bold"), bg="#3498db", fg="white").pack(pady=25)

        # Content frame with scrollbar
        content_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Get unique genres
        genres = sorted(list(set([song.playlist_genre for song in self.songs])))

        # Cards frame
        cards_frame = tk.Frame(content_frame, bg="#f0f0f0")
        cards_frame.pack(pady=20)

        # Create genre cards (2 rows of 3)
        row = 0
        col = 0
        for genre in genres[:6]:  # Show first 6 genres
            card = self.create_genre_card(cards_frame, genre)
            card.grid(row=row, column=col, padx=15, pady=15)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Search section
        search_frame = tk.Frame(content_frame, bg="#f0f0f0")
        search_frame.pack(pady=20)

        tk.Label(search_frame, text="Don't see your favorite genre? Search:",
                font=("Arial", 11), bg="#f0f0f0").pack()

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                               font=("Arial", 12), width=30)
        search_entry.pack(pady=10)

        search_btn = tk.Button(search_frame, text="Search Genre",
                              command=lambda: self.search_genre(search_var.get()),
                              font=("Arial", 11), bg="#95a5a6", fg="white",
                              padx=20, pady=8)
        search_btn.pack()

    def create_genre_card(self, parent, genre):
        """Create a clickable genre card"""
        # Genre emoji mapping
        genre_emojis = {
            "pop": "🎤",
            "rock": "🎸",
            "edm": "🎹",
            "rap": "🎤",
            "latin": "💃",
            "r&b": "🎵",
            "hip-hop": "🎤"
        }

        # Genre color mapping
        genre_colors = {
            "pop": "#e74c3c",
            "rock": "#9b59b6",
            "edm": "#3498db",
            "rap": "#f39c12",
            "latin": "#e67e22",
            "r&b": "#1abc9c",
            "hip-hop": "#34495e"
        }

        emoji = genre_emojis.get(genre.lower(), "🎵")
        color = genre_colors.get(genre.lower(), "#95a5a6")

        # Card frame
        card = tk.Frame(parent, bg="white", relief="raised", bd=2,
                       cursor="hand2", width=200, height=150)
        card.pack_propagate(False)

        # Emoji
        tk.Label(card, text=emoji, font=("Arial", 40),
                bg="white").pack(pady=(20, 10))

        # Genre name
        tk.Label(card, text=genre.upper(), font=("Arial", 14, "bold"),
                bg="white", fg=color).pack()

        # Song count
        genre_count = len([s for s in self.songs if s.playlist_genre == genre])
        tk.Label(card, text=f"{genre_count} songs",
                font=("Arial", 10), bg="white", fg="#7f8c8d").pack(pady=5)

        # Bind click event
        card.bind("<Button-1>", lambda e: self.select_genre(genre))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e: self.select_genre(genre))

        # Hover effects
        card.bind("<Enter>", lambda e: card.config(bg="#ecf0f1"))
        card.bind("<Leave>", lambda e: card.config(bg="white"))

        return card

    def search_genre(self, search_term):
        """Search for a genre"""
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a genre to search")
            return

        genres = list(set([song.playlist_genre for song in self.songs]))
        matching = [g for g in genres if search_term.lower() in g.lower()]

        if matching:
            self.select_genre(matching[0])
        else:
            messagebox.showinfo("Not Found",
                              f"Genre '{search_term}' not found in our database.\n"
                              f"Available genres: {', '.join(sorted(genres))}")

    def select_genre(self, genre):
        """Handle genre selection"""
        self.selected_genre = genre
        print(f"Selected genre: {genre}")
        self.show_song_selection()

    def show_song_selection(self):
        """Show song selection screen"""
        self.clear_screen()
        self.current_screen = 2

        # Header
        header_frame = tk.Frame(self.main_container, bg="#27ae60", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text=f"Step 2: Select 5 Songs You Love",
                font=("Arial", 20, "bold"), bg="#27ae60", fg="white").pack(pady=15)
        tk.Label(header_frame, text=f"Genre: {self.selected_genre.upper()}",
                font=("Arial", 12), bg="#27ae60", fg="white").pack()

        # Content frame
        content_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Selected songs display
        self.selected_display_frame = tk.Frame(content_frame, bg="#ecf0f1",
                                               relief="solid", bd=2)
        self.selected_display_frame.pack(fill="x", pady=(0, 20))

        tk.Label(self.selected_display_frame,
                text=f"Selected: {len(self.selected_songs)}/5",
                font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=10)

        # Get genre songs
        genre_songs = [s for s in self.songs if s.playlist_genre == self.selected_genre]

        # Display 6 random songs
        import random
        display_songs = random.sample(genre_songs, min(6, len(genre_songs)))

        # Songs frame
        songs_frame = tk.Frame(content_frame, bg="#f0f0f0")
        songs_frame.pack(pady=20)

        # Create song cards (2 rows of 3)
        row = 0
        col = 0
        for song in display_songs:
            card = self.create_song_card(songs_frame, song)
            card.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Search section
        search_frame = tk.Frame(content_frame, bg="#f0f0f0")
        search_frame.pack(pady=20)

        tk.Label(search_frame, text="Search for a specific song:",
                font=("Arial", 11), bg="#f0f0f0").pack()

        self.song_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.song_search_var,
                               font=("Arial", 12), width=40)
        search_entry.pack(pady=10)

        search_btn = tk.Button(search_frame, text="Search Song",
                              command=self.search_song,
                              font=("Arial", 11), bg="#95a5a6", fg="white",
                              padx=20, pady=8)
        search_btn.pack()

        # Navigation buttons
        nav_frame = tk.Frame(content_frame, bg="#f0f0f0")
        nav_frame.pack(pady=20)

        back_btn = tk.Button(nav_frame, text="← Back",
                            command=self.show_genre_selection,
                            font=("Arial", 11), bg="#95a5a6", fg="white",
                            padx=20, pady=10)
        back_btn.pack(side="left", padx=10)

        next_btn = tk.Button(nav_frame, text="Next →",
                            command=self.validate_and_show_use_case,
                            font=("Arial", 11), bg="#27ae60", fg="white",
                            padx=20, pady=10)
        next_btn.pack(side="left", padx=10)

    def create_song_card(self, parent, song):
        """Create a song card"""
        card = tk.Frame(parent, bg="white", relief="raised", bd=2,
                       cursor="hand2", width=280, height=120)
        card.pack_propagate(False)

        # Song info frame
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Song name (truncate if too long)
        song_name = song.track_name[:35] + "..." if len(song.track_name) > 35 else song.track_name
        tk.Label(info_frame, text=song_name,
                font=("Arial", 11, "bold"), bg="white",
                wraplength=250, justify="left").pack(anchor="w")

        # Artist name
        artist_name = song.track_artist[:40] + "..." if len(song.track_artist) > 40 else song.track_artist
        tk.Label(info_frame, text=artist_name,
                font=("Arial", 9), bg="white", fg="#7f8c8d",
                wraplength=250, justify="left").pack(anchor="w", pady=(5, 10))

        # Stats
        stats_text = f"⚡ Energy: {song.energy:.2f} | 🎵 Tempo: {song.tempo:.0f} BPM"
        tk.Label(info_frame, text=stats_text,
                font=("Arial", 8), bg="white", fg="#95a5a6").pack(anchor="w")

        # Bind click event
        card.bind("<Button-1>", lambda e: self.toggle_song_selection(song, card))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e: self.toggle_song_selection(song, card))

        # Hover effects
        card.bind("<Enter>", lambda e: card.config(bg="#ecf0f1") if song not in self.selected_songs else None)
        card.bind("<Leave>", lambda e: card.config(bg="white") if song not in self.selected_songs else None)

        return card

    def toggle_song_selection(self, song, card):
        """Toggle song selection"""
        if song in self.selected_songs:
            self.selected_songs.remove(song)
            card.config(bg="white", relief="raised")
        else:
            if len(self.selected_songs) >= 5:
                messagebox.showwarning("Limit Reached",
                                      "You can only select up to 5 songs")
                return
            self.selected_songs.append(song)
            card.config(bg="#d5f4e6", relief="sunken")

        # Update selected count
        for widget in self.selected_display_frame.winfo_children():
            widget.destroy()

        tk.Label(self.selected_display_frame,
                text=f"Selected: {len(self.selected_songs)}/5",
                font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=10)

        # Show selected songs
        if self.selected_songs:
            for song in self.selected_songs:
                song_text = f"✓ {song.track_name} - {song.track_artist}"
                tk.Label(self.selected_display_frame, text=song_text,
                        font=("Arial", 9), bg="#ecf0f1",
                        fg="#27ae60").pack(anchor="w", padx=20)

    def search_song(self):
        """Search for a song"""
        search_term = self.song_search_var.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a song name to search")
            return

        # Search in genre songs
        genre_songs = [s for s in self.songs if s.playlist_genre == self.selected_genre]
        matching = [s for s in genre_songs
                   if search_term.lower() in s.track_name.lower() or
                   search_term.lower() in s.track_artist.lower()]

        if not matching:
            messagebox.showinfo("Not Found",
                              f"No songs matching '{search_term}' found in {self.selected_genre} genre.")
            return

        # Show search results in new window
        self.show_search_results(matching)

    def show_search_results(self, songs):
        """Show search results in a popup"""
        results_window = tk.Toplevel(self.root)
        results_window.title("Search Results")
        results_window.geometry("500x600")

        tk.Label(results_window, text="Search Results",
                font=("Arial", 14, "bold")).pack(pady=10)

        # Scrollable frame
        canvas = tk.Canvas(results_window)
        scrollbar = tk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display results
        for song in songs[:20]:  # Limit to 20 results
            song_frame = tk.Frame(scrollable_frame, bg="white",
                                 relief="raised", bd=1, cursor="hand2")
            song_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(song_frame, text=song.track_name,
                    font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=10, pady=2)
            tk.Label(song_frame, text=song.track_artist,
                    font=("Arial", 9), bg="white", fg="#7f8c8d").pack(anchor="w", padx=10, pady=2)

            song_frame.bind("<Button-1>",
                           lambda e, s=song: self.select_from_search(s, results_window))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_from_search(self, song, window):
        """Select a song from search results"""
        if len(self.selected_songs) >= 5:
            messagebox.showwarning("Limit Reached",
                                  "You can only select up to 5 songs")
            return

        if song not in self.selected_songs:
            self.selected_songs.append(song)
            messagebox.showinfo("Added", f"Added '{song.track_name}' to your selection")
            window.destroy()
            self.show_song_selection()  # Refresh the screen
        else:
            messagebox.showinfo("Already Selected",
                              "This song is already in your selection")

    def validate_and_show_use_case(self):
        """Validate song selection and show use case screen"""
        if len(self.selected_songs) < 5:
            messagebox.showwarning("Incomplete Selection",
                                  f"Please select 5 songs. You have selected {len(self.selected_songs)}.")
            return

        self.show_use_case_selection()

    def show_use_case_selection(self):
        """Show use case selection screen"""
        self.clear_screen()
        self.current_screen = 3

        # Header
        header_frame = tk.Frame(self.main_container, bg="#9b59b6", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Step 3: What's Your Primary Use Case?",
                font=("Arial", 20, "bold"), bg="#9b59b6", fg="white").pack(pady=25)

        # Content frame
        content_frame = tk.Frame(self.main_container, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Use cases
        use_cases = [
            ("Workout", "🏋️", "High-energy activities, sweat-resistant", "#e74c3c"),
            ("Casual", "☕", "Daily listening, commuting, relaxation", "#3498db"),
            ("Studio", "🎙️", "Professional audio work, accurate sound", "#f39c12"),
            ("Gaming", "🎮", "Gaming sessions, immersive audio", "#9b59b6")
        ]

        # Cards frame
        cards_frame = tk.Frame(content_frame, bg="#f0f0f0")
        cards_frame.pack(expand=True)

        row = 0
        col = 0
        for use_case, emoji, description, color in use_cases:
            card = self.create_use_case_card(cards_frame, use_case, emoji,
                                            description, color)
            card.grid(row=row, column=col, padx=20, pady=20)

            col += 1
            if col >= 2:
                col = 0
                row += 1

        # Navigation
        nav_frame = tk.Frame(content_frame, bg="#f0f0f0")
        nav_frame.pack(pady=20)

        back_btn = tk.Button(nav_frame, text="← Back",
                            command=self.show_song_selection,
                            font=("Arial", 11), bg="#95a5a6", fg="white",
                            padx=20, pady=10)
        back_btn.pack()

    def create_use_case_card(self, parent, use_case, emoji, description, color):
        """Create a use case card"""
        card = tk.Frame(parent, bg="white", relief="raised", bd=2,
                       cursor="hand2", width=350, height=180)
        card.pack_propagate(False)

        # Emoji
        tk.Label(card, text=emoji, font=("Arial", 50),
                bg="white").pack(pady=(20, 10))

        # Use case name
        tk.Label(card, text=use_case.upper(), font=("Arial", 16, "bold"),
                bg="white", fg=color).pack()

        # Description
        tk.Label(card, text=description, font=("Arial", 10),
                bg="white", fg="#7f8c8d", wraplength=300).pack(pady=10)

        # Bind click event
        card.bind("<Button-1>", lambda e: self.select_use_case(use_case))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e: self.select_use_case(use_case))

        # Hover effects
        card.bind("<Enter>", lambda e: card.config(bg="#ecf0f1"))
        card.bind("<Leave>", lambda e: card.config(bg="white"))

        return card

    def select_use_case(self, use_case):
        """Handle use case selection"""
        self.selected_use_case = use_case
        print(f"Selected use case: {use_case}")
        self.generate_recommendations()

    def generate_recommendations(self):
        """Generate headphone recommendations based on user input"""
        print("\n=== Generating Recommendations ===")
        print(f"Genre: {self.selected_genre}")
        print(f"Songs: {len(self.selected_songs)}")
        print(f"Use Case: {self.selected_use_case}")

        # Calculate average audio features from selected songs
        avg_energy = sum([s.energy for s in self.selected_songs]) / len(self.selected_songs)
        avg_bass = sum([s.loudness for s in self.selected_songs]) / len(self.selected_songs)
        avg_tempo = sum([s.tempo for s in self.selected_songs]) / len(self.selected_songs)

        print(f"Avg Energy: {avg_energy:.2f}")
        print(f"Avg Bass (Loudness): {avg_bass:.2f}")
        print(f"Avg Tempo: {avg_tempo:.0f}")

        # Filter headphones by use case
        matching_headphones = [hp for hp in self.headphones
                              if hp.use_case.lower() == self.selected_use_case.lower()]
        print(f"Found {len(matching_headphones)} headphones for {self.selected_use_case}")

        # Score headphones based on music preferences
        scored_headphones = []
        for hp in matching_headphones:
            score = 0

            # Bass matching
            if avg_bass > -4 and hp.bass_level == "High":
                score += 3
            elif avg_bass < -7 and hp.bass_level == "Low":
                score += 3
            elif hp.bass_level == "Medium":
                score += 2

            # Energy matching
            if avg_energy > 0.7 and hp.sound_profile == "Bass-heavy":
                score += 2
            elif avg_energy < 0.4 and hp.sound_profile == "Flat":
                score += 2
            else:
                score += 1

            # Add user rating to score
            score += hp.user_rating

            scored_headphones.append((hp, score))

        # Sort by score
        scored_headphones.sort(key=lambda x: x[1], reverse=True)

        # Categorize recommendations
        budget = []  # < $150
        premium = []  # > $400
        balanced = []  # $150 - $400

        for hp, score in scored_headphones:
            if hp.price < 150:
                budget.append(hp)
            elif hp.price > 400:
                premium.append(hp)
            else:
                balanced.append(hp)

        # Get top 3 from each category
        recommendations = {
            "Budget-Friendly": budget[:3],
            "Best of the Line": premium[:3],
            "Best of Both": balanced[:3]
        }

        # Find most positively reviewed (highest rating * reviews)
        all_recommended = budget[:3] + premium[:3] + balanced[:3]
        if all_recommended:
            most_reviewed = max(all_recommended,
                                key=lambda hp: hp.user_rating * hp.user_reviews)
        else:
            most_reviewed = None

        self.show_recommendations(recommendations, most_reviewed)

    def show_recommendations(self, recommendations, most_reviewed):
        """Show final recommendations screen"""
        self.clear_screen()

        # Header
        header_frame = tk.Frame(self.main_container, bg="#27ae60", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🎉 Your Perfect Headphones!",
                 font=("Arial", 24, "bold"), bg="#27ae60", fg="white").pack(pady=15)
        tk.Label(header_frame, text=f"Based on {self.selected_genre} music for {self.selected_use_case}",
                 font=("Arial", 12), bg="#27ae60", fg="white").pack()

        # Scrollable content
        canvas = tk.Canvas(self.main_container, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg="#f0f0f0")

        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Most Positively Reviewed Section
        if most_reviewed:
            most_reviewed_frame = tk.Frame(content_frame, bg="#fff9e6",
                                           relief="solid", bd=2)
            most_reviewed_frame.pack(fill="x", padx=20, pady=20)

            tk.Label(most_reviewed_frame,
                     text="⭐ MOST POSITIVELY REVIEWED ⭐",
                     font=("Arial", 16, "bold"), bg="#fff9e6",
                     fg="#f39c12").pack(pady=15)

            self.create_recommendation_card(most_reviewed_frame, most_reviewed, True)

        # Categories
        category_colors = {
            "Budget-Friendly": ("#d5f4e6", "#27ae60"),
            "Best of Both": ("#e3f2fd", "#2196f3"),
            "Best of the Line": ("#fce4ec", "#e91e63")
        }

        for category, headphones in recommendations.items():
            if not headphones:
                continue

            bg_color, text_color = category_colors.get(category, ("#f0f0f0", "#000"))

            category_frame = tk.Frame(content_frame, bg=bg_color,
                                      relief="solid", bd=2)
            category_frame.pack(fill="x", padx=20, pady=20)

            tk.Label(category_frame, text=category.upper(),
                     font=("Arial", 14, "bold"), bg=bg_color,
                     fg=text_color).pack(pady=15)

            for hp in headphones:
                self.create_recommendation_card(category_frame, hp, False)

        # Navigation
        nav_frame = tk.Frame(content_frame, bg="#f0f0f0")
        nav_frame.pack(pady=20)

        restart_btn = tk.Button(nav_frame, text="🔄 Start Over",
                                command=self.restart,
                                font=("Arial", 12), bg="#3498db", fg="white",
                                padx=30, pady=15)
        restart_btn.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_recommendation_card(self, parent, headphone, highlight=False):
        """Create a recommendation card"""
        card_bg = "#fffacd" if highlight else "white"

        card = tk.Frame(parent, bg=card_bg, relief="groove", bd=2)
        card.pack(fill="x", padx=20, pady=10)

        # Content frame
        content = tk.Frame(card, bg=card_bg)
        content.pack(fill="x", padx=20, pady=15)

        # Header (Brand and Model)
        header_frame = tk.Frame(content, bg=card_bg)
        header_frame.pack(fill="x", pady=(0, 10))

        tk.Label(header_frame, text=f"{headphone.brand} {headphone.model}",
                 font=("Arial", 14, "bold"), bg=card_bg,
                 fg="#2c3e50").pack(side="left")

        tk.Label(header_frame, text=f"${headphone.price:.0f}",
                 font=("Arial", 14, "bold"), bg=card_bg,
                 fg="#27ae60").pack(side="right")

        # Rating
        stars = "⭐" * int(headphone.user_rating)
        rating_text = f"{stars} {headphone.user_rating}/5.0 ({headphone.user_reviews:,} reviews)"
        tk.Label(content, text=rating_text, font=("Arial", 10),
                 bg=card_bg, fg="#f39c12").pack(anchor="w")

        # Specs
        specs_frame = tk.Frame(content, bg=card_bg)
        specs_frame.pack(fill="x", pady=10)

        specs = [
            ("Type", headphone.hp_type),
            ("Bass", headphone.bass_level),
            ("Profile", headphone.sound_profile),
            ("ANC", "Yes" if headphone.noise_cancellation else "No")
        ]

        for label, value in specs:
            spec_frame = tk.Frame(specs_frame, bg="#ecf0f1", relief="flat")
            spec_frame.pack(side="left", padx=5)

            tk.Label(spec_frame, text=label, font=("Arial", 8),
                     bg="#ecf0f1", fg="#7f8c8d").pack(padx=10, pady=(5, 0))
            tk.Label(spec_frame, text=value, font=("Arial", 10, "bold"),
                     bg="#ecf0f1", fg="#2c3e50").pack(padx=10, pady=(0, 5))

    def restart(self):
        """Restart the application"""
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.show_welcome_screen()



def main():
    root = tk.Tk()
    app = MusicMatchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()