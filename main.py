"""
Music Match Headphones - Milestone Submission
Main GUI Application
Date: [Your Date]
Authors: Haihan Zhang, Anish Suresh Saini
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from song import Song
from headphone import Headphone


class MusicMatchApp:
    def __init__(self, root):
        """Initialize the Music Match Headphones application"""
        self.root = root
        self.root.title("Music Match Headphones - Milestone")
        self.root.geometry("800x600")

        # Load data
        self.songs = []
        self.headphones = []
        self.load_data()

        # Create GUI
        self.create_gui()

    def load_data(self):
        """Load song and headphone data from CSV files"""
        try:
            # Load songs from spotify_songs.csv
            print("Loading spotify_songs.csv...")
            songs_df = pd.read_csv('data/spotify_songs.csv')

            # Strip whitespace from column names (fixes the leading spaces issue)
            songs_df.columns = songs_df.columns.str.strip()

            print(f"Available columns: {songs_df.columns.tolist()}")
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

            # Get unique genres first
            unique_genres = songs_df['playlist_genre'].unique()
            print(f"Found {len(unique_genres)} unique genres: {unique_genres}")

            # Count songs per genre
            for genre in unique_genres:
                count = len(songs_df[songs_df['playlist_genre'] == genre])
                print(f"  {genre}: {count} songs")

            # Sample songs evenly from each genre
            songs_per_genre = 300  # Adjust this number based on your needs
            sampled_songs = []

            for genre in unique_genres:
                genre_songs = songs_df[songs_df['playlist_genre'] == genre]
                # Sample randomly from each genre (or take all if less than songs_per_genre)
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
                        row['noise_cancellation']
                    )
                    self.headphones.append(headphone)
                except Exception as e:
                    print(f"Error loading headphone: {e}")
                    continue

            print(f"Loaded {len(self.headphones)} headphones")

            messagebox.showinfo("Success",
                                f"Loaded {len(self.songs)} songs across {len(unique_genres)} genres\n"
                                f"and {len(self.headphones)} headphones")

        except FileNotFoundError as e:
            messagebox.showerror("Error",
                                 f"Data file not found: {e}\n\n"
                                 f"Make sure spotify_songs.csv and headphones.csv are in the same directory as main.py")
        except KeyError as e:
            messagebox.showerror("Error",
                                 f"Column not found in CSV: {e}\n\n"
                                 f"Please check your CSV file structure.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

    def create_gui(self):
        """Create the GUI elements"""
        # Title
        title_label = tk.Label(self.root, text="Music Match Headphones",
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Instructions
        instructions = tk.Label(self.root,
                                text="Select your music preferences to get headphone recommendations",
                                font=("Arial", 12))
        instructions.pack(pady=10)

        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        # Genre selection (Interactive Element 1)
        tk.Label(control_frame, text="Favorite Genre:", font=("Arial", 11)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.genre_var = tk.StringVar()
        genres = list(set([song.playlist_genre for song in self.songs]))
        self.genre_combo = ttk.Combobox(control_frame, textvariable=self.genre_var,
                                        values=genres, state="readonly", width=20)
        self.genre_combo.grid(row=0, column=1, padx=10, pady=10)
        if genres:
            self.genre_combo.current(0)

        # Use case selection (Interactive Element 2)
        tk.Label(control_frame, text="Use Case:", font=("Arial", 11)).grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.use_case_var = tk.StringVar(value="Casual")
        use_cases = ["Workout", "Casual", "Studio"]
        for i, case in enumerate(use_cases):
            rb = tk.Radiobutton(control_frame, text=case, variable=self.use_case_var,
                                value=case, font=("Arial", 10))
            rb.grid(row=1, column=i + 1, padx=5, pady=10)

        # Get Recommendations button (Interactive Element 3)
        recommend_btn = tk.Button(self.root, text="Get Recommendations",
                                  command=self.get_recommendations,
                                  font=("Arial", 12), bg="#4CAF50", fg="white",
                                  padx=20, pady=10)
        recommend_btn.pack(pady=20)

        # Results display area
        results_frame = tk.Frame(self.root)
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        tk.Label(results_frame, text="Recommendations:",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        # Text widget with scrollbar (Interactive Element 4 - scrollbar)
        self.results_text = tk.Text(results_frame, height=10, width=70,
                                    font=("Arial", 10), wrap="word")
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)

        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # View All Data button (Interactive Element 5)
        view_data_btn = tk.Button(self.root, text="View All Songs",
                                  command=self.view_all_songs,
                                  font=("Arial", 11), bg="#2196F3", fg="white",
                                  padx=15, pady=8)
        view_data_btn.pack(pady=10)

    def get_recommendations(self):
        """Get headphone recommendations based on user preferences"""
        genre = self.genre_var.get()
        use_case = self.use_case_var.get()

        if not genre:
            messagebox.showwarning("Warning", "Please select a genre")
            return

        # Filter songs by genre
        genre_songs = [song for song in self.songs if song.playlist_genre == genre]

        # Calculate average energy for the genre
        if genre_songs:
            avg_energy = sum([song.energy for song in genre_songs]) / len(genre_songs)
        else:
            avg_energy = 0.5

        # Filter headphones by use case
        matching_headphones = [hp for hp in self.headphones
                               if hp.matches_use_case(use_case)]

        # Display results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END,
                                 f"Based on your {genre} preference and {use_case} use case:\n\n")
        self.results_text.insert(tk.END,
                                 f"Average energy level: {avg_energy:.2f}\n")
        self.results_text.insert(tk.END,
                                 f"Songs analyzed: {len(genre_songs)}\n\n")
        self.results_text.insert(tk.END, "Recommended Headphones:\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n")

        if matching_headphones:
            for hp in matching_headphones:
                self.results_text.insert(tk.END, f"\n• {hp}\n")
                self.results_text.insert(tk.END,
                                         f"  Sound Profile: {hp.sound_profile}\n")
                self.results_text.insert(tk.END,
                                         f"  Bass Level: {hp.bass_level}\n")
        else:
            self.results_text.insert(tk.END, "\nNo matching headphones found.\n")

    def view_all_songs(self):
        """Display all loaded songs in a new window"""
        songs_window = tk.Toplevel(self.root)
        songs_window.title("All Songs")
        songs_window.geometry("600x400")

        # Create text widget with scrollbar
        text_frame = tk.Frame(songs_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 10))
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display songs
        for i, song in enumerate(self.songs[:50], 1):  # Limit to first 50
            text_widget.insert(tk.END, f"{i}. {song}\n")

        text_widget.config(state="disabled")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = MusicMatchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()