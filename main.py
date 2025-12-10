"""
Music Match Headphones - One Page Application (Standalone)
Modern styled with dark theme and red accents
Authors: Haihan Zhang, Anish Suresh Saini
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import numpy as np
from song import Song
from headphone import Headphone
import threading

class RecommendationEngine:
    """Simple recommendation engine"""

    def __init__(self, headphones):
        self.headphones = headphones

    def generate_recommendations(self, selected_songs, use_case):
        """Generate recommendations"""
        # Calculate averages
        avg_energy = np.mean([s.energy for s in selected_songs])
        avg_loudness = np.mean([s.loudness for s in selected_songs])

        # Filter by use case
        matching = [hp for hp in self.headphones
                   if hp.use_case.lower() == use_case.lower()]

        # Score headphones
        scored = []
        for hp in matching:
            score = hp.user_rating * 2

            # Bass matching
            if avg_loudness > -4 and hp.bass_level == "High":
                score += 3
            elif avg_loudness < -7 and hp.bass_level == "Low":
                score += 3
            else:
                score += 1

            # Energy matching
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

        # Most reviewed
        all_hp = budget + premium + balanced
        most_reviewed = max(all_hp, key=lambda hp: hp.user_rating * hp.user_reviews) if all_hp else None

        return recommendations, most_reviewed

class MusicMatchOnePageApp:
    """One-page application with modern styling"""

    def __init__(self, root):
        self.root = root
        self.root.title("Music Match Headphones - Recommendation System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a0a")

        # Modern dark theme with red accents
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_card': '#1a1a1a',
            'bg_lighter': '#2a2a2a',
            'bg_hover': '#353535',
            'primary_red': '#ff006e',
            'primary_red_dark': '#d90062',
            'accent_red': '#e63946',
            'gradient_start': '#ff006e',
            'gradient_end': '#8b0000',
            'success': '#06ffa5',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'text_muted': '#6a6a6a',
            'border': '#333333'
        }

        # Data
        self.songs_df = None
        self.headphones = []
        self.genre_counts = {}
        self.unique_genres = []
        self.recommendation_engine = None
        self.selected_genre = None
        self.selected_songs = []
        self.selected_song_ids = set()
        self.selected_use_case = None
        self.filtered_songs = []
        self.current_display_songs = []

        # Load data
        self.load_data_background()

    def load_data_background(self):
        """Load data in background"""
        self.show_loading_splash()
        threading.Thread(target=self.load_data, daemon=True).start()

    def show_loading_splash(self):
        """Show loading overlay"""
        self.splash = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.splash.place(relx=0, rely=0, relwidth=1, relheight=1)

        content = tk.Frame(self.splash, bg=self.colors['bg_dark'])
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Animated logo
        logo = tk.Label(
            content,
            text="🎧",
            font=("Segoe UI Emoji", 100),
            bg=self.colors['bg_dark'],
            fg=self.colors['primary_red']
        )
        logo.pack(pady=20)

        # Title
        title = tk.Label(
            content,
            text="Music Match AI",
            font=("Segoe UI", 36, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_primary']
        )
        title.pack(pady=10)

        # Loading text
        self.loading_label = tk.Label(
            content,
            text="Loading...",
            font=("Segoe UI", 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_secondary']
        )
        self.loading_label.pack(pady=20)

        self.animate_loading()

    def animate_loading(self, dots=0):
        """Animate loading dots"""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.config(text="Loading" + "." * (dots % 4))
            self.root.after(300, lambda: self.animate_loading(dots + 1))

    def load_data(self):
        """Load all data"""
        try:
            # Load songs
            self.songs_df = pd.read_csv('data/spotify_songs.csv')
            self.songs_df.columns = self.songs_df.columns.str.strip()

            # Get genres
            self.unique_genres = self.songs_df['playlist_genre'].unique()
            for genre in self.unique_genres:
                self.genre_counts[genre] = len(self.songs_df[self.songs_df['playlist_genre'] == genre])

            # Load headphones
            headphones_df = pd.read_csv('data/headphones.csv')
            headphones_df.columns = headphones_df.columns.str.strip()

            for _, row in headphones_df.iterrows():
                hp = Headphone(
                    row['headphone_id'], row['brand'], row['model'],
                    row['price'], row['type'], row['use_case'],
                    row['bass_level'], row['sound_profile'],
                    row['noise_cancellation'], row['user_rating'],
                    row['user_reviews']
                )
                self.headphones.append(hp)

            # Initialize recommendation engine
            self.recommendation_engine = RecommendationEngine(self.headphones)

            self.root.after(0, self.create_main_ui)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load data: {e}"))

    def create_main_ui(self):
        """Create the main one-page UI"""
        # Destroy splash
        if hasattr(self, 'splash'):
            self.splash.destroy()

        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill="both", expand=True)

        # Header with gradient effect
        self.create_header(main_container)

        # Create main vertical PanedWindow for dynamic resizing
        self.main_paned = tk.PanedWindow(
            main_container,
            orient=tk.VERTICAL,
            bg=self.colors['bg_dark'],
            sashwidth=8,
            sashrelief=tk.RAISED,
            sashpad=2,
            relief=tk.FLAT,
            bd=0
        )
        self.main_paned.pack(fill="both", expand=True, padx=20, pady=20)

        # Top section - Three columns (Steps 1, 2, 3)
        top_section = tk.Frame(self.main_paned, bg=self.colors['bg_dark'])
        self.main_paned.add(top_section, minsize=300)

        # Create three-column layout in top section
        self.create_three_column_layout(top_section)

        # Bottom section - Recommendations (resizable)
        self.create_recommendations_section_dynamic(self.main_paned)

    def create_header(self, parent):
        """Create animated header that scales with window"""
        header = tk.Frame(parent, bg=self.colors['primary_red'], height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Create gradient effect with canvas that expands
        self.header_canvas = tk.Canvas(
            header,
            height=80,
            highlightthickness=0,
            bg=self.colors['primary_red']
        )
        self.header_canvas.pack(fill="both", expand=True)

        # Bind to canvas resize instead of window resize
        self.header_canvas.bind('<Configure>', self.on_header_resize)

        # Store text ID for updates
        self.header_text_id = None

    def on_header_resize(self, event):
        """Handle header canvas resize"""
        width = event.width
        height = 80

        # Clear canvas
        self.header_canvas.delete("all")

        # Redraw gradient
        for i in range(height):
            ratio = i / height
            r1 = int(255 * (1 - ratio) + 139 * ratio)
            g1 = int(0 * (1 - ratio) + 0 * ratio)
            b1 = int(110 * (1 - ratio) + 0 * ratio)
            color = f'#{r1:02x}{g1:02x}{b1:02x}'
            self.header_canvas.create_line(0, i, width, i, fill=color)

        # Redraw text centered
        self.header_text_id = self.header_canvas.create_text(
            width // 2,
            height // 2,
            text="🎧 Music Match AI",
            font=("Segoe UI", 28, "bold"),
            fill="white",
            anchor="center"
        )

    def create_three_column_layout(self, parent):
        """Create three columns for steps"""
        # Step 1: Genre Selection
        step1_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief="flat")
        step1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.create_genre_section(step1_frame)

        # Step 2: Song Selection
        step2_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief="flat")
        step2_frame.pack(side="left", fill="both", expand=True, padx=10)
        self.create_song_section(step2_frame)

        # Step 3: Use Case Selection
        step3_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief="flat")
        step3_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.create_use_case_section(step3_frame)

    def create_genre_section(self, parent):
        """Create genre selection section"""
        # Header
        header = tk.Frame(parent, bg=self.colors['bg_lighter'], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg=self.colors['bg_lighter'])
        header_content.pack(expand=True)

        tk.Label(
            header_content,
            text="Step 1.Select Genre",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary']
        ).pack()

        # Genre listbox with styling
        list_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, bg=self.colors['bg_lighter'])
        scrollbar.pack(side="right", fill="y")

        # Listbox
        self.genre_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary_red'],
            selectforeground="white",
            activestyle="none",
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
            yscrollcommand=scrollbar.set
        )
        self.genre_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.genre_listbox.yview)

        # Populate genres
        for genre in sorted(self.unique_genres):
            count = self.genre_counts.get(genre, 0)
            self.genre_listbox.insert(tk.END, f"{genre.upper()} ({count:,})")

        # Bind selection
        self.genre_listbox.bind('<<ListboxSelect>>', self.on_genre_select)

    def create_song_section(self, parent):
        """Create song selection section"""
        # Header with counter
        header = tk.Frame(parent, bg=self.colors['bg_lighter'], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_left = tk.Frame(header, bg=self.colors['bg_lighter'])
        header_left.pack(side="left", padx=15, expand=True, anchor="w")

        tk.Label(
            header_left,
            text="Step 2.Select 5 Songs",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary']
        ).pack(anchor="w")

        # Counter badge
        self.counter_frame = tk.Frame(
            header,
            bg=self.colors['primary_red'],
            width=60,
            height=40
        )
        self.counter_frame.pack(side="right", padx=15)
        self.counter_frame.pack_propagate(False)

        self.song_counter = tk.Label(
            self.counter_frame,
            text="0/5",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['primary_red'],
            fg="white"
        )
        self.song_counter.pack(expand=True)

        # Search bar
        search_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        search_frame.pack(fill="x", padx=10, pady=10)

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief="flat",
            bd=0
        )
        search_entry.pack(fill="x", ipady=8, padx=2, pady=2)

        # Placeholder
        search_entry.insert(0, "🔍 Search songs...")
        search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in(search_entry))
        search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out(search_entry))

        # Song listbox
        list_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame, bg=self.colors['bg_lighter'])
        scrollbar.pack(side="right", fill="y")

        self.song_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 10),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary_red'],
            selectforeground="white",
            selectmode="multiple",
            activestyle="none",
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
            yscrollcommand=scrollbar.set
        )
        self.song_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.song_listbox.yview)

        # Bind selection
        self.song_listbox.bind('<<ListboxSelect>>', self.on_song_select)

        # ADD TRACE AFTER LISTBOX IS CREATED
        self.search_var.trace('w', self.on_search)

    def create_use_case_section(self, parent):
        """Create use case selection section"""
        # Header
        header = tk.Frame(parent, bg=self.colors['bg_lighter'], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg=self.colors['bg_lighter'])
        header_content.pack(expand=True)

        tk.Label(
            header_content,
            text="Step 3.Select Use Case",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary']
        ).pack()

        # Use cases with modern cards
        cards_container = tk.Frame(parent, bg=self.colors['bg_card'])
        cards_container.pack(fill="both", expand=True, padx=10, pady=20)

        use_cases = [
            ("Workout", "🏋️"),
            ("Casual", "☕"),
            ("Studio", "🎙️"),
            ("Gaming", "🎮")
        ]

        self.use_case_var = tk.StringVar()

        for i, (name, emoji) in enumerate(use_cases):
            card = self.create_use_case_card(cards_container, name, emoji)
            card.pack(fill="x", pady=8, padx=5)

        # Buttons frame
        button_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        button_frame.pack(fill="x", padx=10, pady=20)

        # Analyze button (main button)
        self.analyze_btn_frame = tk.Frame(
            button_frame,
            bg=self.colors['primary_red'],
            cursor="hand2",
            relief="flat",
            bd=0
        )
        self.analyze_btn_frame.pack(fill="x", pady=(0, 8))

        self.analyze_btn_label = tk.Label(
            self.analyze_btn_frame,
            text="🤖 Start Analysis",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['primary_red'],
            fg="white",
            cursor="hand2",
            pady=15
        )
        self.analyze_btn_label.pack(fill="both", expand=True)

        # Bind click events
        self.analyze_btn_frame.bind('<Button-1>', lambda e: self.start_analysis())
        self.analyze_btn_label.bind('<Button-1>', lambda e: self.start_analysis())

        # Hover effects
        def analyze_on_enter(e):
            self.analyze_btn_frame.config(bg=self.colors['accent_red'])
            self.analyze_btn_label.config(bg=self.colors['accent_red'])

        def analyze_on_leave(e):
            self.analyze_btn_frame.config(bg=self.colors['primary_red'])
            self.analyze_btn_label.config(bg=self.colors['primary_red'])

        self.analyze_btn_frame.bind('<Enter>', analyze_on_enter)
        self.analyze_btn_frame.bind('<Leave>', analyze_on_leave)
        self.analyze_btn_label.bind('<Enter>', analyze_on_enter)
        self.analyze_btn_label.bind('<Leave>', analyze_on_leave)

        # Secondary buttons frame (Clear and Reset)
        secondary_buttons = tk.Frame(button_frame, bg=self.colors['bg_card'])
        secondary_buttons.pack(fill="x")

        # Clear Selections button
        self.clear_btn_frame = tk.Frame(
            secondary_buttons,
            bg=self.colors['bg_lighter'],
            cursor="hand2",
            relief="flat",
            bd=0
        )
        self.clear_btn_frame.pack(side="left", fill="both", expand=True, padx=(0, 4))

        self.clear_btn_label = tk.Label(
            self.clear_btn_frame,
            text="🔄 Clear Songs",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            cursor="hand2",
            pady=10
        )
        self.clear_btn_label.pack(fill="both", expand=True)

        # Bind clear button
        self.clear_btn_frame.bind('<Button-1>', lambda e: self.clear_selections())
        self.clear_btn_label.bind('<Button-1>', lambda e: self.clear_selections())

        # Hover for clear
        def clear_on_enter(e):
            self.clear_btn_frame.config(bg=self.colors['bg_hover'])
            self.clear_btn_label.config(bg=self.colors['bg_hover'])

        def clear_on_leave(e):
            self.clear_btn_frame.config(bg=self.colors['bg_lighter'])
            self.clear_btn_label.config(bg=self.colors['bg_lighter'])

        self.clear_btn_frame.bind('<Enter>', clear_on_enter)
        self.clear_btn_frame.bind('<Leave>', clear_on_leave)
        self.clear_btn_label.bind('<Enter>', clear_on_enter)
        self.clear_btn_label.bind('<Leave>', clear_on_leave)

        # Reset button
        self.reset_btn_frame = tk.Frame(
            secondary_buttons,
            bg=self.colors['bg_lighter'],
            cursor="hand2",
            relief="flat",
            bd=0
        )
        self.reset_btn_frame.pack(side="left", fill="both", expand=True, padx=(4, 0))

        self.reset_btn_label = tk.Label(
            self.reset_btn_frame,
            text="♻️ Reset All",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            cursor="hand2",
            pady=10
        )
        self.reset_btn_label.pack(fill="both", expand=True)

        # Bind reset button
        self.reset_btn_frame.bind('<Button-1>', lambda e: self.reset())
        self.reset_btn_label.bind('<Button-1>', lambda e: self.reset())

        # Hover for reset
        def reset_on_enter(e):
            self.reset_btn_frame.config(bg=self.colors['bg_hover'])
            self.reset_btn_label.config(bg=self.colors['bg_hover'])

        def reset_on_leave(e):
            self.reset_btn_frame.config(bg=self.colors['bg_lighter'])
            self.reset_btn_label.config(bg=self.colors['bg_lighter'])

        self.reset_btn_frame.bind('<Enter>', reset_on_enter)
        self.reset_btn_frame.bind('<Leave>', reset_on_leave)
        self.reset_btn_label.bind('<Enter>', reset_on_enter)
        self.reset_btn_label.bind('<Leave>', reset_on_leave)

    def create_use_case_card(self, parent, name, emoji):
        """Create individual use case card with full clickable area"""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['bg_lighter'],
            relief="flat",
            cursor="hand2"
        )

        # Content
        content = tk.Frame(card_frame, bg=self.colors['bg_lighter'], cursor="hand2")
        content.pack(fill="both", expand=True, padx=15, pady=12)

        # Emoji and name
        left_frame = tk.Frame(content, bg=self.colors['bg_lighter'], cursor="hand2")
        left_frame.pack(side="left", fill="both", expand=True)

        emoji_label = tk.Label(
            left_frame,
            text=emoji,
            font=("Segoe UI Emoji", 24),
            bg=self.colors['bg_lighter'],
            cursor="hand2"
        )
        emoji_label.pack(side="left", padx=(0, 10))

        name_label = tk.Label(
            left_frame,
            text=name,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            cursor="hand2"
        )
        name_label.pack(side="left")

        # Radio button indicator
        radio = tk.Radiobutton(
            content,
            variable=self.use_case_var,
            value=name,
            bg=self.colors['bg_lighter'],
            activebackground=self.colors['bg_lighter'],
            selectcolor=self.colors['primary_red'],
            fg=self.colors['text_primary'],
            cursor="hand2"
        )
        radio.pack(side="right")

        # Bind click to ALL elements
        def select_use_case(e=None):
            self.use_case_var.set(name)
            self.selected_use_case = name

        for widget in [card_frame, content, left_frame, emoji_label, name_label, radio]:
            widget.bind('<Button-1>', select_use_case)

            # Hover effects on all elements
            def on_enter(e):
                for widget in [card_frame, content, left_frame, emoji_label, name_label]:
                    widget.config(bg=self.colors['bg_hover'])
                radio.config(bg=self.colors['bg_hover'], activebackground=self.colors['bg_hover'])

            def on_leave(e):
                for widget in [card_frame, content, left_frame, emoji_label, name_label]:
                    widget.config(bg=self.colors['bg_lighter'])
                radio.config(bg=self.colors['bg_lighter'], activebackground=self.colors['bg_lighter'])

            for widget in [card_frame, content, left_frame, emoji_label, name_label]:
                widget.bind('<Enter>', on_enter)
                widget.bind('<Leave>', on_leave)

            return card_frame

    def create_recommendations_section_dynamic(self, paned_window):
        """Create resizable recommendations section"""
        # Recommendations frame
        rec_container = tk.Frame(paned_window, bg=self.colors['bg_dark'])
        paned_window.add(rec_container, minsize=150)

        # Separator
        separator = tk.Frame(rec_container, bg=self.colors['success'], height=3)
        separator.pack(fill="x", pady=(0, 10))

        # Recommendations header
        rec_header = tk.Frame(rec_container, bg=self.colors['bg_card'], height=50)
        rec_header.pack(fill="x")
        rec_header.pack_propagate(False)

        header_content = tk.Frame(rec_header, bg=self.colors['bg_card'])
        header_content.pack(side="left", padx=15, expand=True, anchor="w")

        # Header icon and text
        tk.Label(
            header_content,
            text="✨ Recommendations",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side="left")

        # Add resize indicator
        tk.Label(
            header_content,
            text="⇕ Drag to resize",
            font=("Segoe UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        ).pack(side="left", padx=15)

        # Recommendations content
        rec_frame = tk.Frame(rec_container, bg=self.colors['bg_card'])
        rec_frame.pack(fill="both", expand=True)

        # Scrolled text for recommendations
        self.recommendations_text = scrolledtext.ScrolledText(
            rec_frame,
            font=("Consolas", 10),
            bg=self.colors['bg_lighter'],
            fg=self.colors['text_primary'],
            relief="flat",
            wrap="word",
            insertbackground=self.colors['text_primary']
        )
        self.recommendations_text.pack(fill="both", expand=True, padx=10, pady=10)

        welcome_text = """Welcome! Complete the 3 steps above to get recommendations.
        Instructions:
        Select a genre from the left
        Select 5 songs (Click on songs)
        Choose use case and click Analyze
        Your personalized headphone recommendations will appear here!
