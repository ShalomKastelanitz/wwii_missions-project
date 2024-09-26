from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/api/mission', methods=['GET'])
def get_missions():
    query = "SELECT * FROM missions;"  # מחזיר את כל העמודות
    result = db.session.execute(query)
    missions = [{column: row[i] for i, column in enumerate(result.keys())} for row in result]
    return jsonify(missions)


@app.route('/api/mission/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    query = "SELECT * FROM missions WHERE id = :id;"
    result = db.session.execute(query, {'id': mission_id}).fetchone()

    if result is None:
        return jsonify({'error': 'Mission not found'}), 404

    mission = {column: result[i] for i, column in enumerate(result.keys())}
    return jsonify(mission)


if __name__ == '__main__':
    app.run(debug=True)
