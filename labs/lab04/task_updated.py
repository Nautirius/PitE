import logging
import json
from statistics import mean


def save_school_data(school_data: dict, file_name: str = "school.txt") -> None:
    try:
        with open(file_name, "w") as f:
            json.dump(school_data, f, indent=4)
    except TypeError as e:
        logger.warning(f"Unable to save data to file {file_name}: {e}")


def read_school_data(file_name: str = "school.txt") -> dict:
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except OSError as e:
        logger.warning(f"Unable to read data from file {file_name}: {e}")
        return {}
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON syntax in file {file_name}: {e}")
        return {}


def calculate_student_subject_average(student: dict, subject_name: str) -> float:
    try:
        subject = student.get("subjects", {}).get(subject_name, {})
        if subject and "grades" in subject:
            return mean(subject["grades"])
        else:
            logger.warning(f"Subject '{subject_name}' not found for the student")
            return 0.0
    except Exception as e:
        logger.warning(f"Error calculating student subject average for {subject_name}: {e}")
        return 0.0


def calculate_student_overall_average(student: dict) -> float:
    try:
        all_grades = [
            grade for subject in student["subjects"].values()
            for grade in subject["grades"]
        ]
        return mean(all_grades) if all_grades else 0.0
    except Exception as e:
        logger.warning(f"Error calculating overall student average: {e}")
        return 0.0


def calculate_student_subject_attendance(student: dict, subject_name: str) -> float:
    try:
        subject = student.get("subjects", {}).get(subject_name, {})
        if subject and "attendance" in subject:
            attendance_days = list(subject.get("attendance").values())
            return (sum(attendance_days) / len(attendance_days)) * 100.0 if attendance_days else 0.0
        else:
            logger.warning(f"Subject '{subject_name}' not found for the student")
            return 0.0
    except Exception as e:
        logger.warning(f"Error calculating attendance for {subject_name}: {e}")
        return 0.0


def calculate_class_subject_average(class_data: dict, subject_name: str) -> float:
    try:
        all_grades = [
            grade for student in class_data.get("students", [])
            for grade in student.get("subjects", {}).get(subject_name, {}).get("grades", [])
        ]
        return mean(all_grades) if all_grades else 0.0
    except Exception as e:
        logger.warning(f"Error calculating class average for {subject_name}: {e}")
        return 0.0


def calculate_year_subject_average(year: dict, subject_name: str) -> float:
    try:
        all_grades = [
            grade for class_data in year.values()
            for student in class_data.get("students", [])
            for grade in student.get("subjects", {}).get(subject_name, {}).get("grades", [])
        ]
        return mean(all_grades) if all_grades else 0.0
    except Exception as e:
        logger.warning(f"Error calculating year average for {subject_name}: {e}")
        return 0.0


def calculate_student_overall_attendance(student: dict) -> float:
    try:
        all_attendance = [
            attended for subject in student.get("subjects", {}).values()
            for attended in subject.get("attendance", {}).values()
        ]
        return (sum(all_attendance) / len(all_attendance)) * 100.0 if all_attendance else 0.0
    except Exception as e:
        logger.warning(f"Error calculating overall attendance for student: {e}")
        return 0.0


def calculate_class_attendance_on_date(class_data: dict, date: str) -> float:
    try:
        all_attendance = [
            student.get("subjects", {}).get(subject, {}).get("attendance", {}).get(date)
            for student in class_data.get("students", [])
            for subject in student.get("subjects", {})
        ]
        valid_attendance = [attended for attended in all_attendance if attended is not None]
        return (sum(valid_attendance) / len(valid_attendance)) * 100.0 if valid_attendance else 0.0
    except Exception as e:
        logger.warning(f"Error calculating class attendance for date {date}: {e}")
        return 0.0


def create_school_summary(school_data: dict) -> dict:
    summary = {}
    try:
        for year_name, year_data in school_data.get("classes", {}).items():
            year_summary = {
                "total_students": sum(len(class_data.get("students", [])) for class_data in year_data.values()),
                "subject_averages": {
                    subject: calculate_year_subject_average(year_data, subject)
                    for subject in {subject for class_data in year_data.values()
                                    for student in class_data.get("students", [])
                                    for subject in student.get("subjects", {}).keys()}
                }
            }
            summary[year_name] = year_summary

    except Exception as e:
        logging.warning(f"Error creating school summary: {e}")

    return summary


if __name__ == "__main__":
    logging.basicConfig(filename="school.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO)
    logger = logging.getLogger()

    school_1 = read_school_data("school_saved.txt")

    student_1 = school_1["classes"]["year_1"]["class_a"]["students"][0]
    student_1_english_avg = calculate_student_subject_average(student_1, "english")
    logger.info(f"Average grade for english for the first student of the class 1a: {student_1_english_avg:.2f}")

    student_1_overall_avg = calculate_student_overall_average(student_1)
    logger.info(f"Average overall grade for the first student of the class 1a: {student_1_overall_avg:.2f}")

    student_1_english_attendance = calculate_student_subject_attendance(student_1, "english")
    logger.info(f"Attendance of the first student of the class 1a for english: {student_1_english_attendance:.2f}%")

    student_1_overall_attendance = calculate_student_overall_attendance(student_1)
    logger.info(f"Overall attendance of the first student of the class 1a: {student_1_overall_attendance:.2f}%")

    class_2b = school_1["classes"]["year_2"]["class_b"]
    class_2b_french_avg = calculate_class_subject_average(class_2b, "french")
    logger.info(f"Average grade for class 2b for french: {class_2b_french_avg:.2f}")

    class_2b_attendance = calculate_class_attendance_on_date(class_2b, "2024-09-03")
    logger.info(f"Attendance of the class 2b on 2024-09-03: {class_2b_attendance:.2f}%")

    year_1 = school_1["classes"]["year_1"]
    year_1_chemistry_avg = calculate_year_subject_average(year_1, "chemistry")
    logger.info(f"Average grade for year 1 for chemistry: {year_1_chemistry_avg:.2f}")

    school_1["classes"]["year_2"]["class_c"]["students"][2]["subjects"]["physics"]["grades"].append(5.0)
    save_school_data(school_1, "school_updated.txt")

    school_2 = read_school_data("school_updated.txt")
    school_summary = create_school_summary(school_2)
    save_school_data(school_summary, "school_summary.txt")
