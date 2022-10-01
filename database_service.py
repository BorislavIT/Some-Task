from datetime import datetime
import sqlite3

from patient import Patient


class database_service:
    patient_mapping_table = {
        "name": 1,
        "age": 2,
        "previous_diseases": 3,
        "cough": 4,
        "cough_type": 5,
        "temperature": 6,
        "temperature_value": 7,
        "stuffed_nose": 8,
        "stuffed_nose_level": 9,
        "diziness": 10,
        "diziness_level": 11,
        "lack_of_taste": 12,
        "lack_of_taste_level": 13,
        "lack_of_smell": 14,
        "lack_of_smell_level": 15,
        "headache": 16,
        "headache_level": 17,
        "day_since_symptomps": 18,
        "date_of_creation": 19,
        "overall_feeling": 20,
        "pcr_test": 21,
        "other_test": 22
    }

    def __init__(self):
        self.conn = sqlite3.connect('covid.db')
        self.cur = self.conn.cursor()
        self.create_table_if_not_exist()

    def create_table_if_not_exist(self):
        table_schema = """
        CREATE TABLE IF NOT EXISTS patients(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Age TEXT NOT NULL,
            PreviousDiseases Boolean NOT NULL,
            Cough Boolean NOT NULL,
            CoughType INT NULL,
            Temperature Boolean NOT NULL,
            TemperatureValue INT NULL,
            StuffedNose Boolean NOT NULL,
            StuffedNoseLevel INT,
            Diziness Boolean NOT NULL,
            DiziniessLevel INT,
            LackOfTaste Boolean NOT NULL,
            LackOfTasteLevel INT,
            LackOfSmell Boolean NOT NULL,
            LackOfSmellLevel INT,
            Headache Boolean NOT NULL,
            HeadacheLevel INT,
            DaySinceSymptomps DATE NOT NULL,
            DateOfCreation DATE,
            OverAllFeeling TEXT,
            PCRTest Boolean,
            OtherTest Boolean
            );
        """
        self.cur.execute(table_schema)

    def add_patient(self, patient):
        insert_query = """
        INSERT INTO patients (Name, Age, PreviousDiseases, Cough, Temperature, StuffedNose, Diziness, LackOfTaste, LackOfSmell, Headache, DaySinceSymptomps, PCRTest, OtherTest)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.cur.execute(insert_query, (patient.name, patient.age, patient.previous_diseases, patient.cough, patient.temperature,
                         patient.stuffed_nose, patient.diziness, patient.lack_of_taste, patient.lack_of_smell, patient.headache, patient.day_since_symptomps, patient.pcr_test, patient.other_test))
        self.conn.commit()
        print("Succesfully added patient!")

    def get_patient(self, id):
        get_query = """SELECT * FROM patients WHERE Id = ?"""
        self.cur.execute(get_query, id)
        selected_patient = self.cur.fetchone()
        if not selected_patient:
            return None
        patient = Patient(selected_patient[self.patient_mapping_table["name"]],
                          selected_patient[self.patient_mapping_table["age"]],
                          selected_patient[self.patient_mapping_table["previous_diseases"]],
                          selected_patient[self.patient_mapping_table["cough"]],
                          selected_patient[self.patient_mapping_table["temperature"]],
                          selected_patient[self.patient_mapping_table["stuffed_nose"]],
                          selected_patient[self.patient_mapping_table["diziness"]],
                          selected_patient[self.patient_mapping_table["lack_of_taste"]],
                          selected_patient[self.patient_mapping_table["lack_of_smell"]],
                          selected_patient[self.patient_mapping_table["headache"]],
                          selected_patient[self.patient_mapping_table["pcr_test"]],
                          selected_patient[self.patient_mapping_table["other_test"]],
                          selected_patient[self.patient_mapping_table["day_since_symptomps"]]
                          )
        patient.stuffed_nose_level = selected_patient[self.patient_mapping_table["stuffed_nose_level"]]
        patient.diziness_level = selected_patient[self.patient_mapping_table["diziness_level"]]
        patient.lack_of_smell_level = selected_patient[self.patient_mapping_table["lack_of_smell_level"]]
        patient.lack_of_taste_level = selected_patient[self.patient_mapping_table["lack_of_taste_level"]]
        patient.headache_level = selected_patient[self.patient_mapping_table["headache_level"]]
        patient.cough_type = selected_patient[self.patient_mapping_table["cough_type"]]
        patient.temperature_value = selected_patient[self.patient_mapping_table["temperature_value"]]
        patient.overall_feeling = selected_patient[self.patient_mapping_table["overall_feeling"]]
        patient.date_of_creation = selected_patient[self.patient_mapping_table["date_of_creation"]]

        return patient

    def update_patient(self, id):
        patient = self.get_patient(id)
        if not patient:
            print("Patient not found")
            return
        print((datetime.now() -
              datetime.strptime(patient.day_since_symptomps, '%Y-%m-%d %H:%M:%S')).days, "DAYS since first sign of symptomps")
        if patient.cough:
            print("Please select cough type: [1 - wet, 2 - dry]:")
            patient.cough_type = input()
            while type(patient.cough_type) != int and int(patient.cough_type) != 1 and int(patient.cough_type) != 2:
                print(
                    "Invalid value, please select cough type: [1 - wet, 2 - dry]:")
                patient.cough_type = input()
        if patient.stuffed_nose:
            print(
                "Please select how stuffed do you feel your nose: [1 - only a little bit of snots, 2 - trouble breathing, 3 - can't breath at all]:")
            patient.stuffed_nose_level = input()
            while type(patient.stuffed_nose_level) != int and int(patient.stuffed_nose_level) != 1 and int(patient.stuffed_nose_level) != 2 and int(patient.stuffed_nose_level) != 3:
                print(
                    "Invalid value, please select how stuffed do you feel your nose: [1 - only a little bit of snots, 2 - trouble breathing, 3 - can't breath at all]:")
                patient.stuffed_nose_level = input()
        if patient.temperature:
            print(
                "Please select temperature:")
            patient.temperature_value = input()
            while type(patient.temperature_value) != int:
                print(
                    "Invalid value, please select temperature [Celsius]")
                patient.temperature_value = input()
        if patient.diziness:
            print(
                "Please select how dizzy you feel: [1 - feel lightweighted, 2 - my head is spinning, 3 - I can't stand up without falling]:")
            patient.diziness_level = input()
            while type(patient.diziness_level) != int and int(patient.diziness_level) != 1 and int(patient.diziness_level) != 2 and int(patient.diziness_level) != 3:
                print(
                    "Invalid value, please select how dizzy you feel: [1 - feel lightweighted, 2 - my head is spinning, 3 - I can't stand up without falling]:")
                patient.diziness_level = input()
        if patient.lack_of_smell:
            print(
                "Please select how much you can smell: [1 - can smell only STRONG smells (perfume, deodorant etc..), 2 - completely lacking the feeling of smell]:")
            patient.lack_of_smell_level = input()
            while type(patient.lack_of_smell_level) != int and int(patient.lack_of_smell_level) != 1 and int(patient.lack_of_smell_level) != 2:
                print(
                    "Invalid value, please select how much you can smell: [1 - can smell only STRONG smells (perfume, deodorant etc..), 2 - completely lacking the feeling of smell]:")
                patient.lack_of_smell_level = input()
        if patient.lack_of_taste:
            print(
                "Please select how much you can taste: [1 - can taste only STRONG flavors (salt, sugar etc..), 2 - completely lacking the feeling of taste]: ")
            patient.lack_of_taste = input()
            while type(patient.lack_of_taste) != int and int(patient.lack_of_taste) != 1 and int(patient.lack_of_taste) != 2:
                print(
                    "Invalid value, please select how much you can taste: [1 - can taste only STRONG flavors (salt, sugar etc..), 2 - completely lacking the feeling of taste]: ")
                patient.lack_of_taste = input()
        if patient.headache:
            print(
                "Please select how much your head hurts: [1 - I feel like my head is pulsating, 2 - I cannot focus/think about anything]:")
            patient.headache_level = input()
            while type(patient.headache_level) != int and int(patient.headache_level) != 1 and int(patient.headache_level) != 2:
                print(
                    "Invalid value, please select how much your head hurts: [1 - I feel like my head is pulsating, 2 - I cannot focus/think about anything]:")
                patient.headache_level = input()
        print("Please tell me, how you feel overall?")
        patient.overall_feeling = input()
        patient.date_of_creation = datetime.strptime(datetime.now(
        ).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        update_query = """UPDATE patients SET CoughType = ?, TemperatureValue = ?, StuffedNoseLevel = ?, DiziniessLevel = ?, LackOfTasteLevel = ?, LackOfSmellLevel = ?, HeadacheLevel = ?, DateOfCreation = ?, OverAllFeeling = ? WHERE id = ? """
        self.cur.execute(update_query, (patient.cough_type, patient.temperature_value, patient.stuffed_nose_level,
                         patient.diziness_level, patient.lack_of_taste_level, patient.lack_of_smell_level, patient.headache_level, patient.date_of_creation, patient.overall_feeling, id))
        self.conn.commit()
        print("Succesfully updated patient!")
