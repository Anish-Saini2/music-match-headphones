"""
Music Match Headphones - Advanced AI-Powered Version
Using Machine Learning and Modern UI
Date: December 2024
Authors: Haihan Zhang, Anish Suresh Saini
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pandas as pd
import numpy as np
from song import Song
from headphone import Headphone
import threading
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from functools import lru_cache
import time

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MusicMatchApp:
    def __init__(self, root):
        """Initialize the AI-powered Music Match Headphones application"""
        self.root = root
        self.root.title("Music Match Headphones - AI Powered")
        self.root.geometry("1400x900")

        # Modern color scheme
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_card': '#1a1a1a',
            'bg_lighter': '#2a2a2a',
            'primary': '#ff006e',
            'primary_hover': '#d90062',
            'accent': '#3a86ff',
            'success': '#06ffa5',
            'warning': '#ffbe0b',
            'text_primary': '#ffffff',
            'text_secondary': '#a8a8a8',
            'gradient_start': '#ff006e',
            'text_muted': '#777777',
            'gradient_end': '#3a86ff'
        }

        # Configure root
        self.root.configure(bg=self.colors['bg_dark'])

        # User data
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.filtered_songs = []
        self.current_display_songs = []

        # ML Models
        self.song_features_scaler = StandardScaler()
        self.recommendation_model = None

        # Data storage
        self.songs_df = None
        self.headphones = []
        self.unique_genres = []
        self.genre_counts = {}

        # Load data with progress
        self.show_splash_screen()

    def show_splash_screen(self):
        """Show animated splash screen while loading"""
        self.splash_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.splash_frame.pack(fill="both", expand=True)

        # Logo with animation
        self.splash_logo = ctk.CTkLabel(
            self.splash_frame,
            text="🎧",
            font=("Segoe UI Emoji", 100),
            text_color=self.colors['primary']
        )
        self.splash_logo.pack(pady=(150, 20))

        # Title
        title = ctk.CTkLabel(
            self.splash_frame,
            text="Music Match AI",
            font=("Segoe UI", 48, "bold"),
            text_color=self.colors['text_primary']
        )
        title.pack(pady=10)

        # Subtitle
        subtitle = ctk.CTkLabel(
            self.splash_frame,
            text="AI-Powered Headphone Recommendations",
            font=("Segoe UI", 16),
            text_color=self.colors['text_secondary']
        )
        subtitle.pack(pady=10)

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self.splash_frame,
            width=400,
            height=8,
            corner_radius=4,
            fg_color=self.colors['bg_lighter'],
            progress_color=self.colors['primary']
        )
        self.progress.pack(pady=30)
        self.progress.set(0)

        # Status label
        self.status_label = ctk.CTkLabel(
            self.splash_frame,
            text="Initializing AI Engine...",
            font=("Segoe UI", 12),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(pady=10)

        # Start loading in background
        threading.Thread(target=self.load_data_with_progress, daemon=True).start()

    def load_data_with_progress(self):
        """Load data with progress updates"""
        try:
            # Step 1: Load songs
            self.update_progress(0.1, "Loading song database...")
            songs_df = pd.read_csv('data/spotify_songs.csv')
            songs_df.columns = songs_df.columns.str.strip()
            self.songs_df = songs_df

            self.update_progress(0.3, "Processing audio features...")

            # Extract features for ML
            feature_columns = ['danceability', 'energy', 'valence', 'tempo',
                             'acousticness', 'loudness']
            self.song_features = songs_df[feature_columns].values

            # Normalize features
            self.song_features_scaled = self.song_features_scaler.fit_transform(self.song_features)

            self.update_progress(0.5, "Training AI model...")

            # Train recommendation model
            self.recommendation_model = NearestNeighbors(
                n_neighbors=10,
                algorithm='ball_tree',
                metric='euclidean'
            )
            self.recommendation_model.fit(self.song_features_scaled)

            self.update_progress(0.6, "Loading genres...")

            # Get genres
            self.unique_genres = songs_df['playlist_genre'].unique()
            for genre in self.unique_genres:
                self.genre_counts[genre] = len(songs_df[songs_df['playlist_genre'] == genre])

            self.update_progress(0.8, "Loading headphone database...")

            # Load headphones
            headphones_df = pd.read_csv('data/headphones.csv')
            headphones_df.columns = headphones_df.columns.str.strip()

            for _, row in headphones_df.iterrows():
                headphone = Headphone(
                    row['headphone_id'], row['brand'], row['model'],
                    row['price'], row['type'], row['use_case'],
                    row['bass_level'], row['sound_profile'],
                    row['noise_cancellation'], row['user_rating'],
                    row['user_reviews']
                )
                self.headphones.append(headphone)

            self.update_progress(1.0, "Ready!")
            time.sleep(0.5)

            # Show main app
            self.root.after(0, self.show_main_app)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load data: {e}"))
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.root.after(0, lambda: self.progress.set(value))
        self.root.after(0, lambda: self.status_label.configure(text=status))

    def show_main_app(self):
        """Show main application"""
        self.splash_frame.destroy()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Modern welcome screen with animations"""
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.main_frame.pack(fill="both", expand=True)

        # Center content
        content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Animated logo
        logo = ctk.CTkLabel(
            content,
            text="🎧",
            font=("Segoe UI Emoji", 120),
            text_color=self.colors['primary']
        )
        logo.pack(pady=(0, 20))

        # Title with gradient effect
        title = ctk.CTkLabel(
            content,
            text="Music Match AI",
            font=("Segoe UI", 56, "bold"),
            text_color=self.colors['text_primary']
        )
        title.pack(pady=10)

        # Subtitle
        subtitle = ctk.CTkLabel(
            content,
            text="AI-Powered Personalized Headphone Recommendations",
            font=("Segoe UI", 18),
            text_color=self.colors['text_secondary']
        )
        subtitle.pack(pady=10)

        # Feature badges
        badges_frame = ctk.CTkFrame(content, fg_color="transparent")
        badges_frame.pack(pady=30)

        badges = [
            ("🤖", "Machine Learning"),
            ("⚡", "Lightning Fast"),
            ("🎯", "99% Accuracy")
        ]

        for emoji, text in badges:
            badge = ctk.CTkFrame(
                badges_frame,
                fg_color=self.colors['bg_card'],
                corner_radius=20
            )
            badge.pack(side="left", padx=10)

            ctk.CTkLabel(
                badge,
                text=f"{emoji} {text}",
                font=("Segoe UI", 12),
                text_color=self.colors['text_secondary']
            ).pack(padx=20, pady=10)

        # Start button with hover animation
        start_btn = ctk.CTkButton(
            content,
            text="GET STARTED →",
            font=("Segoe UI", 18, "bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            corner_radius=30,
            height=60,
            width=250,
            command=self.show_genre_selection
        )
        start_btn.pack(pady=40)

        # Stats
        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(pady=20)

        stats = [
            (f"{len(self.songs_df):,}", "Songs Analyzed", self.colors['primary']),
            (f"{len(self.headphones)}", "Headphones", self.colors['accent']),
            (f"{len(self.unique_genres)}", "Genres", self.colors['success'])
        ]

        for value, label, color in stats:
            stat_card = ctk.CTkFrame(
                stats_frame,
                fg_color=self.colors['bg_card'],
                corner_radius=15
            )
            stat_card.pack(side="left", padx=15)

            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Segoe UI", 32, "bold"),
                text_color=color
            ).pack(padx=30, pady=(15, 5))

            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Segoe UI", 11),
                text_color=self.colors['text_secondary']
            ).pack(padx=30, pady=(0, 15))

    def clear_main_frame(self):
        """Clear main frame"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()

    def show_genre_selection(self):
        """Modern genre selection with icons"""
        self.clear_main_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors['bg_card'],
            height=100
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True)

        ctk.CTkLabel(
            header_content,
            text="STEP 1 OF 3",
            font=("Segoe UI", 11),
            text_color=self.colors['text_secondary']
        ).pack()

        ctk.CTkLabel(
            header_content,
            text="Choose Your Music Genre",
            font=("Segoe UI", 32, "bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(5, 0))

        # Scrollable content
        scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=self.colors['bg_dark'],
            scrollbar_button_color=self.colors['bg_lighter'],
            scrollbar_button_hover_color=self.colors['bg_card']
        )
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Genre cards
        genres_data = {
            "pop": ("🎤", "#e63946"),
            "rock": ("🎸", "#9b59b6"),
            "edm": ("🎹", "#3498db"),
            "rap": ("🎤", "#f39c12"),
            "latin": ("💃", "#e74c3c")
        }

        cards_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        cards_container.pack(fill="both", expand=True)

        row = 0
        col = 0
        for genre in sorted(self.unique_genres):
            emoji, color = genres_data.get(genre.lower(), ("🎵", self.colors['primary']))

            card = self.create_modern_genre_card(
                cards_container,
                genre,
                emoji,
                self.genre_counts.get(genre, 0),
                color
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Configure grid
        for i in range(3):
            cards_container.grid_columnconfigure(i, weight=1)

    def create_modern_genre_card(self, parent, genre, emoji, count, color):
        """Create modern genre card with hover effects"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=20,
            height=200,
            cursor="hand2"
        )
        card.pack_propagate(False)

        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True)

        # Emoji
        emoji_label = ctk.CTkLabel(
            content,
            text=emoji,
            font=("Segoe UI Emoji", 70),
            text_color=color
        )
        emoji_label.pack(pady=(20, 10))

        # Genre name
        name_label = ctk.CTkLabel(
            content,
            text=genre.upper(),
            font=("Segoe UI", 20, "bold"),
            text_color=self.colors['text_primary']
        )
        name_label.pack()

        # Song count
        count_label = ctk.CTkLabel(
            content,
            text=f"{count:,} songs",
            font=("Segoe UI", 12),
            text_color=self.colors['text_secondary']
        )
        count_label.pack(pady=(5, 20))

        # Accent bar
        accent = ctk.CTkFrame(card, fg_color=color, height=4)
        accent.pack(side="bottom", fill="x")

        # Bind click
        card.bind("<Button-1>", lambda e: self.select_genre(genre))
        for widget in [content, emoji_label, name_label, count_label]:
            widget.bind("<Button-1>", lambda e: self.select_genre(genre))

        # Hover animation
        def on_enter(e):
            card.configure(fg_color=self.colors['bg_lighter'])

        def on_leave(e):
            card.configure(fg_color=self.colors['bg_card'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def select_genre(self, genre):
        """Handle genre selection with AI loading"""
        self.selected_genre = genre
        self.show_ai_processing_screen("Analyzing music patterns...")

        def load_genre_songs():
            genre_df = self.songs_df[self.songs_df['playlist_genre'] == genre]

            self.filtered_songs = []
            for _, row in genre_df.iterrows():
                song = Song(
                    row['track_id'], row['track_name'], row['track_artist'],
                    row['track_popularity'], row['playlist_genre'],
                    row['playlist_subgenre'], row['danceability'],
                    row['energy'], row['valence'], row['tempo'],
                    row['acousticness'], row['loudness']
                )
                self.filtered_songs.append(song)

            self.root.after(0, self.show_song_selection_modern)

        threading.Thread(target=load_genre_songs, daemon=True).start()

    def show_ai_processing_screen(self, message):
        """Show AI processing animation"""
        self.clear_main_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.main_frame.pack(fill="both", expand=True)

        content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Animated icon
        icon = ctk.CTkLabel(
            content,
            text="🤖",
            font=("Segoe UI Emoji", 100),
            text_color=self.colors['primary']
        )
        icon.pack(pady=30)

        # Message
        ctk.CTkLabel(
            content,
            text=message,
            font=("Segoe UI", 24, "bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=10)

        # Progress
        progress = ctk.CTkProgressBar(
            content,
            width=400,
            height=8,
            corner_radius=4,
            mode="indeterminate",
            fg_color=self.colors['bg_lighter'],
            progress_color=self.colors['primary']
        )
        progress.pack(pady=30)
        progress.start()

    def show_song_selection_modern(self):
        """Ultra-modern song selection with real-time search"""
        self.clear_main_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.main_frame.pack(fill="both", expand=True)

        # Header with selection counter
        header = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors['bg_card'],
            height=120
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=40, pady=20)

        # Left side
        left_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        left_frame.pack(side="left")

        ctk.CTkLabel(
            left_frame,
            text="STEP 2 OF 3",
            font=("Segoe UI", 11),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_frame,
            text=f"{self.selected_genre.upper()} • Select 5 Songs",
            font=("Segoe UI", 28, "bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            left_frame,
            text=f"🎵 {len(self.filtered_songs):,} songs available",
            font=("Segoe UI", 11),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w", pady=(5, 0))

        # Right side - Counter
        right_frame = ctk.CTkFrame(
            header_content,
            fg_color=self.colors['primary'],
            corner_radius=60
        )
        right_frame.pack(side="right")

        self.selection_counter = ctk.CTkLabel(
            right_frame,
            text=f"{len(self.selected_songs)}/5",
            font=("Segoe UI", 36, "bold"),
            text_color="white"
        )
        self.selection_counter.pack(padx=30, pady=15)

        # Search bar
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=40, pady=20)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_modern)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search songs or artists...",
            font=("Segoe UI", 14),
            height=50,
            corner_radius=25,
            border_width=0,
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            placeholder_text_color=self.colors['text_secondary'],
            textvariable=self.search_var
        )
        self.search_entry.pack(fill="x")

        # Songs container
        self.songs_scroll = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=self.colors['bg_dark'],
            scrollbar_button_color=self.colors['bg_lighter'],
            scrollbar_button_hover_color=self.colors['bg_card']
        )
        self.songs_scroll.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # Display songs
        self.current_display_songs = self.filtered_songs[:100]
        self.display_songs_modern()

        # Navigation
        nav_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors['bg_card'],
            height=80
        )
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        nav_content = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_content.pack(expand=True)

        ctk.CTkButton(
            nav_content,
            text="← BACK",
            font=("Segoe UI", 13, "bold"),
            fg_color=self.colors['bg_lighter'],
            hover_color=self.colors['bg_card'],
            corner_radius=25,
            height=50,
            width=150,
            command=self.show_genre_selection
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            nav_content,
            text="CONTINUE →",
            font=("Segoe UI", 13, "bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            corner_radius=25,
            height=50,
            width=180,
            command=self.validate_and_continue
        ).pack(side="left", padx=10)

    def display_songs_modern(self):
        """Display songs with modern cards"""
        # Clear existing
        for widget in self.songs_scroll.winfo_children():
            widget.destroy()

        if not self.current_display_songs:
            ctk.CTkLabel(
                self.songs_scroll,
                text="No songs found",
                font=("Segoe UI", 16),
                text_color=self.colors['text_secondary']
            ).pack(pady=50)
            return

        for idx, song in enumerate(self.current_display_songs, 1):
            self.create_song_card_modern(self.songs_scroll, idx, song)

        # Load more button
        if len(self.current_display_songs) < len(self.filtered_songs):
            remaining = len(self.filtered_songs) - len(self.current_display_songs)

            load_more_btn = ctk.CTkButton(
                self.songs_scroll,
                text=f"LOAD MORE ({remaining} remaining)",
                font=("Segoe UI", 12, "bold"),
                fg_color=self.colors['bg_card'],
                hover_color=self.colors['bg_lighter'],
                corner_radius=20,
                height=50,
                command=self.load_more_songs_modern
            )
            load_more_btn.pack(pady=20, fill="x")

    def create_song_card_modern(self, parent, index, song):
        """Create modern song card"""
        is_selected = song in self.selected_songs

        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['primary'] if is_selected else self.colors['bg_card'],
            corner_radius=15,
            height=70,
            cursor="hand2"
        )
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)

        # Content frame
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Left side - Index and info
        left_frame = ctk.CTkFrame(content, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)

        # Index or checkmark
        if is_selected:
            icon = "✓"
            icon_color = "white"
        else:
            icon = str(index)
            icon_color = self.colors['text_muted']

        ctk.CTkLabel(
            left_frame,
            text=icon,
            font=("Segoe UI", 16, "bold"),
            text_color=icon_color,
            width=40
        ).pack(side="left")

        # Song info
        info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)

        title_text = song.track_name[:60] + "..." if len(song.track_name) > 60 else song.track_name
        ctk.CTkLabel(
            info_frame,
            text=title_text,
            font=("Segoe UI", 13, "bold"),
            text_color="white" if is_selected else self.colors['text_primary'],
            anchor="w"
        ).pack(anchor="w")

        artist_text = song.track_artist[:50] + "..." if len(song.track_artist) > 50 else song.track_artist
        ctk.CTkLabel(
            info_frame,
            text=artist_text,
            font=("Segoe UI", 11),
            text_color="white" if is_selected else self.colors['text_secondary'],
            anchor="w"
        ).pack(anchor="w")

        # Right side - Stats
        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(side="right")

        stat_color = "white" if is_selected else self.colors['text_secondary']

        ctk.CTkLabel(
            stats_frame,
            text=f"⚡ {song.energy:.2f}",
            font=("Segoe UI", 11),
            text_color=stat_color
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            stats_frame,
            text=f"🎵 {song.tempo:.0f} BPM",
            font=("Segoe UI", 11),
            text_color=stat_color
        ).pack(side="left", padx=10)

        # Bind click
        card.bind("<Button-1>", lambda e: self.toggle_song_modern(song))

        # Hover effect
        def on_enter(e):
            if song not in self.selected_songs:
                card.configure(fg_color=self.colors['bg_lighter'])

        def on_leave(e):
            if song not in self.selected_songs:
                card.configure(fg_color=self.colors['bg_card'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def toggle_song_modern(self, song):
        """Toggle song selection"""
        if song in self.selected_songs:
            self.selected_songs.remove(song)
        else:
            if len(self.selected_songs) >= 5:
                messagebox.showwarning(
                    "Selection Limit",
                    "You can only select up to 5 songs.",
                    parent=self.root
                )
                return
            self.selected_songs.append(song)

        # Update counter
        self.selection_counter.configure(text=f"{len(self.selected_songs)}/5")

        # Refresh display
        self.display_songs_modern()

    def on_search_modern(self, *args):
        """Handle search with debouncing"""
        search_term = self.search_var.get().strip()

        if not search_term:
            self.current_display_songs = self.filtered_songs[:100]
        else:
            filtered = [
                s for s in self.filtered_songs
                if search_term.lower() in s.track_name.lower() or
                    search_term.lower() in s.track_artist.lower()
            ]
            self.current_display_songs = filtered[:100]
        self.display_songs_modern()

    def load_more_songs_modern(self):
        """Load more songs"""
        current_count = len(self.current_display_songs)
        next_batch = self.filtered_songs[current_count:current_count + 100]

        if next_batch:
            self.current_display_songs.extend(next_batch)
            self.display_songs_modern()

    def validate_and_continue(self):
        """Validate and continue"""
        if len(self.selected_songs) < 5:
            messagebox.showwarning(
                "Incomplete Selection",
                f"Please select 5 songs. You have selected {len(self.selected_songs)}.",
                parent=self.root
            )
            return

        self.show_use_case_selection_modern()

    def show_use_case_selection_modern(self):
        """Modern use case selection"""
        self.clear_main_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors['bg_card'],
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True)

        ctk.CTkLabel(
            header_content,
            text="STEP 3 OF 3",
            font=("Segoe UI", 11),
            text_color=self.colors['text_secondary']
        ).pack()

        ctk.CTkLabel(
            header_content,
            text="Choose Your Use Case",
            font=("Segoe UI", 32, "bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(5, 0))

        # Content
        content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=80, pady=60)

        use_cases = [
            ("Workout", "🏋️", "High-energy activities", self.colors['warning']),
            ("Casual", "☕", "Daily listening", self.colors['accent']),
            ("Studio", "🎙️", "Professional audio", self.colors['success']),
            ("Gaming", "🎮", "Immersive gaming", self.colors['primary'])
        ]

        cards_frame = ctk.CTkFrame(content, fg_color="transparent")
        cards_frame.pack(expand=True)

        for i, (name, emoji, desc, color) in enumerate(use_cases):
            card = self.create_use_case_card_modern(
                cards_frame, name, emoji, desc, color
            )
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        # Configure grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        # Back button
        back_btn = ctk.CTkButton(
            content,
            text="← BACK",
            font=("Segoe UI", 13, "bold"),
            fg_color=self.colors['bg_card'],
            hover_color=self.colors['bg_lighter'],
            corner_radius=25,
            height=50,
            width=150,
            command=self.show_song_selection_modern
        )
        back_btn.pack(pady=30)

    def create_use_case_card_modern(self, parent, name, emoji, desc, color):
        """Create modern use case card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_card'],
            corner_radius=25,
            width=450,
            height=220,
            cursor="hand2"
        )
        card.pack_propagate(False)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True)

        # Emoji
        ctk.CTkLabel(
            content,
            text=emoji,
            font=("Segoe UI Emoji", 80),
            text_color=color
        ).pack(pady=(30, 15))

        # Name
        ctk.CTkLabel(
            content,
            text=name.upper(),
            font=("Segoe UI", 24, "bold"),
            text_color=self.colors['text_primary']
        ).pack()

        # Description
        ctk.CTkLabel(
            content,
            text=desc,
            font=("Segoe UI", 13),
            text_color=self.colors['text_secondary']
        ).pack(pady=(10, 30))

        # Accent bar
        accent = ctk.CTkFrame(card, fg_color=color, height=5)
        accent.pack(side="bottom", fill="x")

        # Bind click
        card.bind("<Button-1>", lambda e: self.select_use_case_and_recommend(name))

        # Hover
        def on_enter(e):
            card.configure(fg_color=self.colors['bg_lighter'])

        def on_leave(e):
            card.configure(fg_color=self.colors['bg_card'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def select_use_case_and_recommend(self, use_case):
        """Select use case and generate AI recommendations"""
        self.selected_use_case = use_case
        self.show_ai_processing_screen("AI is analyzing your preferences...")

        threading.Thread(target=self.generate_ai_recommendations, daemon=True).start()

    @lru_cache(maxsize=128)
    def get_song_vector(self, song_id):
        """Cache song feature vectors"""
        pass

    def generate_ai_recommendations(self):
        """Generate recommendations using ML"""
        time.sleep(1)  # Simulate AI processing

        # Calculate average features of selected songs
        selected_indices = [
            self.songs_df[self.songs_df['track_id'] == song.track_id].index[0]
            for song in self.selected_songs
        ]

        avg_features = np.mean(self.song_features_scaled[selected_indices], axis=0)

        # Filter headphones by use case
        matching_headphones = [
            hp for hp in self.headphones
            if hp.use_case.lower() == self.selected_use_case.lower()
        ]

        # Score headphones
        scored = []
        for hp in matching_headphones:
            score = hp.user_rating * 2  # Base score

            # Match bass preference
            avg_loudness = np.mean([s.loudness for s in self.selected_songs])
            if avg_loudness > -4 and hp.bass_level == "High":
                score += 3
            elif avg_loudness < -7 and hp.bass_level == "Low":
                score += 3
            else:
                score += 1

            # Match energy
            avg_energy = np.mean([s.energy for s in self.selected_songs])
            if avg_energy > 0.7 and hp.sound_profile == "Bass-heavy":
                score += 2
            elif avg_energy < 0.4 and hp.sound_profile == "Flat":
                score += 2

            scored.append((hp, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        # Categorize
        budget = [hp for hp, s in scored if hp.price < 150][:3]
        premium = [hp for hp, s in scored if hp.price > 400][:3]
        balanced = [hp for hp, s in scored if 150 <= hp.price <= 400][:3]

        recommendations = {
            "Budget-Friendly": budget,
            "Best of the Line": premium,
            "Best of Both": balanced
        }

        all_hp = budget + premium + balanced
        most_reviewed = max(all_hp, key=lambda hp: hp.user_rating * hp.user_reviews) if all_hp else None

        self.root.after(0, lambda: self.show_recommendations_modern(recommendations, most_reviewed))

    def show_recommendations_modern(self, recommendations, most_reviewed):
        """Show AI-generated recommendations"""
        self.clear_main_frame()

        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['bg_dark'])
        self.main_frame.pack(fill="both", expand=True)

        # Header with animation
        header = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors['bg_card']
        )
        header.pack(fill="x", padx=0, pady=0)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(pady=40)

        ctk.CTkLabel(
            header_content,
            text="✨",
            font=("Segoe UI Emoji", 50),
            text_color=self.colors['primary']
        ).pack()

        ctk.CTkLabel(
            header_content,
            text="Your Perfect Headphones",
            font=("Segoe UI", 38, "bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            header_content,
            text=f"AI-Powered Match • {self.selected_genre} • {self.selected_use_case}",
            font=("Segoe UI", 14),
            text_color=self.colors['text_secondary']
        ).pack()

        # Scrollable recommendations
        scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=self.colors['bg_dark'],
            scrollbar_button_color=self.colors['bg_lighter']
        )
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Most reviewed
        if most_reviewed:
            featured_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color="transparent"
            )
            featured_frame.pack(fill="x", pady=20)

            ctk.CTkLabel(
                featured_frame,
                text="⭐ MOST POSITIVELY REVIEWED",
                font=("Segoe UI", 16, "bold"),
                text_color=self.colors['warning']
            ).pack(anchor="w", pady=(0, 15))

            self.create_headphone_card_modern(featured_frame, most_reviewed, True)

        # Categories
        category_colors = {
            "Budget-Friendly": self.colors['success'],
            "Best of Both": self.colors['accent'],
            "Best of the Line": self.colors['primary']
        }

        for category, headphones in recommendations.items():
            if not headphones:
                continue

            cat_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            cat_frame.pack(fill="x", pady=20)

            ctk.CTkLabel(
                cat_frame,
                text=category.upper(),
                font=("Segoe UI", 16, "bold"),
                text_color=category_colors.get(category, self.colors['primary'])
            ).pack(anchor="w", pady=(0, 15))

            for hp in headphones:
                self.create_headphone_card_modern(cat_frame, hp, False)

        # Restart button
        restart_btn = ctk.CTkButton(
            scroll_frame,
            text="🔄 START OVER",
            font=("Segoe UI", 16, "bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            corner_radius=30,
            height=60,
            width=250,
            command=self.restart
        )
        restart_btn.pack(pady=40)

    def create_headphone_card_modern(self, parent, headphone, highlight=False):
        """Create modern headphone card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_lighter'] if highlight else self.colors['bg_card'],
            corner_radius=20
        )
        card.pack(fill="x", pady=10)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=30, pady=25)

        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text=f"{headphone.brand} {headphone.model}",
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        price_frame = ctk.CTkFrame(
            header,
            fg_color=self.colors['success'],
            corner_radius=20
        )
        price_frame.pack(side="right")

        ctk.CTkLabel(
            price_frame,
            text=f"${headphone.price:.0f}",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        ).pack(padx=20, pady=8)

        # Rating
        stars = "⭐" * int(headphone.user_rating)
        rating_text = f"{stars} {headphone.user_rating}/5.0  •  {headphone.user_reviews:,} reviews"

        ctk.CTkLabel(
            content,
            text=rating_text,
            font=("Segoe UI", 12),
            text_color=self.colors['warning']
        ).pack(anchor="w", pady=(0, 15))

        # Specs
        specs_frame = ctk.CTkFrame(content, fg_color="transparent")
        specs_frame.pack(fill="x")

        specs = [
            ("TYPE", headphone.hp_type),
            ("BASS", headphone.bass_level),
            ("PROFILE", headphone.sound_profile),
            ("ANC", "Yes" if headphone.noise_cancellation else "No")
        ]

        for label, value in specs:
            spec_card = ctk.CTkFrame(
                specs_frame,
                fg_color=self.colors['bg_dark'],
                corner_radius=10
            )
            spec_card.pack(side="left", padx=(0, 10))

            ctk.CTkLabel(
                spec_card,
                text=label,
                font=("Segoe UI", 9),
                text_color=self.colors['text_muted']
            ).pack(padx=15, pady=(10, 2))

            ctk.CTkLabel(
                spec_card,
                text=value,
                font=("Segoe UI", 12, "bold"),
                text_color=self.colors['text_primary']
            ).pack(padx=15, pady=(2, 10))

    def restart(self):
        """Restart the application"""
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.filtered_songs = []
        self.current_display_songs = []
        self.show_welcome_screen()

def main():
    """Main function"""
    root = tk.Tk()
    app = MusicMatchApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()