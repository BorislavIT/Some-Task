from numpy import true_divide
from database_service import database_service
from patient import Patient
import datetime


def query_yes_no(question):
    valid = {"да": "yes", "yes": "yes", "y": "yes",
             "ye": "yes", "no": "no", "n": "no", "не": "no"}
    print(question)
    while True:
        choice = input().lower()
        if choice and choice in valid:
            if valid[choice] == "yes":
                return True
            else:
                return False
        else:
            print("Invalid answer, choose 'yes' or 'no'")


def get_patient():
    name, age, previous_diseases, cough, temperature, stuffed_nose, diziness, lack_of_taste, lack_of_smell, headache = collect_basic_info()

    patient_pcr = collect_patient_pcr()

    patient_other_test = collect_patient_other_test()

    day_since_symptomps_input = int(input("Days since first symptom: "))
    day_since_symptomps = datetime.datetime.strptime(datetime.datetime.now(
    ).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.timedelta(day_since_symptomps_input)

    return Patient(name, age, previous_diseases, cough, temperature, stuffed_nose, diziness,
                   lack_of_taste, lack_of_smell, headache, patient_pcr, patient_other_test, day_since_symptomps)


def collect_patient_other_test():
    patient_other_test = None
    patient_other_test_exists = query_yes_no("Any other test available? ")
    if (patient_other_test_exists):
        patient_other_test_is_positive = query_yes_no(
            "Is the other test positive? ")
        if patient_other_test_is_positive:
            patient_other_test = True
        else:
            patient_other_test = False
    return patient_other_test


def collect_patient_pcr():
    patient_pcr = None
    pcr_exists = query_yes_no("PCR Test available? ")
    if (pcr_exists):
        pcr_is_positive = query_yes_no("Is the PCR Test positive? ")
        if pcr_is_positive:
            patient_pcr = True
        else:
            patient_pcr = False
    return patient_pcr


def collect_basic_info():
    name = input("Name: ")
    age = int(input("Age: "))
    previous_diseases = input("Previous diseases: ")
    cough = query_yes_no("Presence of cough: ")
    temperature = query_yes_no("High temperature? ")
    stuffed_nose = query_yes_no("Stuffed nose? ")
    diziness = query_yes_no("Diziness? ")
    lack_of_taste = query_yes_no("Lack of taste? ")
    lack_of_smell = query_yes_no("Lack of smell? ")
    headache = query_yes_no("Headache? ")
    return name, age, previous_diseases, cough, temperature, stuffed_nose, diziness, lack_of_taste, lack_of_smell, headache


def main():
    db_service = database_service()
    command = ""
    while (True):
        print("1. Add a new patient")
        print("2. Give extra information about an existing patient")
        print("3. Get information about a patient")
        print("4. Exit")

        command = input()
        if command == "1":
            db_service.add_patient(get_patient())
        elif command == "2":
            print("Please enter patient id:")
            patient_id = input()
            db_service.update_patient(patient_id)
        elif command == "3":
            print("Please enter patient id:")
            patient_id = input()
            patient = db_service.get_patient(patient_id)
            if not patient:
                print("Patient not found")
            else:
                print_patient_full_information(patient)
        elif command == "4":
            break
        else:
            print("Invalid command!")


def print_patient_full_information(patient):
    print("------- Patient: ", patient.name)
    print("------- Age: ", patient.age)
    if patient.cough:
        if patient.cough_type == 1:
            print("------- Cough: wet coughing")
        else:
            print("------- Cough: dry coughing")
    if patient.stuffed_nose:
        if patient.stuffed_nose_level == 1:
            print("------- Stuffed nose: only a little bit of snots")
        elif patient.stuffed_nose_level == 2:
            print("------- Stuffed nose: trouble breathing")
        else:
            print("------- Stuffed nose: can't breath at all")
    if patient.temperature:
        print("------- Temperature in Celsius :",
              patient.temperature_value)
    if patient.diziness:
        if patient.diziness_level == 1:
            print("------- Diziness: feel lightweighted")
        elif patient.diziness_level == 2:
            print("------- Diziness: my head is spinning")
        else:
            print("------- Diziness: I can't stand up without falling")
    if patient.lack_of_smell:
        if patient.lack_of_smell_level == 1:
            print("------- Lack of Smell: can smell only STRONG smells")
        else:
            print(
                "------- Lack of Smell: completely lacking the feeling of smell")
    if patient.lack_of_taste:
        if patient.lack_of_taste_level == 1:
            print("------- Lack of Taste: can taste only STRONG flavors")
        else:
            print(
                "------- Lack of Taste: completely lacking the feeling of taste")
    if patient.headache:
        if patient.headache_level == 1:
            print("------- Headache: I feel like my head is pulsating ")
        else:
            print(
                "------- Headache: I cannot focus/think about anything ")
    print("------- Overall feeling:", patient.overall_feeling)
    print("------- Diagnosis made on:", patient.date_of_creation)


if __name__ == "__main__":
    main()