💡      TIP: Drag the green separator above to resize this area!
        The sections above will adjust automatically.
        """
        self.recommendations_text.insert("1.0",welcome_text)
        self.recommendations_text.config(state="disabled")

    def on_genre_select(self, event):
        """Handle genre selection"""
        selection = self.genre_listbox.curselection()
        if selection:
            genre_text = self.genre_listbox.get(selection[0])
            genre = genre_text.split('(')[0].strip()

            # Find matching genre
            for g in self.unique_genres:
                if g.upper() == genre:
                    # Only clear selections if changing to a different genre
                    if self.selected_genre != g:
                        self.selected_genre = g
                        self.selected_songs = []
                        self.selected_song_ids = set()
                        self.update_counter(0)
                    break

            self.load_songs_for_genre(self.selected_genre)

    def load_songs_for_genre(self, genre):
        """Load songs for selected genre"""
        if not hasattr(self, 'song_listbox'):
            return

        self.song_listbox.delete(0, tk.END)
        self.song_listbox.insert(0, "Loading songs...")

        def load():
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

            self.root.after(0, self.display_songs)

        threading.Thread(target=load, daemon=True).start()

    def display_songs(self):
        """Display songs in listbox and restore selections"""
        if not hasattr(self, 'song_listbox') or not self.song_listbox.winfo_exists():
            return

        self.song_listbox.delete(0, tk.END)
        self.current_display_songs = self.filtered_songs[:500]

        for song in self.current_display_songs:
            display_text = f"♪ {song.track_name[:45]} - {song.track_artist[:30]}"
            self.song_listbox.insert(tk.END, display_text)

        # Restore selections based on song IDs
        for idx, song in enumerate(self.current_display_songs):
            if song.track_id in self.selected_song_ids:
                self.song_listbox.selection_set(idx)

    def on_song_select(self, event):
        """Handle song selection - persist across searches"""
        if not hasattr(self, 'current_display_songs'):
            return

        selections = self.song_listbox.curselection()

        # Get newly selected songs
        new_selected_ids = set()
        new_selected_songs = []

        for idx in selections:
            if idx < len(self.current_display_songs):
                song = self.current_display_songs[idx]
                new_selected_ids.add(song.track_id)
                new_selected_songs.append(song)

        # Check limit
        if len(new_selected_ids) > 5:
            messagebox.showwarning("Selection Limit", "You can only select up to 5 songs.")
            # Restore previous selection
            self.display_songs()
            return

        # Update selections
        self.selected_song_ids = new_selected_ids
        self.selected_songs = new_selected_songs
        self.update_counter(len(self.selected_songs))

    def update_counter(self, count):
        """Update song counter"""
        self.song_counter.config(text=f"{count}/5")

        if count == 5:
            self.counter_frame.config(bg=self.colors['success'])
            self.song_counter.config(bg=self.colors['success'])
        else:
            self.counter_frame.config(bg=self.colors['primary_red'])
            self.song_counter.config(bg=self.colors['primary_red'])

    def on_search(self, *args):
        """Handle search while maintaining selections"""
        if not hasattr(self, 'song_listbox') or not self.song_listbox.winfo_exists():
            return

        search_term = self.search_var.get()

        if search_term and search_term != "🔍 Search songs..." and self.filtered_songs:
            # Filter songs
            filtered = [
                song for song in self.filtered_songs
                if (search_term.lower() in song.track_name.lower() or
                    search_term.lower() in song.track_artist.lower())
            ]

            self.current_display_songs = filtered[:500]

            # Display filtered songs
            self.song_listbox.delete(0, tk.END)
            for song in self.current_display_songs:
                display_text = f"♪ {song.track_name[:45]} - {song.track_artist[:30]}"
                self.song_listbox.insert(tk.END, display_text)

            # Restore selections
            for idx, song in enumerate(self.current_display_songs):
                if song.track_id in self.selected_song_ids:
                    self.song_listbox.selection_set(idx)

        elif not search_term or search_term == "🔍 Search songs...":
            if self.filtered_songs:
                self.display_songs()

    def on_search_focus_in(self, entry):
        """Clear placeholder"""
        if entry.get() == "🔍 Search songs...":
            entry.delete(0, tk.END)

    def on_search_focus_out(self, entry):
        """Restore placeholder"""
        if not entry.get():
            entry.insert(0, "🔍 Search songs...")

    def start_analysis(self):
        """Start recommendation analysis"""
        # Check if button is disabled
        if hasattr(self, 'button_disabled') and self.button_disabled:
            return

        if not self.selected_genre:
            messagebox.showwarning("Missing Selection", "Please select a genre first!")
            return

        if len(self.selected_songs) < 5:
            messagebox.showwarning("Missing Selection",
                                   f"Please select 5 songs. You have {len(self.selected_songs)}.")
            return

        if not self.use_case_var.get():
            messagebox.showwarning("Missing Selection", "Please select a use case!")
            return

        # Disable button
        self.button_disabled = True
        self.analyze_btn_label.config(text="🤖 Analyzing...")
        self.analyze_btn_frame.config(cursor="wait")
        self.analyze_btn_label.config(cursor="wait")

        self.recommendations_text.config(state="normal")
        self.recommendations_text.delete("1.0", tk.END)
        self.recommendations_text.insert("1.0", "AI is analyzing your music preferences...\n\n")
        self.recommendations_text.config(state="disabled")

        threading.Thread(target=self.generate_recommendations, daemon=True).start()

    def generate_recommendations(self):
        """Generate recommendations"""
        import time
        time.sleep(1)

        self.selected_use_case = self.use_case_var.get()

        recommendations, most_reviewed = self.recommendation_engine.generate_recommendations(
            self.selected_songs,
            self.selected_use_case
        )

        self.root.after(0, lambda: self.display_recommendations(recommendations, most_reviewed))

    def display_recommendations(self, recommendations, most_reviewed):
        """Display recommendations in the same window"""
        # Re-enable button
        self.button_disabled = False
        self.analyze_btn_label.config(text="🤖 Start Analysis")
        self.analyze_btn_frame.config(cursor="hand2")
        self.analyze_btn_label.config(cursor="hand2")

        # Update recommendations text
        self.recommendations_text.config(state="normal")
        self.recommendations_text.delete("1.0", tk.END)

        # Build results text
        self.recommendations_text.insert("end", "=" * 80 + "\n")
        self.recommendations_text.insert("end", "✨ YOUR PERFECT HEADPHONES - AI POWERED RECOMMENDATIONS ✨\n")
        self.recommendations_text.insert("end", "=" * 80 + "\n\n")

        self.recommendations_text.insert("end",
                                         f"Based on: {self.selected_genre} music • {self.selected_use_case} use case\n")
        self.recommendations_text.insert("end", f"Songs analyzed: {len(self.selected_songs)}\n\n")

        # Most reviewed
        if most_reviewed:
            self.recommendations_text.insert("end", "⭐ " + "=" * 76 + " ⭐\n")
            self.recommendations_text.insert("end", "  MOST POSITIVELY REVIEWED\n")
            self.recommendations_text.insert("end", "⭐ " + "=" * 76 + " ⭐\n\n")
            self.format_headphone(self.recommendations_text, most_reviewed)
            self.recommendations_text.insert("end", "\n")

        # Categories
        category_icons = {
            "Budget-Friendly": "💚",
            "Best of Both": "💙",
            "Best of the Line": "❤️"
        }

        for category, headphones in recommendations.items():
            if not headphones:
                continue

            icon = category_icons.get(category, "🎧")
            self.recommendations_text.insert("end", f"\n{icon} {category.upper()} {icon}\n")
            self.recommendations_text.insert("end", "-" * 80 + "\n\n")

            for i, hp in enumerate(headphones, 1):
                self.recommendations_text.insert("end", f"{i}. ")
                self.format_headphone(self.recommendations_text, hp)
                if i < len(headphones):
                    self.recommendations_text.insert("end", "\n")

        self.recommendations_text.insert("end", "\n" + "=" * 80 + "\n")
        self.recommendations_text.insert("end", "Thank you for using Music Match AI! 🎧\n")
        self.recommendations_text.insert("end", "\n💡 TIP: Drag the separator to resize!\n")

        self.recommendations_text.config(state="disabled")
        self.recommendations_text.see("1.0")

    def format_headphone(self, text_widget, hp):
        """Format single headphone for display"""
        stars = "⭐" * int(hp.user_rating)

        text_widget.insert("end", f"{hp.brand} {hp.model}\n")
        text_widget.insert("end", f"  💰 Price: ${hp.price:.0f}\n")
        text_widget.insert("end", f"  {stars} {hp.user_rating}/5.0 ({hp.user_reviews:,} reviews)\n")
        text_widget.insert("end", f"  🎧 Type: {hp.hp_type} | Bass: {hp.bass_level} | Profile: {hp.sound_profile}\n")
        text_widget.insert("end", f"  🔇 Noise Cancellation: {'Yes' if hp.noise_cancellation else 'No'}\n")
        text_widget.insert("end", "\n")

    def clear_selections(self):
        """Clear song selections and use case, keep genre"""
        # Clear song selections
        if hasattr(self, 'song_listbox'):
            self.song_listbox.selection_clear(0, tk.END)

        self.selected_songs = []
        self.selected_song_ids = set()

        # Clear use case
        self.use_case_var.set("")
        self.selected_use_case = None

        # Reset counter
        self.update_counter(0)

        # Clear recommendations
        self.recommendations_text.config(state='normal')
        self.recommendations_text.delete('1.0', tk.END)
        self.recommendations_text.insert('1.0',
                                         "Selections cleared! Genre preserved.\n\n"
                                         "Select 5 songs and choose a use case to continue.\n\n"
                                         "💡 TIP: Drag the separator to resize this area!")
        self.recommendations_text.config(state='disabled')

        messagebox.showinfo("Cleared", "Song selections and use case cleared. Genre preserved.", parent=self.root)

    def reset(self):
        """Reset entire application"""
        # Clear all selections
        self.selected_genre = None
        self.selected_songs = []
        self.selected_song_ids = set()
        self.selected_use_case = None
        self.filtered_songs = []
        self.current_display_songs = []

        # Clear genre selection
        if hasattr(self, 'genre_listbox'):
            self.genre_listbox.selection_clear(0, tk.END)

        # Clear song listbox
        if hasattr(self, 'song_listbox'):
            self.song_listbox.delete(0, tk.END)

        # Clear use case
        self.use_case_var.set("")

        # Clear search
        if hasattr(self, 'search_var'):
            self.search_var.set("")

        # Reset counter
        self.update_counter(0)

        # Reset recommendations
        self.recommendations_text.config(state='normal')
        self.recommendations_text.delete('1.0', tk.END)
        self.recommendations_text.insert('1.0',
                                         """Welcome! Complete the 3 steps above to get recommendations.
                                         Instructions:

Select a genre from the left
Select 5 songs (Click on songs)
Choose use case and click Analyze

Your personalized headphone recommendations will appear here!
💡 TIP: Drag the green separator above to resize this area!
The sections above will adjust automatically.
""")
        self.recommendations_text.config(state='disabled')
        messagebox.showinfo("Reset Complete", "Application has been reset to initial state.", parent=self.root)

def main():
    root = tk.Tk()
    app = MusicMatchOnePageApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
