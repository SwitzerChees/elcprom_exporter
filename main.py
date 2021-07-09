from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, Response, request, jsonify
from prometheus_client import make_wsgi_app
from utils import get_env_vars
from pytimeparse import parse
from logger import Logger
from mapper import Mapper
from state import State
from time import sleep
from datetime import datetime
import traceback
import threading

env_vars = get_env_vars()

log = Logger(env_vars)
st = State(env_vars)
ma = Mapper(env_vars, log)

# Define the endpoint for the state manipulation
app = Flask(__name__)


@app.route('/states', methods=['POST'])
def states():
    try:
        log.info(request.get_data())
        req_data = request.get_json(force=True)
        ma.apply_mapping(req_data)
        st.check_inc_dec(req_data)
        return jsonify(st.current_state)
    except Exception as err:
        now = datetime.utcnow()
        formated_error = ''.join(traceback.format_exception(
            etype=type(err), value=err, tb=err.__traceback__))
        log.error(formated_error)
        return Response(formated_error, 500)


# Define the endpoint for the metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


def update_state_schedule():
    while True:
        sleep(parse(env_vars['SCHEDULE_INTERVAL']))
        st.update_states()


if __name__ == '__main__':
    threading.Thread(target=update_state_schedule).start()
    app.run(debug=False, port=8080)
