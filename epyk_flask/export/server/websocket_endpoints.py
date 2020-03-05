from flask import request, Blueprint

ws = Blueprint('ws', __name__)

@ws.route('/ws')
def basic_ws():
  if request.environ.get('wsgi.websocket'):
    ws = request.environ['wsgi.websocket']
    while True:
      message = ws.receive()
      ws.send(message)
  return