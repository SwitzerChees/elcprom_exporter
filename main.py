from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Gauge
from flask import Flask, Response, request
from datetime import datetime
import yaml
import os
import re


def load_states(state_file='states.yml'):
    '''
    Load the states file with the configured states
    '''
    dir_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(dir_path, state_file)) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def inc_dec(state, val, data):
    '''
    Calculate incrementation of a state
    '''
    change = 0
    m = re.findall(str(state['inc_pattern']), val)
    if len(m) > 0:
        change += 1
    m = re.findall(str(state['dec_pattern']), val)
    if len(m) > 0:
        change -= 1
    if state.get('label_fields') is None:
        change_metric(change, state['type'], state['state'])
    else:
        label_values = [data[l] for l in state['label_fields']]
        change_metric(change, state['type'],
                      state['state'].labels(*label_values))
    return change != 0


def change_metric(change, type, metric):
    '''
    Change the metric depends on the type
    '''
    if type == 'binary':
        if change > 0:
            metric.set(1)
        elif change < 0:
            metric.set(0)
    else:
        if change > 0:
            metric.inc()
        elif change < 0:
            metric.dec()


def generate_prometheus_states():
    '''
    Create gauge metric for every configured state
    '''
    configured_states = load_states()
    for configured_state in configured_states:
        g = Gauge(
            configured_state['name'], configured_state['decription'], configured_state['label_fields'])
        configured_state['state'] = g
    return configured_states


def manipulate_state(data):
    '''
    Manipulate the states based on the matching patterns
    '''
    for state in configured_states:
        for key in data:
            if key in state['parse_fields']:
                if inc_dec(state, data[key], data):
                    break


# Define the endpoint for the state manipulation
app = Flask(__name__)
configured_states = generate_prometheus_states()


@app.route('/states', methods=['POST'])
def states():
    try:
        print(request.get_data())
        req_data = request.get_json(force=True)
        manipulate_state(req_data)
        return Response('Success!', 200)
    except Exception as err:
        now = datetime.utcnow()
        print(f'{now.strftime("%d.%m.%Y %H:%M:%S")}: ', err)
        return Response('Internal Error!', 500)


# Define the endpoint for the metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(debug=False, port=8080)
