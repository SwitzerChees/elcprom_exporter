from prometheus_client import Gauge
from utils import get_env_vars
import yaml
import json
import os
import re


class State:
    def __init__(self) -> None:
        env_vars = get_env_vars()
        self.state_file = env_vars['STATE_FILE']
        self.current_state_file = env_vars['CURRENT_STATE_FILE']
        self.load()
        self.generate_prometheus_states()
        self.update_states()

    def load(self):
        '''
        Load the states files with the states
        '''
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(dir_path, self.state_file)) as file:
            self.state = yaml.load(file, Loader=yaml.FullLoader)
        if os.path.exists(self.current_state_file):
            with open(os.path.join(dir_path, self.current_state_file)) as file:
                self.current_state = json.load(file)
        else:
            self.current_state = []

    def persist(self):
        with open(self.current_state_file, 'w') as outfile:
            json.dump(self.current_state, outfile, indent=4)

    def generate_prometheus_states(self):
        for configured_state in self.state:
            g = Gauge(
                configured_state['name'], configured_state['decription'], configured_state['label_fields'])
            configured_state['state'] = g

    def check_inc_dec(self, data):
        '''
        Manipulate the states based on the matching patterns
        '''
        for configured_state in self.state:
            for key in data:
                if key in configured_state['parse_fields']:
                    if self.inc_dec(configured_state, data[key], data):
                        break

    def inc_dec(self, state, val, data):
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
        if change != 0:
            label_values = []
            if state.get('label_fields') is not None:
                for label in state['label_fields']:
                    if label in data:
                        label_values.append(data[label])
                    else:
                        label_values.append('MISSING_LABEL')
            self.change_state(
                change, state, label_values)
            self.update_states()
            return True
        return False

    def change_state(self, change, state, label_values):
        '''
        Change the metric depends on the type
        '''
        type = state['type']
        state_name = state['name']
        remove_on_zero = state.get('remove_on_zero') if state.get('remove_on_zero') is not None else False
        found_state = [s for s in self.current_state if s['state_name']
                       == state_name and s['labels'] == label_values]
        if len(found_state) == 0:
            found_state = {
                "state_name": state_name, "labels": label_values, "value": 0}
            self.current_state.append(found_state)
        else:
            found_state = found_state[0]
        if type == 'binary':
            if change > 0:
                found_state['value'] = 1
            elif change < 0:
                if remove_on_zero:
                    self.current_state.remove(found_state)
                    state['state'].remove(*found_state['labels'])
                else:
                    found_state['value'] = 0
        else:
            if change > 0:
                found_state['value'] += 1
            elif change < 0:
                found_state['value'] -= 1
        self.persist()

    def update_states(self):
        for curr_state in self.current_state:
            for state in self.state:
                if state['name'] == curr_state['state_name']:
                    metric = state['state'].labels(*curr_state['labels'])
                    metric.set(curr_state['value'])
