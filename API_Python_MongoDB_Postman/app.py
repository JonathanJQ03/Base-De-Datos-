from flask import Flask, request, jsonify  # permite manejar archivos json
from pymongo import MongoClient  # Conectarnos a la BDD

app = Flask(__name__)  # Definir el nombre de nuestra aplicacion

# Credenciales de la BDD
mongo_uri = "mongodb+srv://jjjaguaco:20030706Jq@dbapi.nfarw.mongodb.net/?retryWrites=true&w=majority&appName=DBAPI"
client = MongoClient(mongo_uri)
db = client['espe']
students_collection = db['estudiantes']

# Definición de rutas
@app.route('/students', methods=['GET'])  # la ruta con el método GET
def get_students():
    students = list(students_collection.find({}, {'_id': 0}))
    return jsonify(students)


@app.route('/students/<student_id>', methods=['GET'])
def get_students_by_id(student_id):
    student = students_collection.find_one({"student_id": student_id}, {'_id': 0})
    if student:
        return jsonify(student)
    else:

        return jsonify({"message": "Estudiante no encontrado en la BDD"}), 404

@app.route('/students/', methods=['POST'])
def add_students():
    students = request.json  # Suponiendo que envíes un array de estudiantes
    
    if not isinstance(students, list) or len(students) == 0:
        return jsonify({"message": "Debe proporcionar una lista de estudiantes"}), 400

    for student in students:
        if not student.get('student_id') or students_collection.find_one({"student_id": student["student_id"]}):
            return jsonify({"message": f"ID de estudiante {student['student_id']} es obligatorio y debe ser único"}), 400

    # Insertar todos los estudiantes de la lista
    students_collection.insert_many(students)
    return jsonify({"message": "Estudiantes insertados correctamente"}), 201



@app.route('/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    result = students_collection.delete_one({"student_id": student_id})

    if result.deleted_count:
        return jsonify({"message": "Estudiante eliminado de la BDD"}), 200
    else:
        return jsonify({"message": "No se pudo encontrar un estudiante"}), 404


if __name__ == '__main__':
    app.run(debug=True)
