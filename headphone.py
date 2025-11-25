"""
Headphone Class
Represents a headphone model with specifications
"""


class Headphone:
    def __init__(self, headphone_id, brand, model, price, hp_type,
                 use_case, bass_level, sound_profile, noise_cancellation):
        """Initialize a Headphone object"""
        self.headphone_id = headphone_id
        self.brand = brand
        self.model = model
        self.price = float(price)
        self.hp_type = hp_type
        self.use_case = use_case
        self.bass_level = bass_level
        self.sound_profile = sound_profile
        self.noise_cancellation = noise_cancellation == "Yes"

    def matches_use_case(self, use_case):
        """Check if headphone matches the use case"""
        return self.use_case.lower() == use_case.lower()

    def __str__(self):
        """String representation of the headphone"""
        return f"{self.brand} {self.model} - ${self.price} ({self.use_case})"