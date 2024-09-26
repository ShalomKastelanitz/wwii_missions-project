from flask import Flask, jsonify
from models import db, Mission
from config import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
#שליפה של כל המשימות
@app.route('/api/mission', methods=['GET'])
def get_missions():
    missions = Mission.query.limit(100).all()
    missions_list = [
        {
            'mission_id': mission.mission_id,
            'mission_date': mission.mission_date,
            'mission_type': mission.mission_type,
            'target_country': mission.target_country
        }
        for mission in missions
    ]
    return jsonify(missions_list)

#שליפה לפי id
@app.route('/api/mission/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    mission = Mission.query.get(mission_id)

    if mission is None:
        return jsonify({'error': 'Mission not found'}), 404

    mission_data = {
        'mission_id': mission.mission_id,
        'mission_date': mission.mission_date,
        'mission_type': mission.mission_type,
        'target_country': mission.target_country
    }
    return jsonify(mission_data)


if __name__ == '__main__':
    app.run(debug=True)
