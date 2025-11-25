"""
Quick script to check the columns in spotify_songs.csv
"""
import pandas as pd

try:
    df = pd.read_csv('spotify_songs.csv')
    print("Columns in spotify_songs.csv:")
    print(df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")