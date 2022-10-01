class Patient:
    def __init__(self, name, age, previous_diseases, cough, temperature, stuffed_nose, diziness, lack_of_taste, lack_of_smell, headache, pcr_test, other_test, day_since_symptomps):
        self.name = name
        self.age = age
        self.previous_diseases = previous_diseases
        self.cough = cough
        self.temperature = temperature
        self.stuffed_nose = stuffed_nose
        self.diziness = diziness
        self.lack_of_taste = lack_of_taste
        self.lack_of_smell = lack_of_smell
        self.headache = headache
        self.pcr_test = pcr_test
        self.other_test = other_test
        self.day_since_symptomps = day_since_symptomps
        self.cough_type = None
        self.temperature_value = None
        self.stuffed_nose_level = None
        self.diziness_level = None
        self.lack_of_taste_level = None
        self.lack_of_smell_level = None
        self.headache_level = None
        self.overall_feeling = None
        self.date_of_creation = None
