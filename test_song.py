"""
Tests for Song and Headphone classes
"""
import pytest
from song import Song
from headphone import Headphone

def test_song_creation():
    """Test creating a Song object"""
    song = Song("123", "Test Song", "Test Artist", 75, "Pop", "dance pop",
                0.8, 0.9, 0.7, 120, 0.1, -5.0)
    assert song.track_name == "Test Song"
    assert song.energy == 0.9

def test_song_get_energy():
    """Test getting song energy"""
    song = Song("123", "Test", "Artist", 50, "Rock", "rock",
                0.5, 0.7, 0.6, 110, 0.2, -4.0)
    assert song.get_avg_energy() == 0.7

def test_headphone_creation():
    """Test creating a Headphone object"""
    hp = Headphone("1", "Sony", "WH-1000XM5", 399, "Over-ear",
                   "Casual", "Medium", "Balanced", "Yes")
    assert hp.brand == "Sony"
    assert hp.noise_cancellation == True

def test_headphone_matches_use_case():
    """Test headphone use case matching"""
    hp = Headphone("1", "Sony", "Model", 300, "Over-ear",
                   "Workout", "High", "Bass-heavy", "Yes")
    assert hp.matches_use_case("Workout") == True
    assert hp.matches_use_case("Studio") == False

def test_song_str():
    """Test Song string representation"""
    song = Song("123", "Great Song", "Amazing Artist", 80, "EDM", "electro",
                0.9, 0.95, 0.8, 128, 0.05, -3.0)
    assert "Great Song" in str(song)
    assert "Amazing Artist" in str(song)