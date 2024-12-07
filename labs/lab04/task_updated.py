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


def calculate_student_subject_average(student: dict, subject_name: str) -> dict:
    try:
        subject = student.get("subjects", {}).get(subject_name, {})
        if subject and "grades" in subject:
            return {"success": True, "data": mean(subject["grades"]), "message": "Data computed successfully"}
        else:
            return {"success": False, "data": 0.0, "message": f"Subject '{subject_name}' not found for the student"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating student subject average for "
                                                          f"{subject_name}: {e}"}


def calculate_student_overall_average(student: dict) -> dict:
    try:
        all_grades = [
            grade for subject in student["subjects"].values()
            for grade in subject["grades"]
        ]
        avg = mean(all_grades) if all_grades else 0.0
        return {"success": True, "data": avg, "message": "Data computed successfully"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating overall student average: {e}"}


def calculate_student_subject_attendance(student: dict, subject_name: str) -> dict:
    try:
        subject = student.get("subjects", {}).get(subject_name, {})
        if subject and "attendance" in subject:
            attendance_days = list(subject.get("attendance").values())
            attendance = (sum(attendance_days) / len(attendance_days)) * 100.0 if attendance_days else 0.0
            return {"success": True, "data": attendance, "message": "Data computed successfully"}
        else:
            return {"success": False, "data": 0.0, "message": f"Subject '{subject_name}' not found for the student"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating attendance for {subject_name}: {e}"}


def calculate_class_subject_average(class_data: dict, subject_name: str) -> dict:
    try:
        all_grades = [
            grade for student in class_data.get("students", [])
            for grade in student.get("subjects", {}).get(subject_name, {}).get("grades", [])
        ]
        avg = mean(all_grades) if all_grades else 0.0
        return {"success": True, "data": avg, "message": "Data computed successfully"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating class average for {subject_name}: {e}"}


def calculate_year_subject_average(year: dict, subject_name: str) -> dict:
    try:
        all_grades = [
            grade for class_data in year.values()
            for student in class_data.get("students", [])
            for grade in student.get("subjects", {}).get(subject_name, {}).get("grades", [])
        ]
        avg = mean(all_grades) if all_grades else 0.0
        return {"success": True, "data": avg, "message": "Data computed successfully"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating year average for {subject_name}: {e}"}


def calculate_student_overall_attendance(student: dict) -> dict:
    try:
        all_attendance = [
            attended for subject in student.get("subjects", {}).values()
            for attended in subject.get("attendance", {}).values()
        ]
        attendance = (sum(all_attendance) / len(all_attendance)) * 100.0 if all_attendance else 0.0
        return {"success": True, "data": attendance, "message": "Data computed successfully"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating overall attendance for student: {e}"}


def calculate_class_attendance_on_date(class_data: dict, date: str) -> dict:
    try:
        all_attendance = [
            student.get("subjects", {}).get(subject, {}).get("attendance", {}).get(date)
            for student in class_data.get("students", [])
            for subject in student.get("subjects", {})
        ]
        valid_attendance = [attended for attended in all_attendance if attended is not None]
        attendance = (sum(valid_attendance) / len(valid_attendance)) * 100.0 if valid_attendance else 0.0
        return {"success": True, "data": attendance, "message": "Data computed successfully"}
    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error calculating class attendance for date {date}: {e}"}


def create_school_summary(school_data: dict) -> dict:
    summary = {}
    try:
        for year_name, year_data in school_data.get("classes", {}).items():
            year_summary = {
                "total_students": sum(len(class_data.get("students", [])) for class_data in year_data.values()),
                "subject_averages": {
                    subject: calculate_year_subject_average(year_data, subject).get("data")
                    for subject in {subject for class_data in year_data.values()
                                    for student in class_data.get("students", [])
                                    for subject in student.get("subjects", {}).keys()}
                }
            }
            summary[year_name] = year_summary

    except Exception as e:
        return {"success": False, "data": 0.0, "message": f"Error creating school summary: {e}"}

    return {"success": True, "data": summary, "message": "Data computed successfully"}


if __name__ == "__main__":
    logging.basicConfig(filename="school.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO)
    logger = logging.getLogger()

    school_1 = read_school_data("school_saved.txt")

    student_1 = school_1["classes"]["year_1"]["class_a"]["students"][0]
    student_1_english_avg = calculate_student_subject_average(student_1, "english")
    if student_1_english_avg.get("success"):
        logger.info(f"Average grade for english for the first student of the class 1a: "
                    f"{student_1_english_avg.get('data'):.2f}")
    else:
        logger.warning(student_1_english_avg.get("message"))

    student_1_overall_avg = calculate_student_overall_average(student_1)
    if student_1_overall_avg.get("success"):
        logger.info(f"Average overall grade for the first student of the class 1a: "
                    f"{student_1_overall_avg.get('data'):.2f}")
    else:
        logger.warning(student_1_overall_avg.get("message"))

    student_1_english_attendance = calculate_student_subject_attendance(student_1, "english")
    if student_1_english_attendance.get("success"):
        logger.info(f"Attendance of the first student of the class 1a for english: "
                    f"{student_1_english_attendance.get('data'):.2f}%")
    else:
        logger.warning(student_1_english_attendance.get("message"))

    student_1_overall_attendance = calculate_student_overall_attendance(student_1)
    if student_1_overall_attendance.get("success"):
        logger.info(f"Overall attendance of the first student of the class 1a: "
                    f"{student_1_overall_attendance.get('data'):.2f}%")
    else:
        logger.warning(student_1_overall_attendance.get("message"))

    class_2b = school_1["classes"]["year_2"]["class_b"]
    class_2b_french_avg = calculate_class_subject_average(class_2b, "french")
    if class_2b_french_avg.get("success"):
        logger.info(f"Average grade for class 2b for french: "
                    f"{class_2b_french_avg.get('data'):.2f}")
    else:
        logger.warning(class_2b_french_avg.get("message"))

    class_2b_attendance = calculate_class_attendance_on_date(class_2b, "2024-09-03")
    if class_2b_attendance.get("success"):
        logger.info(f"Attendance of the class 2b on 2024-09-03: "
                    f"{class_2b_attendance.get('data'):.2f}%")
    else:
        logger.warning(class_2b_attendance.get("message"))

    year_1 = school_1["classes"]["year_1"]
    year_1_chemistry_avg = calculate_year_subject_average(year_1, "chemistry")
    if year_1_chemistry_avg.get("success"):
        logger.info(f"Average grade for year 1 for chemistry: "
                    f"{year_1_chemistry_avg.get('data'):.2f}")
    else:
        logger.warning(year_1_chemistry_avg.get("message"))

    school_1["classes"]["year_2"]["class_c"]["students"][2]["subjects"]["physics"]["grades"].append(5.0)
    save_school_data(school_1, "school_updated.txt")

    school_2 = read_school_data("school_updated.txt")
    school_summary = create_school_summary(school_2)
    if school_summary.get("success"):
        save_school_data(school_summary.get("data"), "school_summary.txt")
    else:
        logger.warning(school_summary.get("message"))
