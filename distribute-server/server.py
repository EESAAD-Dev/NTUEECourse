import os
from pymongo import MongoClient
from flask import Flask, request, Response
import sys


from algorithm import Algorithm, Course, Student
from statistics import Analysis
# ========================================

app = Flask(__name__)

PORT = os.environ.get("PORT", 8001)
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DBNAME = os.environ.get("MONGO_DBNAME", "ntuee-course")
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")

url = "mongodb://%s:%s@%s/%s" % (MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_DBNAME)
client = MongoClient(url)
# ========================================


def genCourse(raw_courses):
    courses = []
    for data in raw_courses.find():
        courseDict = {}

        courseDict["name"] = data["name"]
        courseDict["id"] = data["id"]
        courseDict["type"] = data["type"]
        courseDict["number"] = data["number"]
        courseDict["students"] = data["students"]
        courseDict["options"] = {}
        for op in data["options"]:
            option = {
                "limit": op["limit"],
            }
            if data["type"] in "1234":
                option["priority_type"] = "higher-grade-first"
                option["priority_value"] = "0"
            elif data["type"] in "Ten-Select-Two":
                option["priority_type"] = op["priority_type"]
                option["priority_value"] = op["priority_value"]
            elif data["type"] == "EE-Lab":
                option["priority_type"] = "none"
                option["priority_value"] = "0"
            else:
                raise ValueError("Invalid type")
            courseDict["options"][op["name"]] = option
        courses.append(Course(courseDict))

    return courses


def getCourseid(raw_courses):
    name = []
    for data in raw_courses.find():
        name.append(data["id"])
    return name


def genStudent(raw_student, raw_selections, course_id):
    students = []
    for data in raw_student.find():  # iterate through all students
        result_selection = {}
        for name in course_id:  # iterate through every course
            result_selection[name] = []
            # all selections made by a student of certain course
            student_selections = raw_selections.find(
                {"userID": data["userID"], "courseID": name})
            for i in range(len(list(student_selections))):
                rank_i_selection = raw_selections.find(
                    {"userID": data["userID"], "courseID": name, "ranking": i + 1})  # the (i+1)th selection
                for ith_option in rank_i_selection:
                    result_selection[name].append(ith_option["name"])

        students.append(
            Student(data["name"], data["userID"], result_selection, data["grade"]))
    return students


def genPreselect(raw_preselects):
    preselects = []
    for data in raw_preselects.find():
        preselects.append(data["userID"])
    return preselects

# ========================================
@app.route("/")
def index():
    return "Distribute server"

@app.route("/distribute", methods=["POST"])
def distribute():
    db = client[MONGO_DBNAME]
    raw_selections = db["selections"]
    raw_students = db["students"]
    raw_courses = db["courses"]

    try:
        courses = genCourse(raw_courses)
    except ValueError:
        return "Invalid course type detected", 400

    course_names = getCourseid(raw_courses)
    students = genStudent(raw_students, raw_selections, course_names)


    results = Algorithm.distribute(courses, students)
    db.results.delete_many({})

    if len(results) > 0:
        db.results.insert_many(results)
        
    # client.close()
    return ""


@app.route("/specific_distribute", methods=["POST"])
def specific_distribute():
    db = client[MONGO_DBNAME]
    raw_selections = db["selections"]
    raw_students = db["students"]
    raw_courses = db["courses"]
    raw_preselects = db["preselects"]
    student_in_course_data = {}
    for data in request.get_json():
        student_in_course_data[data["course_id"]] = data["students"]

    db.results.delete_many({})

    course_names = getCourseid(raw_courses)

    if len(student_in_course_data) == 0:

        try:
            courses = genCourse(raw_courses)
        except ValueError:
            return "Invalid course type detected", 400

        students = genStudent(raw_students, raw_selections, course_names)

        preselects = genPreselect(raw_preselects)

        results = Algorithm.distribute(courses, students, preselects)
        # results = Algorithm.distribute(courses, students)
        if len(results) > 0:
            db.results.insert_many(results)
    else:
        results = []
        for course_name in course_names:

            try:
                # courses = genCourse(raw_courses, course_name=course_name)
                courses = genCourse(raw_courses)
            except ValueError:
                return "Invalid course type detected", 400

            # students = genStudent(raw_students, raw_selections, course_names,
            #         student_in_course_data)
            students = genStudent(raw_students, raw_selections, course_names)

            preselects = genPreselect(raw_preselects)

            # result = Algorithm.distribute(courses, students, preselects)
            result = Algorithm.distribute(courses, students)
            results.extend(result)
        if len(results) > 0:
            db.results.insert_many(results)

    # client.close()
    return ""

@app.route("/new_distribute", methods=["POST"])
def new_distribute():
    client = MongoClient(url)
    db = client[MONGO_DBNAME]
    raw_selections = db["selections"]
    raw_students = db["students"]
    raw_courses = db["courses"]

    db.results.delete_many({})

    course_names = getCourseid(raw_courses)

    try:
        courses = genCourse(raw_courses)
    except ValueError:
        return "Invalid course type detected", 400

    students = genStudent(raw_students, raw_selections, course_names)

    results = Algorithm.distribute(courses, students)
    if len(results) > 0:
        db.results.insert_many(results)
    print(results, file=sys.stderr)
    print(db.results, file=sys.stderr)

    # client.close()
    return ""


@app.route("/statistics", methods=["GET"])
def statistics():
    db = client[MONGO_DBNAME]
    raw_selections = db["selections"]
    raw_students = db["students"]
    raw_courses = db["courses"]
    raw_results = db["results"]

    try:
        courses = genCourse(raw_courses)
    except ValueError:
        return "Invalid course type detected", 400

    course_names = getCourseid(raw_courses)
    students = genStudent(raw_students, raw_selections, course_names)
    results = [result for result in raw_results.find()]
    
    analysis = Analysis(courses, students, results)
    analysis.analyze()
    analysis.analyze_grade()
    analysis.analyze_selection_grade()
    analysis.analyze_selection_result()
    csv_string = analysis.to_csv()
    return Response(csv_string, mimetype='text/plain')
# ========================================


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
