"""
Headphone Class
Represents a headphone model with specifications
"""

class Headphone:
    def __init__(self, headphone_id, brand, model, price, hp_type,
                 use_case, bass_level, sound_profile, noise_cancellation,
                 user_rating, user_reviews):
        """Initialize a Headphone object"""
        self.headphone_id = headphone_id
        self.brand = brand
        self.model = model
        self.price = float(price)
        self.hp_type = hp_type
        self.use_case = use_case  # workout, casual, studio, gaming
        self.bass_level = bass_level  # low, medium, high
        self.sound_profile = sound_profile  # balanced, bass-heavy, flat
        self.noise_cancellation = noise_cancellation == "Yes"
        self.user_rating = float(user_rating)
        self.user_reviews = int(user_reviews)

    def matches_use_case(self, use_case):
        """Check if headphone matches the use case"""
        return self.use_case.lower() == use_case.lower()

    def get_category(self):
        """Categorize headphone by price"""
        if self.price < 150:
            return "Budget-Friendly"
        elif self.price > 400:
            return "Best of the Line"
        else:
            return "Best of Both"

    def __str__(self):
        """String representation of the headphone"""
        return f"{self.brand} {self.model} - ${self.price:.0f}"

    def get_detailed_info(self):
        """Get detailed information string"""
        nc_status = "Yes" if self.noise_cancellation else "No"
        return (f"{self.brand} {self.model}\n"
                f"Price: ${self.price:.0f} | Rating: ⭐ {self.user_rating}/5.0 ({self.user_reviews:,} reviews)\n"
                f"Type: {self.hp_type} | Use: {self.use_case}\n"
                f"Bass: {self.bass_level} | Profile: {self.sound_profile}\n"
                f"Noise Cancellation: {nc_status}")