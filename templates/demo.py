from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
mentors = [
    {'id': 1, 'name': 'John Doe', 'expertise': 'Data Science'},
    {'id': 2, 'name': 'Jane Smith', 'expertise': 'Web Development'}
]

# Home route
@app.route('/')
def home():
    return "Welcome to the Mentorship API"

# Get all mentors
@app.route('/api/mentors', methods=['GET'])
def get_mentors():
    return jsonify(mentors)

# Get mentor by ID
@app.route('/api/mentors/<int:id>', methods=['GET'])
def get_mentor(id):
    mentor = next((mentor for mentor in mentors if mentor['id'] == id), None)
    if mentor is None:
        return jsonify({'message': 'Mentor not found'}), 404
    return jsonify(mentor)

# Add a new mentor
@app.route('/api/mentors', methods=['POST'])
def add_mentor():
    new_mentor = request.json
    mentors.append(new_mentor)
    return jsonify(new_mentor), 201

# Update a mentor
@app.route('/api/mentors/<int:id>', methods=['PUT'])
def update_mentor(id):
    mentor = next((mentor for mentor in mentors if mentor['id'] == id), None)
    if mentor is None:
        return jsonify({'message': 'Mentor not found'}), 404
    
    updated_data = request.json
    mentor.update(updated_data)
    return jsonify(mentor)

# Delete a mentor
@app.route('/api/mentors/<int:id>', methods=['DELETE'])
def delete_mentor(id):
    global mentors
    mentors = [mentor for mentor in mentors if mentor['id'] != id]
    return jsonify({'message': 'Mentor deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
