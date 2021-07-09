import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


def get_env_vars():
    env_vars = {}
    env_vars['MAPPING_FILE'] = make_abs_rel(
        os.getenv('MAPPING_FILE', "mappings.yml"))
    env_vars['MAPPING_FOLDER'] = make_abs_rel(
        os.getenv('MAPPING_FOLDER', "mappings"))
    env_vars['OUTPUT_FILE'] = make_abs_rel(os.getenv('OUTPUT_FILE', ''))
    env_vars['STATE_FILE'] = make_abs_rel(
        os.getenv('STATE_FILE', "states.yml"))
    env_vars['CURRENT_STATE_FILE'] = make_abs_rel(
        os.getenv('CURRENT_STATE_FILE', "current_states.json"))
    env_vars['SCHEDULE_INTERVAL'] = os.getenv('SCHEDULE_INTERVAL', "1m")
    return env_vars


def make_abs_rel(path):
    if path is not None and path != '' and path[0] != '/':
        path = os.path.join(DIR_PATH, path)
    return path
