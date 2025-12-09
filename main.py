"""
Music Match Headphones - Final Submission
Optimized version with batch loading
Date: December 2024
Authors: Haihan Zhang, Anish Suresh Saini
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import pandas as pd
from song import Song
from headphone import Headphone
import random
import threading

class MusicMatchApp:
    def __init__(self, root):
        """Initialize the Music Match Headphones application"""
        self.root = root
        self.root.title("Music Match Headphones")
        self.root.geometry("1200x800")
        self.root.configure(bg="#121212")

        # Color scheme - Dark theme with red accents
        self.colors = {
            'bg_dark': '#121212',
            'bg_card': '#1e1e1e',
            'bg_lighter': '#282828',
            'primary_red': '#e63946',
            'primary_red_hover': '#d62828',
            'accent_red': '#ff006e',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'text_muted': '#6a6a6a',
            'success': '#1db954',
            'warning': '#ffd60a',
            'selected': '#2a2a2a',
            'hover': '#333333'
        }

        # User selection data
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.filtered_songs = []
        self.current_display_songs = []

        # Load data
        self.songs = []
        self.headphones = []
        self.load_data()

        # Current screen tracker
        self.current_screen = 0

        # Configure styles
        self.configure_styles()

        # Create main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.main_container.pack(fill="both", expand=True)

        # Show welcome screen
        self.show_welcome_screen()

    def configure_styles(self):
        """Configure ttk styles for better UI"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure scrollbar
        style.configure("Vertical.TScrollbar",
                       background=self.colors['bg_lighter'],
                       troughcolor=self.colors['bg_dark'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_secondary'])

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

            # Store the dataframe for lazy loading
            self.songs_df = songs_df

            # Get unique genres
            self.unique_genres = songs_df['playlist_genre'].unique()
            print(f"Found {len(self.unique_genres)} unique genres: {self.unique_genres}")

            # Count songs per genre
            self.genre_counts = {}
            for genre in self.unique_genres:
                count = len(songs_df[songs_df['playlist_genre'] == genre])
                self.genre_counts[genre] = count
                print(f"  {genre}: {count} songs")

            print(f"\nTotal: {len(songs_df)} songs available")

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
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

    def create_song_row(self, parent, index, song):
        """Create a song row - Spotify style"""
        is_selected = song in self.selected_songs
        bg_color = self.colors['selected'] if is_selected else self.colors['bg_dark']

        row = tk.Frame(parent, bg=bg_color, cursor="hand2", height=60)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        # Index/Checkbox
        index_frame = tk.Frame(row, bg=bg_color, width=50)
        index_frame.pack(side="left")
        index_frame.pack_propagate(False)

        if is_selected:
            tk.Label(index_frame, text="✓", font=("Segoe UI", 14, "bold"),
                     bg=bg_color, fg=self.colors['success']).pack(expand=True)
        else:
            tk.Label(index_frame, text=str(index), font=("Segoe UI", 11),
                     bg=bg_color, fg=self.colors['text_muted']).pack(expand=True)

        # Title
        title_text = song.track_name[:50] + "..." if len(song.track_name) > 50 else song.track_name
        title_label = tk.Label(row, text=title_text, font=("Segoe UI", 11),
                               bg=bg_color, fg=self.colors['text_primary'],
                               anchor="w", width=40)
        title_label.pack(side="left", padx=5)

        # Artist
        artist_text = song.track_artist[:40] + "..." if len(song.track_artist) > 40 else song.track_artist
        artist_label = tk.Label(row, text=artist_text, font=("Segoe UI", 10),
                                bg=bg_color, fg=self.colors['text_secondary'],
                                anchor="w", width=30)
        artist_label.pack(side="left", padx=5)

        # Energy
        energy_label = tk.Label(row, text=f"{song.energy:.2f}", font=("Segoe UI", 10),
                                bg=bg_color, fg=self.colors['text_secondary'],
                                anchor="center", width=10)
        energy_label.pack(side="left", padx=5)

        # Tempo
        tempo_label = tk.Label(row, text=f"{song.tempo:.0f}", font=("Segoe UI", 10),
                               bg=bg_color, fg=self.colors['text_secondary'],
                               anchor="center", width=10)
        tempo_label.pack(side="left", padx=5)

        # Bind click
        def click_handler(e):
            self.toggle_song_selection_list(song)

        row.bind("<Button-1>", click_handler)
        for child in row.winfo_children():
            child.bind("<Button-1>", click_handler)
            for grandchild in child.winfo_children():
                grandchild.bind("<Button-1>", click_handler)

        # Hover effect
        def on_enter(e):
            if song not in self.selected_songs:
                row.config(bg=self.colors['hover'])
                index_frame.config(bg=self.colors['hover'])
                for widget in [title_label, artist_label, energy_label, tempo_label]:
                    widget.config(bg=self.colors['hover'])
                for child in index_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.colors['hover'])

        def on_leave(e):
            if song not in self.selected_songs:
                row.config(bg=self.colors['bg_dark'])
                index_frame.config(bg=self.colors['bg_dark'])
                for widget in [title_label, artist_label, energy_label, tempo_label]:
                    widget.config(bg=self.colors['bg_dark'])
                for child in index_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.colors['bg_dark'])

        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)

    def toggle_song_selection_list(self, song):
        """Toggle song selection from list"""
        if song in self.selected_songs:
            self.selected_songs.remove(song)
        else:
            if len(self.selected_songs) >= 5:
                messagebox.showwarning("Limit Reached",
                                       "You can only select up to 5 songs.",
                                       parent=self.root)
                return
            self.selected_songs.append(song)

        # Update count
        self.selected_count_label.config(text=f"{len(self.selected_songs)}/5")

        # Refresh display
        search_term = self.song_search_var.get()
        if search_term and search_term != "Search songs or artists...":
            self.on_search_change()
        else:
            self.display_songs(self.current_display_songs)

    def clear_screen(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def create_gradient_button(self, parent, text, command, width=200):
        """Create a button with gradient effect"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_dark'])

        # Create canvas for gradient
        canvas = tk.Canvas(button_frame, width=width, height=50,
                          bg=self.colors['bg_dark'], highlightthickness=0,
                          cursor="hand2")
        canvas.pack()

        # Draw gradient
        gradient = canvas.create_rectangle(0, 0, width, 50,
                                          fill=self.colors['primary_red'],
                                          outline="")

        # Add text
        text_id = canvas.create_text(width//2, 25, text=text,
                                     font=("Segoe UI", 12, "bold"),
                                     fill=self.colors['text_primary'])

        # Bind events
        def on_click(e):
            command()

        def on_enter(e):
            canvas.itemconfig(gradient, fill=self.colors['accent_red'])

        def on_leave(e):
            canvas.itemconfig(gradient, fill=self.colors['primary_red'])

        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)

        return button_frame

    def create_modern_button(self, parent, text, command, bg_color=None, width=None):
        """Create a modern styled button"""
        if bg_color is None:
            bg_color = self.colors['primary_red']

        button = tk.Button(parent, text=text, command=command,
                          font=("Segoe UI", 11, "bold"),
                          bg=bg_color, fg=self.colors['text_primary'],
                          activebackground=self.colors['primary_red_hover'],
                          activeforeground=self.colors['text_primary'],
                          relief="flat", cursor="hand2",
                          borderwidth=0, highlightthickness=0,
                          padx=25, pady=12)

        if width:
            button.config(width=width)

        def on_enter(e):
            button['background'] = self.colors['primary_red_hover']

        def on_leave(e):
            button['background'] = bg_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def show_welcome_screen(self):
        """Show the welcome/landing screen"""
        self.clear_screen()

        # Welcome frame
        welcome_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        welcome_frame.pack(expand=True)

        # Logo/Icon
        tk.Label(welcome_frame, text="🎧", font=("Segoe UI Emoji", 80),
                bg=self.colors['bg_dark']).pack(pady=30)

        # Title
        tk.Label(welcome_frame, text="Music Match Headphones",
                font=("Segoe UI", 42, "bold"), bg=self.colors['bg_dark'],
                fg=self.colors['text_primary']).pack(pady=10)

        # Subtitle with gradient effect
        subtitle_frame = tk.Frame(welcome_frame, bg=self.colors['bg_dark'])
        subtitle_frame.pack(pady=15)

        tk.Label(subtitle_frame,
                text="Find Your Perfect",
                font=("Segoe UI", 16), bg=self.colors['bg_dark'],
                fg=self.colors['text_secondary']).pack()
        tk.Label(subtitle_frame,
                text="Headphones",
                font=("Segoe UI", 16, "bold"), bg=self.colors['bg_dark'],
                fg=self.colors['primary_red']).pack()

        # Description
        tk.Label(welcome_frame,
                text="Personalized recommendations based on your music taste",
                font=("Segoe UI", 13), bg=self.colors['bg_dark'],
                fg=self.colors['text_muted']).pack(pady=20)

        # Start button with gradient
        start_btn = self.create_gradient_button(welcome_frame, "GET STARTED →",
                                                self.show_genre_selection,
                                                width=250)
        start_btn.pack(pady=40)

        # Stats
        stats_frame = tk.Frame(welcome_frame, bg=self.colors['bg_dark'])
        stats_frame.pack(pady=30)

        total_songs = len(self.songs_df) if hasattr(self, 'songs_df') else 0

        stats = [
            (f"{total_songs:,}", "Songs", self.colors['primary_red']),
            (f"{len(self.headphones)}", "Headphones", self.colors['accent_red']),
            (f"{len(self.unique_genres) if hasattr(self, 'unique_genres') else 0}", "Genres", self.colors['success'])
        ]

        for value, label, color in stats:
            stat_card = tk.Frame(stats_frame, bg=self.colors['bg_card'])
            stat_card.pack(side="left", padx=25)

            inner = tk.Frame(stat_card, bg=self.colors['bg_card'])
            inner.pack(padx=35, pady=20)

            tk.Label(inner, text=value, font=("Segoe UI", 32, "bold"),
                    bg=self.colors['bg_card'], fg=color).pack()
            tk.Label(inner, text=label, font=("Segoe UI", 12),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()

    def show_genre_selection(self):
        """Show genre selection screen"""
        self.clear_screen()
        self.current_screen = 1

        # Header
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_card'], height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="STEP 1 OF 3",
                font=("Segoe UI", 10), bg=self.colors['bg_card'],
                fg=self.colors['text_muted']).pack(pady=(20, 5))
        tk.Label(header_frame, text="Choose Your Genre",
                font=("Segoe UI", 26, "bold"), bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack()

        # Main content with scrolling
        main_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1200)
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Content
        content_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_dark'])
        content_frame.pack(padx=60, pady=40)

        # Get genres
        genres = sorted(list(self.unique_genres))

        # Genre cards
        cards_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        cards_frame.pack(pady=20)

        row = 0
        col = 0
        for genre in genres:
            card = self.create_dark_genre_card(cards_frame, genre)
            card.grid(row=row, column=col, padx=20, pady=20)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_dark_genre_card(self, parent, genre):
        """Create a dark themed genre card"""
        genre_emojis = {
            "pop": "🎤", "rock": "🎸", "edm": "🎹", "rap": "🎤",
            "latin": "💃", "r&b": "🎵", "hip-hop": "🎤"
        }

        emoji = genre_emojis.get(genre.lower(), "🎵")

        # Card
        card = tk.Frame(parent, bg=self.colors['bg_card'], cursor="hand2",
                       width=280, height=200)
        card.pack_propagate(False)

        # Emoji
        tk.Label(card, text=emoji, font=("Segoe UI Emoji", 60),
                bg=self.colors['bg_card']).pack(pady=(35, 15))

        # Genre name
        tk.Label(card, text=genre.upper(), font=("Segoe UI", 18, "bold"),
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack()

        # Song count
        genre_count = self.genre_counts.get(genre, 0)
        tk.Label(card, text=f"{genre_count:,} songs",
                font=("Segoe UI", 11), bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(pady=15)

        # Add accent line at bottom
        accent_line = tk.Frame(card, bg=self.colors['primary_red'], height=3)
        accent_line.pack(side="bottom", fill="x")

        # Bind events
        def click_handler(e):
            self.select_genre(genre)

        card.bind("<Button-1>", click_handler)
        for child in card.winfo_children():
            child.bind("<Button-1>", click_handler)

        def on_enter(e):
            card.config(bg=self.colors['hover'])
            for child in card.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.colors['hover'])

        def on_leave(e):
            card.config(bg=self.colors['bg_card'])
            for child in card.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.colors['bg_card'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def select_genre(self, genre):
        """Handle genre selection with loading screen"""
        self.selected_genre = genre
        print(f"Selected genre: {genre}")

        # Show loading screen
        self.show_loading_screen()

        # Load songs in background thread
        def load_songs():
            # Filter dataframe for selected genre
            genre_df = self.songs_df[self.songs_df['playlist_genre'] == genre]

            # Convert to Song objects
            self.filtered_songs = []
            for _, row in genre_df.iterrows():
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
                    self.filtered_songs.append(song)
                except Exception as e:
                    print(f"Error loading song: {e}")
                    continue

            print(f"Loaded {len(self.filtered_songs)} songs for {genre}")

            # Update UI on main thread
            self.root.after(0, self.show_song_selection)

        # Start loading in background
        thread = threading.Thread(target=load_songs, daemon=True)
        thread.start()

    def show_loading_screen(self):
        """Show loading screen"""
        self.clear_screen()

        loading_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        loading_frame.pack(expand=True)

        tk.Label(loading_frame, text="🎵", font=("Segoe UI Emoji", 80),
                bg=self.colors['bg_dark']).pack(pady=30)

        tk.Label(loading_frame, text="Loading Songs...",
                font=("Segoe UI", 24, "bold"), bg=self.colors['bg_dark'],
                fg=self.colors['text_primary']).pack(pady=10)

        tk.Label(loading_frame, text=f"Preparing {self.genre_counts.get(self.selected_genre, 0):,} songs",
                font=("Segoe UI", 13), bg=self.colors['bg_dark'],
                fg=self.colors['text_secondary']).pack()

        # Animated dots
        self.loading_label = tk.Label(loading_frame, text="",
                                     font=("Segoe UI", 16), bg=self.colors['bg_dark'],
                                     fg=self.colors['primary_red'])
        self.loading_label.pack(pady=20)

        self.animate_loading()

    def animate_loading(self, dots=0):
        """Animate loading dots"""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.config(text="." * (dots % 4))
            self.root.after(500, lambda: self.animate_loading(dots + 1))

    def show_song_selection(self):
        """Show song selection screen with full list - Spotify inspired"""
        self.clear_screen()
        self.current_screen = 2

        # Header
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_card'])
        header_frame.pack(fill="x")

        header_inner = tk.Frame(header_frame, bg=self.colors['bg_card'])
        header_inner.pack(fill="x", padx=40, pady=25)

        # Left side - Title
        left_header = tk.Frame(header_inner, bg=self.colors['bg_card'])
        left_header.pack(side="left")

        tk.Label(left_header, text="STEP 2 OF 3",
                font=("Segoe UI", 10), bg=self.colors['bg_card'],
                fg=self.colors['text_muted']).pack(anchor="w")
        tk.Label(left_header, text=f"{self.selected_genre.upper()} • Select 5 Songs",
                font=("Segoe UI", 24, "bold"), bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(anchor="w", pady=(5, 0))

        tk.Label(left_header, text=f"{len(self.filtered_songs):,} songs available",
                font=("Segoe UI", 10), bg=self.colors['bg_card'],
                fg=self.colors['text_muted']).pack(anchor="w", pady=(5, 0))

        # Right side - Selected count
        right_header = tk.Frame(header_inner, bg=self.colors['bg_card'])
        right_header.pack(side="right")

        self.selected_count_label = tk.Label(right_header,
                                             text=f"{len(self.selected_songs)}/5",
                                             font=("Segoe UI", 32, "bold"),
                                             bg=self.colors['bg_card'],
                                             fg=self.colors['primary_red'])
        self.selected_count_label.pack()
        tk.Label(right_header, text="SELECTED",
                font=("Segoe UI", 10), bg=self.colors['bg_card'],
                fg=self.colors['text_muted']).pack()

        # Search bar
        search_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        search_frame.pack(fill="x", padx=40, pady=(20, 10))

        search_inner = tk.Frame(search_frame, bg=self.colors['bg_lighter'])
        search_inner.pack(fill="x")

        tk.Label(search_inner, text="🔍", font=("Segoe UI", 14),
                bg=self.colors['bg_lighter'], fg=self.colors['text_muted']).pack(side="left", padx=(15, 5))

        self.song_search_var = tk.StringVar()

        search_entry = tk.Entry(search_inner, textvariable=self.song_search_var,
                               font=("Segoe UI", 13), bg=self.colors['bg_lighter'],
                               fg=self.colors['text_primary'], relief="flat",
                               insertbackground=self.colors['text_primary'],
                               borderwidth=0, highlightthickness=0)
        search_entry.pack(side="left", fill="x", expand=True, padx=(5, 15), pady=15)
        search_entry.insert(0, "Search songs or artists...")

        def on_focus_in(e):
            if search_entry.get() == "Search songs or artists...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=self.colors['text_primary'])

        def on_focus_out(e):
            if not search_entry.get():
                search_entry.insert(0, "Search songs or artists...")
                search_entry.config(fg=self.colors['text_muted'])

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        search_entry.config(fg=self.colors['text_muted'])

        # Main content
        main_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        main_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # Song list with headers
        list_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        list_frame.pack(fill="both", expand=True)

        # Table header
        header = tk.Frame(list_frame, bg=self.colors['bg_dark'])
        header.pack(fill="x", pady=(0, 10))

        tk.Label(header, text="#", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_dark'], fg=self.colors['text_muted'],
                width=4, anchor="w").pack(side="left", padx=(10, 5))
        tk.Label(header, text="TITLE", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_dark'], fg=self.colors['text_muted'],
                anchor="w", width=40).pack(side="left", padx=5)
        tk.Label(header, text="ARTIST", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_dark'], fg=self.colors['text_muted'],
                anchor="w", width=30).pack(side="left", padx=5)
        tk.Label(header, text="ENERGY", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_dark'], fg=self.colors['text_muted'],
                anchor="center", width=10).pack(side="left", padx=5)
        tk.Label(header, text="TEMPO", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_dark'], fg=self.colors['text_muted'],
                anchor="center", width=10).pack(side="left", padx=5)

        # Separator
        tk.Frame(list_frame, bg=self.colors['bg_lighter'], height=1).pack(fill="x")

        # Scrollable song list
        canvas = tk.Canvas(list_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.songs_container = tk.Frame(canvas, bg=self.colors['bg_dark'])

        self.songs_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.songs_container, anchor="nw", width=1100)
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Display initial songs (first 100)
        self.current_display_songs = self.filtered_songs[:100]
        self.display_songs(self.current_display_songs)

        # Set trace AFTER displaying songs
        self.song_search_var.trace('w', self.on_search_change)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom navigation
        nav_frame = tk.Frame(self.main_container, bg=self.colors['bg_card'])
        nav_frame.pack(fill="x")

        nav_inner = tk.Frame(nav_frame, bg=self.colors['bg_card'])
        nav_inner.pack(pady=20)

        back_btn = self.create_modern_button(nav_inner, "← BACK",
                                             self.show_genre_selection,
                                             bg_color=self.colors['bg_lighter'])
        back_btn.pack(side="left", padx=10)

        next_btn = self.create_modern_button(nav_inner, "CONTINUE →",
                                             self.validate_and_show_use_case)
        next_btn.pack(side="left", padx=10)

    def on_search_change(self, *args):
        """Handle search text changes"""
        search_term = self.song_search_var.get()
        if not search_term or search_term == "Search songs or artists...":
            self.current_display_songs = self.filtered_songs[:100]
            self.display_songs(self.current_display_songs)
            return

        filtered = [s for s in self.filtered_songs
                   if search_term.lower() in s.track_name.lower() or
                   search_term.lower() in s.track_artist.lower()]

        self.current_display_songs = filtered[:100]
        self.display_songs(filtered)

    def load_more_songs(self):
        """Load more songs in batches"""
        current_count = len(self.current_display_songs)
        next_batch = self.filtered_songs[current_count:current_count + 100]

        if next_batch:
            self.current_display_songs.extend(next_batch)
            self.display_songs(self.current_display_songs)

    def display_songs(self, songs):
        """Display songs in the list"""
        # Check if songs_container exists
        if not hasattr(self, 'songs_container'):
            return

        # Clear existing
        for widget in self.songs_container.winfo_children():
            widget.destroy()

        # Display message if no songs
        if not songs:
            no_songs_label = tk.Label(self.songs_container,
                                      text="No songs found matching your search",
                                      font=("Segoe UI", 12),
                                      bg=self.colors['bg_dark'],
                                      fg=self.colors['text_muted'])
            no_songs_label.pack(pady=50)
            return

        # Display songs
        for idx, song in enumerate(songs, 1):
            self.create_song_row(self.songs_container, idx, song)

        # Re-add load more button if needed
        if len(songs) < len(self.filtered_songs):
            load_more_frame = tk.Frame(self.songs_container, bg=self.colors['bg_dark'])
            load_more_frame.pack(pady=20)
            remaining = len(self.filtered_songs) - len(songs)
            self.load_more_btn = self.create_modern_button(load_more_frame,
                                                           f"LOAD MORE ({remaining} remaining)",
                                                           self.load_more_songs)
            self.load_more_btn.pack()

    def create_song_row(self, parent, index, song):
        """Create a song row - Spotify style"""
        is_selected = song in self.selected_songs
        bg_color = self.colors['selected'] if is_selected else self.colors['bg_dark']

        row = tk.Frame(parent, bg=bg_color, cursor="hand2", height=60)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        # Index/Checkbox
        index_frame = tk.Frame(row, bg=bg_color, width=50)
        index_frame.pack(side="left")
        index_frame.pack_propagate(False)

        if is_selected:
            tk.Label(index_frame, text="✓", font=("Segoe UI", 14, "bold"),
                     bg=bg_color, fg=self.colors['success']).pack(expand=True)
        else:
            tk.Label(index_frame, text=str(index), font=("Segoe UI", 11),
                     bg=bg_color, fg=self.colors['text_muted']).pack(expand=True)

        # Title
        title_text = song.track_name[:50] + "..." if len(song.track_name) > 50 else song.track_name
        title_label = tk.Label(row, text=title_text, font=("Segoe UI", 11),
                               bg=bg_color, fg=self.colors['text_primary'],
                               anchor="w", width=40)
        title_label.pack(side="left", padx=5)

        # Artist
        artist_text = song.track_artist[:40] + "..." if len(song.track_artist) > 40 else song.track_artist
        artist_label = tk.Label(row, text=artist_text, font=("Segoe UI", 10),
                                bg=bg_color, fg=self.colors['text_secondary'],
                                anchor="w", width=30)
        artist_label.pack(side="left", padx=5)

        # Energy
        energy_label = tk.Label(row, text=f"{song.energy:.2f}", font=("Segoe UI", 10),
                                bg=bg_color, fg=self.colors['text_secondary'],
                                anchor="center", width=10)
        energy_label.pack(side="left", padx=5)

        # Tempo
        tempo_label = tk.Label(row, text=f"{song.tempo:.0f}", font=("Segoe UI", 10),
                               bg=bg_color, fg=self.colors['text_secondary'],
                               anchor="center", width=10)
        tempo_label.pack(side="left", padx=5)

        # Bind click
        def click_handler(e):
            self.toggle_song_selection_list(song)

        row.bind("<Button-1>", click_handler)
        for child in row.winfo_children():
            child.bind("<Button-1>", click_handler)
            for grandchild in child.winfo_children():
                grandchild.bind("<Button-1>", click_handler)

        # Hover effect
        def on_enter(e):
            if song not in self.selected_songs:
                row.config(bg=self.colors['hover'])
                index_frame.config(bg=self.colors['hover'])
                for widget in [title_label, artist_label, energy_label, tempo_label]:
                    widget.config(bg=self.colors['hover'])
                for child in index_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.colors['hover'])

        def on_leave(e):
            if song not in self.selected_songs:
                row.config(bg=self.colors['bg_dark'])
                index_frame.config(bg=self.colors['bg_dark'])
                for widget in [title_label, artist_label, energy_label, tempo_label]:
                    widget.config(bg=self.colors['bg_dark'])
                for child in index_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.colors['bg_dark'])

        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)

    def toggle_song_selection_list(self, song):
        """Toggle song selection from list"""
        if song in self.selected_songs:
            self.selected_songs.remove(song)
        else:
            if len(self.selected_songs) >= 5:
                messagebox.showwarning("Limit Reached",
                                       "You can only select up to 5 songs.",
                                       parent=self.root)
                return
            self.selected_songs.append(song)

        # Update count
        self.selected_count_label.config(text=f"{len(self.selected_songs)}/5")

        # Refresh display
        search_term = self.song_search_var.get()
        if search_term and search_term != "Search songs or artists...":
            self.on_search_change()
        else:
            self.display_songs(self.current_display_songs)

    def validate_and_show_use_case(self):
        """Validate song selection"""
        if len(self.selected_songs) < 5:
            messagebox.showwarning("Incomplete Selection",
                                   f"Please select 5 songs. You have selected {len(self.selected_songs)}.",
                                   parent=self.root)
            return

        self.show_use_case_selection()

    def show_use_case_selection(self):
        """Show use case selection"""
        self.clear_screen()
        self.current_screen = 3

        # Header
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_card'], height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="STEP 3 OF 3",
                 font=("Segoe UI", 10), bg=self.colors['bg_card'],
                 fg=self.colors['text_muted']).pack(pady=(25, 5))
        tk.Label(header_frame, text="Choose Your Use Case",
                 font=("Segoe UI", 26, "bold"), bg=self.colors['bg_card'],
                 fg=self.colors['text_primary']).pack()

        # Main content
        main_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1200)
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Content
        content_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_dark'])
        content_frame.pack(padx=100, pady=60)

        # Use cases
        use_cases = [
            ("Workout", "🏋️", "High-energy activities, sweat-resistant"),
            ("Casual", "☕", "Daily listening, commuting, relaxation"),
            ("Studio", "🎙️", "Professional audio work, accurate sound"),
            ("Gaming", "🎮", "Gaming sessions, immersive audio")
        ]

        # Cards
        cards_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        cards_frame.pack()

        row = 0
        col = 0
        for use_case, emoji, description in use_cases:
            card = self.create_dark_use_case_card(cards_frame, use_case, emoji, description)
            card.grid(row=row, column=col, padx=30, pady=30)

            col += 1
            if col >= 2:
                col = 0
                row += 1

        # Navigation
        nav_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        nav_frame.pack(pady=30)

        back_btn = self.create_modern_button(nav_frame, "← BACK",
                                             self.show_song_selection,
                                             bg_color=self.colors['bg_lighter'])
        back_btn.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_dark_use_case_card(self, parent, use_case, emoji, description):
        """Create dark themed use case card"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], cursor="hand2",
                        width=420, height=220)
        card.pack_propagate(False)

        # Emoji
        tk.Label(card, text=emoji, font=("Segoe UI Emoji", 70),
                 bg=self.colors['bg_card']).pack(pady=(40, 20))

        # Use case name
        tk.Label(card, text=use_case.upper(), font=("Segoe UI", 20, "bold"),
                 bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack()

        # Description
        tk.Label(card, text=description, font=("Segoe UI", 12),
                 bg=self.colors['bg_card'], fg=self.colors['text_secondary'],
                 wraplength=380).pack(pady=15)

        # Accent line
        accent = tk.Frame(card, bg=self.colors['primary_red'], height=4)
        accent.pack(side="bottom", fill="x")

        # Bind events
        def click_handler(e):
            self.select_use_case(use_case)

        card.bind("<Button-1>", click_handler)
        for child in card.winfo_children():
            child.bind("<Button-1>", click_handler)

        def on_enter(e):
            card.config(bg=self.colors['hover'])
            for child in card.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.colors['hover'])

        def on_leave(e):
            card.config(bg=self.colors['bg_card'])
            for child in card.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.colors['bg_card'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def select_use_case(self, use_case):
        """Handle use case selection"""
        self.selected_use_case = use_case
        print(f"Selected use case: {use_case}")
        self.generate_recommendations()

    def generate_recommendations(self):
        """Generate headphone recommendations"""
        print("\n=== Generating Recommendations ===")
        print(f"Genre: {self.selected_genre}")
        print(f"Songs: {len(self.selected_songs)}")
        print(f"Use Case: {self.selected_use_case}")

        # Calculate averages
        avg_energy = sum([s.energy for s in self.selected_songs]) / len(self.selected_songs)
        avg_bass = sum([s.loudness for s in self.selected_songs]) / len(self.selected_songs)
        avg_tempo = sum([s.tempo for s in self.selected_songs]) / len(self.selected_songs)

        print(f"Avg Energy: {avg_energy:.2f}")
        print(f"Avg Bass: {avg_bass:.2f}")
        print(f"Avg Tempo: {avg_tempo:.0f}")

        # Filter and score
        matching_headphones = [hp for hp in self.headphones
                               if hp.use_case.lower() == self.selected_use_case.lower()]

        scored_headphones = []
        for hp in matching_headphones:
            score = 0

            if avg_bass > -4 and hp.bass_level == "High":
                score += 3
            elif avg_bass < -7 and hp.bass_level == "Low":
                score += 3
            elif hp.bass_level == "Medium":
                score += 2

            if avg_energy > 0.7 and hp.sound_profile == "Bass-heavy":
                score += 2
            elif avg_energy < 0.4 and hp.sound_profile == "Flat":
                score += 2
            else:
                score += 1

            score += hp.user_rating
            scored_headphones.append((hp, score))

        scored_headphones.sort(key=lambda x: x[1], reverse=True)

        # Categorize
        budget = [hp for hp, score in scored_headphones if hp.price < 150][:3]
        premium = [hp for hp, score in scored_headphones if hp.price > 400][:3]
        balanced = [hp for hp, score in scored_headphones if 150 <= hp.price <= 400][:3]

        recommendations = {
            "Budget-Friendly": budget,
            "Best of the Line": premium,
            "Best of Both": balanced
        }

        all_recommended = budget + premium + balanced
        most_reviewed = max(all_recommended,
                            key=lambda hp: hp.user_rating * hp.user_reviews) if all_recommended else None

        self.show_recommendations(recommendations, most_reviewed)

    def show_recommendations(self, recommendations, most_reviewed):
        """Show recommendations - dark theme"""
        self.clear_screen()

        # Header
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_card'])
        header_frame.pack(fill="x")

        header_inner = tk.Frame(header_frame, bg=self.colors['bg_card'])
        header_inner.pack(pady=30)

        tk.Label(header_inner, text="✨", font=("Segoe UI Emoji", 40),
                 bg=self.colors['bg_card']).pack()
        tk.Label(header_inner, text="Your Perfect Headphones",
                 font=("Segoe UI", 32, "bold"), bg=self.colors['bg_card'],
                 fg=self.colors['text_primary']).pack(pady=(10, 5))
        tk.Label(header_inner, text=f"Based on {self.selected_genre} • {self.selected_use_case}",
                 font=("Segoe UI", 13), bg=self.colors['bg_card'],
                 fg=self.colors['text_secondary']).pack()

        # Main content
        main_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])

        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw", width=1160)
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Most reviewed
        if most_reviewed:
            featured_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
            featured_frame.pack(padx=40, pady=30)

            tk.Label(featured_frame, text="⭐ MOST POSITIVELY REVIEWED",
                     font=("Segoe UI", 14, "bold"), bg=self.colors['bg_dark'],
                     fg=self.colors['warning']).pack(pady=(0, 15))

            self.create_dark_headphone_card(featured_frame, most_reviewed, True)

        # Categories
        for category, headphones in recommendations.items():
            if not headphones:
                continue

            cat_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
            cat_frame.pack(padx=40, pady=20, fill="x")

            tk.Label(cat_frame, text=category.upper(),
                     font=("Segoe UI", 14, "bold"), bg=self.colors['bg_dark'],
                     fg=self.colors['primary_red']).pack(anchor="w", pady=(0, 15))

            for hp in headphones:
                self.create_dark_headphone_card(cat_frame, hp, False)

        # Restart button
        nav_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        nav_frame.pack(pady=40)

        restart_btn = self.create_gradient_button(nav_frame, "🔄 START OVER",
                                                  self.restart, width=250)
        restart_btn.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_dark_headphone_card(self, parent, headphone, highlight=False):
        """Create dark themed headphone card"""
        bg_color = self.colors['bg_card'] if not highlight else self.colors['bg_lighter']

        card = tk.Frame(parent, bg=bg_color)
        card.pack(fill="x", pady=10)

        content = tk.Frame(card, bg=bg_color)
        content.pack(padx=30, pady=25)

        # Header
        header = tk.Frame(content, bg=bg_color)
        header.pack(fill="x", pady=(0, 15))

        tk.Label(header, text=f"{headphone.brand} {headphone.model}",
                 font=("Segoe UI", 16, "bold"), bg=bg_color,
                 fg=self.colors['text_primary']).pack(side="left")

        tk.Label(header, text=f"${headphone.price:.0f}",
                 font=("Segoe UI", 16, "bold"), bg=bg_color,
                 fg=self.colors['success']).pack(side="right")

        # Rating
        stars = "⭐" * int(headphone.user_rating)
        tk.Label(content, text=f"{stars} {headphone.user_rating}/5.0 ({headphone.user_reviews:,} reviews)",
                 font=("Segoe UI", 11), bg=bg_color,
                 fg=self.colors['warning']).pack(anchor="w", pady=(0, 15))

        # Specs
        specs_frame = tk.Frame(content, bg=bg_color)
        specs_frame.pack(fill="x")

        specs = [
            ("TYPE", headphone.hp_type),
            ("BASS", headphone.bass_level),
            ("PROFILE", headphone.sound_profile),
            ("ANC", "Yes" if headphone.noise_cancellation else "No")
        ]

        for label, value in specs:
            spec = tk.Frame(specs_frame, bg=self.colors['bg_dark'])
            spec.pack(side="left", padx=(0, 15))

            tk.Label(spec, text=label, font=("Segoe UI", 9),
                     bg=self.colors['bg_dark'], fg=self.colors['text_muted']).pack(padx=15, pady=(10, 2))
            tk.Label(spec, text=value, font=("Segoe UI", 11, "bold"),
                     bg=self.colors['bg_dark'], fg=self.colors['text_primary']).pack(padx=15, pady=(2, 10))

    def restart(self):
        """Restart application"""
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.filtered_songs = []
        self.current_display_songs = []
        self.show_welcome_screen()

def main():
    root = tk.Tk()
    app = MusicMatchApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()