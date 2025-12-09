"""
Music Match Headphones - Advanced AI-Powered Version
Using Machine Learning and Modern UI
Date: December 2024
Authors: Haihan Zhang, Anish Suresh Saini
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import numpy as np
from song import Song
from headphone import Headphone
import threading
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import time

class MusicMatchModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Match Headphones - Recommendation System")
        self.root.geometry("1100x700")

        # Modern color scheme
        self.colors = {
            'primary': '#6366f1',        # Indigo
            'primary_dark': '#4f46e5',
            'secondary': '#8b5cf6',      # Purple
            'accent': '#ec4899',         # Pink
            'success': '#10b981',        # Green
            'warning': '#f59e0b',        # Amber
            'bg_main': '#f8fafc',        # Light gray
            'bg_card': '#ffffff',
            'bg_dark': '#1e293b',
            'text_dark': '#0f172a',
            'text_light': '#64748b',
            'border': '#e2e8f0'
        }

        self.root.configure(bg=self.colors['bg_main'])

        # Application state
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.filtered_songs = []

        # ML components
        self.song_features_scaler = StandardScaler()
        self.recommendation_model = None
        self.songs_df = None
        self.headphones = []
        self.unique_genres = []
        self.genre_counts = {}

        # Load data
        self.load_data()
        self.setup_styles()
        self.build_interface()

    def load_data(self):
        """Load songs and headphones data"""
        try:
            songs_df = pd.read_csv('data/spotify_songs.csv')
            songs_df.columns = songs_df.columns.str.strip()
            self.songs_df = songs_df

            feature_columns = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness']
            self.song_features = songs_df[feature_columns].values
            self.song_features_scaled = self.song_features_scaler.fit_transform(self.song_features)

            self.recommendation_model = NearestNeighbors(n_neighbors=10, algorithm='ball_tree', metric='euclidean')
            self.recommendation_model.fit(self.song_features_scaled)

            self.unique_genres = sorted(songs_df['playlist_genre'].unique())
            for genre in self.unique_genres:
                self.genre_counts[genre] = len(songs_df[songs_df['playlist_genre'] == genre])

            headphones_df = pd.read_csv('data/headphones.csv')
            headphones_df.columns = headphones_df.columns.str.strip()

            for _, row in headphones_df.iterrows():
                self.headphones.append(Headphone(
                    row['headphone_id'], row['brand'], row['model'], row['price'],
                    row['type'], row['use_case'], row['bass_level'], row['sound_profile'],
                    row['noise_cancellation'], row['user_rating'], row['user_reviews']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def setup_styles(self):
        """Setup ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Treeview style
        style.configure("Modern.Treeview",
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['bg_card'],
                       borderwidth=0,
                       font=('Segoe UI', 9))
        style.map("Modern.Treeview",
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])

        # Configure Radiobutton style
        style.configure("Modern.TRadiobutton",
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_dark'],
                       font=('Segoe UI', 9))

    def build_interface(self):
        # Header with gradient effect
        header_frame = tk.Canvas(self.root, height=50, bg=self.colors['primary'], highlightthickness=0)
        header_frame.pack(fill='x')

        # Gradient effect simulation
        header_frame.create_rectangle(0, 0, 1100, 50, fill=self.colors['primary'], outline='')
        header_frame.create_text(550, 25, text="🎧 Music Match AI",
                                font=('Segoe UI', 16, 'bold'), fill='white')

        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True, padx=12, pady=12)

        # Top section (Genre and Songs) - Card style
        top_frame = tk.Frame(main_container, bg=self.colors['bg_main'])
        top_frame.pack(fill='both', expand=True)

        # Left card: Genre Selection
        self.build_genre_card(top_frame)

        # Right card: Song Selection
        self.build_song_card(top_frame)

        # Middle card: Use Case
        self.build_usecase_card(main_container)

        # Bottom card: Results
        self.build_results_card(main_container)

    def create_card(self, parent, **kwargs):
        card = tk.Frame(parent, bg=self.colors['bg_card'],
                       relief='flat', bd=0, **kwargs)
        # Add shadow effect with border
        card.configure(highlightbackground=self.colors['border'],
                      highlightthickness=1)
        return card

    def build_genre_card(self, parent):
        """Build genre selection card"""
        card = self.create_card(parent)
        card.pack(side='left', fill='both', padx=(0, 6), ipadx=8, ipady=8)

        # Header
        header = tk.Frame(card, bg=self.colors['bg_card'])
        header.pack(fill='x', padx=12, pady=(12, 8))

        tk.Label(header, text="Step 1.Select Genre",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_dark']).pack(anchor='w')

        # Separator
        sep = tk.Frame(card, height=2, bg=self.colors['primary'])
        sep.pack(fill='x', padx=12, pady=(0, 8))

        # Genre list with custom styling
        list_frame = tk.Frame(card, bg=self.colors['bg_card'])
        list_frame.pack(fill='both', expand=True, padx=12, pady=(0, 12))

        # Custom listbox with modern colors
        self.genre_listbox = tk.Listbox(list_frame,
                                       width=22, height=10,
                                       font=('Segoe UI', 9),
                                       bg=self.colors['bg_main'],
                                       fg=self.colors['text_dark'],
                                       selectbackground=self.colors['primary'],
                                       selectforeground='white',
                                       relief='flat',
                                       borderwidth=0,
                                       highlightthickness=1,
                                       highlightbackground=self.colors['border'],
                                       highlightcolor=self.colors['primary'])
        self.genre_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.genre_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.genre_listbox.config(yscrollcommand=scrollbar.set)

        for genre in self.unique_genres:
            self.genre_listbox.insert(tk.END, f"  {genre.upper()} ({self.genre_counts[genre]:,})")

        self.genre_listbox.bind('<<ListboxSelect>>', self.on_genre_select)

    def build_song_card(self, parent):
        """Build song selection card"""
        card = self.create_card(parent)
        card.pack(side='left', fill='both', expand=True, padx=(6, 0), ipadx=8, ipady=8)

        # Header
        header = tk.Frame(card, bg=self.colors['bg_card'])
        header.pack(fill='x', padx=12, pady=(12, 8))

        tk.Label(header, text="Step 2.Select 5 Songs",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_dark']).pack(side='left', anchor='w')

        # Counter badge
        self.counter_label = tk.Label(header, text="0/5",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg=self.colors['primary'],
                                     fg='white',
                                     padx=12, pady=4)
        self.counter_label.pack(side='right')

        # Separator
        sep = tk.Frame(card, height=2, bg=self.colors['secondary'])
        sep.pack(fill='x', padx=12, pady=(0, 8))

        # Search bar with modern styling
        search_frame = tk.Frame(card, bg=self.colors['bg_card'])
        search_frame.pack(fill='x', padx=12, pady=(0, 8))

        tk.Label(search_frame, text="🔍",
                font=('Segoe UI', 10),
                bg=self.colors['bg_card']).pack(side='left', padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)

        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=('Segoe UI', 9),
                               bg=self.colors['bg_main'],
                               fg=self.colors['text_dark'],
                               relief='flat',
                               borderwidth=0,
                               highlightthickness=1,
                               highlightbackground=self.colors['border'],
                               highlightcolor=self.colors['primary'])
        search_entry.pack(side='left', fill='x', expand=True, ipady=4)

        # Song list
        list_frame = tk.Frame(card, bg=self.colors['bg_card'])
        list_frame.pack(fill='both', expand=True, padx=12, pady=(0, 12))

        self.songs_listbox = tk.Listbox(list_frame,
                                       height=10,
                                       font=('Segoe UI', 8),
                                       bg=self.colors['bg_main'],
                                       fg=self.colors['text_dark'],
                                       selectbackground=self.colors['secondary'],
                                       selectforeground='white',
                                       selectmode=tk.MULTIPLE,
                                       relief='flat',
                                       borderwidth=0,
                                       highlightthickness=1,
                                       highlightbackground=self.colors['border'],
                                       highlightcolor=self.colors['secondary'])
        self.songs_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.songs_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.songs_listbox.config(yscrollcommand=scrollbar.set)

        self.songs_listbox.bind('<<ListboxSelect>>', self.on_song_select)

    def build_usecase_card(self, parent):
        """Build use case selection card"""
        card = self.create_card(parent)
        card.pack(fill='x', pady=(12, 0), ipadx=12, ipady=12)

        # Header
        header = tk.Frame(card, bg=self.colors['bg_card'])
        header.pack(fill='x', padx=12, pady=(8, 8))

        tk.Label(header, text="Step 3.Select Use Case",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_dark']).pack(side='left')

        # Separator
        sep = tk.Frame(card, height=2, bg=self.colors['accent'])
        sep.pack(fill='x', padx=12, pady=(0, 12))

        # Use case options
        options_frame = tk.Frame(card, bg=self.colors['bg_card'])
        options_frame.pack(fill='x', padx=12, pady=(0, 12))

        self.use_case_var = tk.StringVar()
        use_cases = [
            ("🏋️ Workout", "Workout"),
            ("☕ Casual", "Casual"),
            ("🎙️ Studio", "Studio"),
            ("🎮 Gaming", "Gaming")
        ]

        for i, (text, value) in enumerate(use_cases):
            rb = tk.Radiobutton(options_frame,
                               text=text,
                               variable=self.use_case_var,
                               value=value,
                               font=('Segoe UI', 9),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_dark'],
                               selectcolor=self.colors['bg_main'],
                               activebackground=self.colors['bg_card'],
                               activeforeground=self.colors['primary'],
                               command=self.on_use_case_select)
            rb.pack(side='left', padx=15, pady=5)

        # Modern analyze button
        self.analyze_btn = tk.Button(card,
                                     text="🤖 Start Analysis",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg=self.colors['primary'],
                                     fg='white',
                                     activebackground=self.colors['primary_dark'],
                                     activeforeground='white',
                                     relief='flat',
                                     borderwidth=0,
                                     cursor='hand2',
                                     command=self.analyze_and_recommend,
                                     state='disabled',
                                     padx=20,
                                     pady=10)
        self.analyze_btn.pack(padx=12, pady=(0, 12), fill='x')

        # Hover effect
        self.analyze_btn.bind('<Enter>', lambda e: self.on_button_hover(self.analyze_btn, True))
        self.analyze_btn.bind('<Leave>', lambda e: self.on_button_hover(self.analyze_btn, False))

    def build_results_card(self, parent):
        """Build results display card"""
        card = self.create_card(parent)
        card.pack(fill='both', expand=True, pady=(12, 0), ipadx=12, ipady=12)

        # Header
        header = tk.Frame(card, bg=self.colors['bg_card'])
        header.pack(fill='x', padx=12, pady=(8, 8))

        tk.Label(header, text="✨ Recommendations",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_dark']).pack(side='left')

        # Separator
        sep = tk.Frame(card, height=2, bg=self.colors['success'])
        sep.pack(fill='x', padx=12, pady=(0, 8))

        # Results text area with modern styling
        text_frame = tk.Frame(card, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, padx=12, pady=(0, 12))

        self.results_text = scrolledtext.ScrolledText(text_frame,
                                                      height=8,
                                                      font=('Consolas', 8),
                                                      bg=self.colors['bg_main'],
                                                      fg=self.colors['text_dark'],
                                                      relief='flat',
                                                      borderwidth=0,
                                                      highlightthickness=1,
                                                      highlightbackground=self.colors['border'],
                                                      wrap=tk.WORD,
                                                      padx=8,
                                                      pady=8)
        self.results_text.pack(fill='both', expand=True)

        # Action buttons
        btn_frame = tk.Frame(card, bg=self.colors['bg_card'])
        btn_frame.pack(padx=12, pady=(0, 12))

        # Clear button
        clear_btn = tk.Button(btn_frame,
                             text="🗑️ Clear Selections",
                             font=('Segoe UI', 9, 'bold'),
                             bg=self.colors['warning'],
                             fg='white',
                             activebackground='#d97706',
                             activeforeground='white',
                             relief='flat',
                             borderwidth=0,
                             cursor='hand2',
                             command=self.clear_selections,
                             padx=15,
                             pady=8)
        clear_btn.pack(side='left', padx=5)

        # Reset button
        reset_btn = tk.Button(btn_frame,
                             text="🔄 Reset All",
                             font=('Segoe UI', 9, 'bold'),
                             bg=self.colors['text_light'],
                             fg='white',
                             activebackground='#475569',
                             activeforeground='white',
                             relief='flat',
                             borderwidth=0,
                             cursor='hand2',
                             command=self.reset,
                             padx=15,
                             pady=8)
        reset_btn.pack(side='left', padx=5)

        # Add hover effects
        clear_btn.bind('<Enter>', lambda e: self.on_button_hover(clear_btn, True, '#d97706'))
        clear_btn.bind('<Leave>', lambda e: self.on_button_hover(clear_btn, False, self.colors['warning']))
        reset_btn.bind('<Enter>', lambda e: self.on_button_hover(reset_btn, True, '#475569'))
        reset_btn.bind('<Leave>', lambda e: self.on_button_hover(reset_btn, False, self.colors['text_light']))

        # Initial message
        self.results_text.insert('1.0', "Welcome! Complete the 3 steps above to get recommendations.\n\n"
                                       "Instructions:\n"
                                       "1. Select a genre from the left\n"
                                       "2. Select 5 songs (Click on songs)\n"
                                       "3. Choose use case and click Analyze")
        self.results_text.config(state='disabled')

    def on_button_hover(self, button, entering, hover_color=None):
        """Button hover effect"""
        if button['state'] == 'disabled':
            return

        if entering:
            if hover_color:
                button.config(bg=hover_color)
            elif button == self.analyze_btn:
                button.config(bg=self.colors['primary_dark'])
        else:
            if button == self.analyze_btn:
                button.config(bg=self.colors['primary'])

    def on_genre_select(self, event):
        """Handle genre selection"""
        selection = self.genre_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        genre = self.unique_genres[idx]
        self.selected_genre = genre

        self.load_genre_songs(genre)

    def load_genre_songs(self, genre):
        """Load songs for selected genre"""
        genre_df = self.songs_df[self.songs_df['playlist_genre'] == genre]

        self.filtered_songs = []
        for _, row in genre_df.iterrows():
            self.filtered_songs.append(Song(
                row['track_id'], row['track_name'], row['track_artist'],
                row['track_popularity'], row['playlist_genre'], row['playlist_subgenre'],
                row['danceability'], row['energy'], row['valence'], row['tempo'],
                row['acousticness'], row['loudness']
            ))

        self.display_songs()

    def display_songs(self):
        """Display songs in listbox"""
        self.songs_listbox.delete(0, tk.END)

        for song in self.filtered_songs:
            display_text = f"  {song.track_name} - {song.track_artist}"
            if len(display_text) > 70:
                display_text = display_text[:67] + "..."
            self.songs_listbox.insert(tk.END, display_text)

    def on_song_select(self, event):
        """Handle song selection"""
        selections = self.songs_listbox.curselection()

        if len(selections) > 5:
            messagebox.showwarning("Selection Limit", "You can only select up to 5 songs.")
            self.songs_listbox.selection_clear(selections[-1])
            return

        current_display = []
        search_term = self.search_var.get().strip().lower()

        if not search_term:
            current_display = self.filtered_songs
        else:
            current_display = [s for s in self.filtered_songs
                             if search_term in s.track_name.lower() or
                                search_term in s.track_artist.lower()]

        self.selected_songs = [current_display[i] for i in selections if i < len(current_display)]

        self.counter_label.config(text=f"{len(self.selected_songs)}/5")

        if len(self.selected_songs) == 5 and self.use_case_var.get():
            self.analyze_btn.config(state='normal')
        else:
            self.analyze_btn.config(state='disabled')

    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().strip().lower()

        if not self.filtered_songs:
            return

        self.songs_listbox.delete(0, tk.END)

        if not search_term:
            filtered = self.filtered_songs
        else:
            filtered = [s for s in self.filtered_songs
                       if search_term in s.track_name.lower() or
                          search_term in s.track_artist.lower()]

        for song in filtered:
            display_text = f"  {song.track_name} - {song.track_artist}"
            if len(display_text) > 70:
                display_text = display_text[:67] + "..."
            self.songs_listbox.insert(tk.END, display_text)

        if search_term:
            self.counter_label.config(text=f"{len(self.selected_songs)}/5")

    def on_use_case_select(self):
        """Handle use case selection"""
        self.selected_use_case = self.use_case_var.get()

        if len(self.selected_songs) == 5:
            self.analyze_btn.config(state='normal')

    def analyze_and_recommend(self):
        """Analyze and generate recommendations"""
        if not self.selected_genre or len(self.selected_songs) != 5 or not self.selected_use_case:
            messagebox.showwarning("Incomplete", "Please complete all 3 steps.")
            return

        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "🤖 AI is analyzing your music preferences...\n\n"
                                       "Please wait...")
        self.results_text.config(state='disabled')

        self.analyze_btn.config(state='disabled', text="Processing...")

        threading.Thread(target=self.generate_recommendations, daemon=True).start()

    def generate_recommendations(self):
        """Generate recommendations"""
        time.sleep(1.5)

        matching = [hp for hp in self.headphones
                   if hp.use_case.lower() == self.selected_use_case.lower()]

        scored = []
        for hp in matching:
            score = hp.user_rating * 2

            avg_loudness = np.mean([s.loudness for s in self.selected_songs])
            if avg_loudness > -4 and hp.bass_level == "High":
                score += 3
            elif avg_loudness < -7 and hp.bass_level == "Low":
                score += 3

            avg_energy = np.mean([s.energy for s in self.selected_songs])
            if avg_energy > 0.7 and hp.sound_profile == "Bass-heavy":
                score += 2
            elif avg_energy < 0.4 and hp.sound_profile == "Flat":
                score += 2

            scored.append((hp, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        budget = [hp for hp, s in scored if hp.price < 150][:3]
        premium = [hp for hp, s in scored if hp.price > 400][:3]
        balanced = [hp for hp, s in scored if 150 <= hp.price <= 400][:3]

        recommendations = {
            "Budget-Friendly (Under $150)": budget,
            "Best of Both ($150-$400)": balanced,
            "Best of the Line (Over $400)": premium
        }

        all_hp = budget + premium + balanced
        most_reviewed = max(all_hp, key=lambda hp: hp.user_rating * hp.user_reviews) if all_hp else None

        self.root.after(0, lambda: self.show_recommendations(recommendations, most_reviewed))

    def show_recommendations(self, recommendations, most_reviewed):
        """Display recommendations"""
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)

        self.results_text.insert(tk.END, "="*95 + "\n")
        self.results_text.insert(tk.END, "✨ RECOMMENDATION RESULTS\n")
        self.results_text.insert(tk.END, "="*95 + "\n\n")

        self.results_text.insert(tk.END, f"Genre: {self.selected_genre} | Use Case: {self.selected_use_case}\n\n")

        if most_reviewed:
            self.results_text.insert(tk.END, "⭐ MOST POSITIVELY REVIEWED\n")
            self.results_text.insert(tk.END, "-" * 95 + "\n")
            self.format_headphone(most_reviewed)
            self.results_text.insert(tk.END, "\n")

        for category, headphones in recommendations.items():
            if not headphones:
                continue

            self.results_text.insert(tk.END, f"\n{'='*95}\n")
            self.results_text.insert(tk.END, f"{category.upper()}\n")
            self.results_text.insert(tk.END, f"{'='*95}\n\n")

            for i, hp in enumerate(headphones, 1):
                self.results_text.insert(tk.END, f"#{i}\n")
                self.format_headphone(hp)
                self.results_text.insert(tk.END, "\n")

        self.results_text.config(state='disabled')
        self.analyze_btn.config(state='normal', text="🤖 Start Analysis")

    def format_headphone(self, hp):
        """Format headphone information"""
        stars = "⭐" * int(hp.user_rating)
        anc = "Yes" if hp.noise_cancellation else "No"

        self.results_text.insert(tk.END, f"  {hp.brand} {hp.model}\n")
        self.results_text.insert(tk.END, f"  Price: ${hp.price:.2f} | Rating: {stars} {hp.user_rating}/5.0 ({hp.user_reviews:,})\n")
        self.results_text.insert(tk.END, f"  Type: {hp.hp_type} | Bass: {hp.bass_level} | Profile: {hp.sound_profile} | ANC: {anc}\n")
        self.results_text.insert(tk.END, "-" * 95 + "\n")

    def clear_selections(self):
        """Clear selections"""
        self.songs_listbox.selection_clear(0, tk.END)
        self.selected_songs = []
        self.use_case_var.set("")
        self.selected_use_case = None
        self.counter_label.config(text="0/5")
        self.analyze_btn.config(state='disabled')
        messagebox.showinfo("Cleared", "Selections cleared. Genre preserved.")

    def reset(self):
        """Reset application"""
        self.selected_genre = None
        self.selected_songs = []
        self.selected_use_case = None
        self.filtered_songs = []

        self.genre_listbox.selection_clear(0, tk.END)
        self.songs_listbox.delete(0, tk.END)
        self.use_case_var.set("")
        self.search_var.set("")
        self.counter_label.config(text="0/5")
        self.analyze_btn.config(state='disabled')

        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "Welcome! Complete the 3 steps above to get recommendations.\n\n"
                                       "Instructions:\n"
                                       "1. Select a genre from the left\n"
                                       "2. Select 5 songs (Click on songs)\n"
                                       "3. Choose use case and click Analyze")
        self.results_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = MusicMatchModernApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()