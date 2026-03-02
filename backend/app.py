from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    return jsonify(db.get_all_students()), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json
    # print("Received", student_data, flush=True)

    if not student_data:
        return jsonify({"error": "Missing JSON body"}), 404
    
    name = student_data.get("name")
    course = student_data.get("course")

    if not isinstance(name, str) or name.strip() == "":
        return jsonify({"error": "Invalid or missing name"}), 404
    if not isinstance(course, str) or course.strip() == "":
        return jsonify({"error": "Invalid or missing course"}), 404

    mark = student_data.get("mark")
    try:
        mark = int(mark)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid mark"}), 404
    if mark < 0 or mark > 100:
        return jsonify({"error": "Mark must be between 0 and 100"}), 404

    created = db.insert_student(name, course, mark)
    return jsonify(created), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """

    student_data = request.get_json()
    if not student_data:
        return jsonify({"error": "Missing JSON body"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if "mark" in student_data:
        try:
            mark = int(mark)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid mark"}), 404
        if mark < 0 or mark > 100:
            return jsonify({"error": "Mark must be between 0 and 100"}), 404
    else:
        mark = None
    
    updated = db.update_student(
        student_id,
        name=name,
        course=course,
        mark=mark
    )

    if not updated:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify(updated), 200
    # pass  # replace with your implementation


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)
    if not deleted:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(deleted), 200

    # pass  # replace with your implementation


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    # pass  # replace with your implementation
    students = db.get_all_students()
    if len(students) == 0:
        return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200

    marks = [s["mark"] for s in students]
    count = len(marks)
    average = sum(marks) / count
    return jsonify(
        {
            "count": count,
            "average": average,
            "min": min(marks),
            "max": max(marks),
        }
    ), 200



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
