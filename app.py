from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """Render the room page with unique room ID"""
    return render_template('room.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    """User joins a room"""
    username = data.get('username', 'User')
    room = data.get('room', 'default')
    join_room(room)
    print(f'{username} joined room {room}')
    emit('user_joined', {'username': username}, to=room)

@socketio.on('offer')
def handle_offer(data):
    """Forward WebRTC offer to the other peer"""
    print(f"Forwarding offer to room: {data['room']}")
    emit('offer', data, to=data['room'], include_self=False)

@socketio.on('answer')
def handle_answer(data):
    """Forward WebRTC answer to the other peer"""
    print(f"Forwarding answer to room: {data['room']}")
    emit('answer', data, to=data['room'], include_self=False)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    """Forward ICE candidate to the other peer"""
    print(f"Forwarding ICE candidate to room: {data['room']}")
    emit('ice_candidate', data, to=data['room'], include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5003)