from utils import get_env_vars
import yaml
import json
import os


class Mapper:
    def __init__(self, env_vars, log) -> None:
        self.log = log
        self.mapping_file = env_vars['MAPPING_FILE']
        self.mapping_folder = env_vars['MAPPING_FOLDER']
        self.load()

    def load(self):
        '''
        Load the mapping files with the mappings
        '''
        self.mapping_files = []
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(dir_path, self.mapping_file)) as file:
            self.mappings = yaml.load(file, Loader=yaml.FullLoader)
        if self.mapping_folder[0] != '/':
            self.mapping_folder = os.path.join(dir_path, self.mapping_folder)
        if os.path.exists(self.mapping_folder):
            for mapping_file in os.listdir(self.mapping_folder):
                with open(os.path.join(self.mapping_folder, mapping_file)) as file:
                    self.mapping_files.append(
                        {"file": mapping_file, "content": json.load(file)})

    def apply_mapping(self, data):
        '''
        Extend the object depends on the configured mappings
        '''
        for mapping in self.mappings:
            if(all(k in data != None for k in mapping['from'])):
                mapping_file = next(
                    x for x in self.mapping_files if x['file'] == mapping['file'])
                if mapping_file is None:
                    self.log.info(f"Mapping file: '{mapping['file']}' not found")
                    continue
                mapping_found = False
                for map_item in mapping_file['content']:
                    if(all(data[k] == map_item[k] for k in mapping['from'])):
                        data[mapping['to']] = map_item[mapping['to']]
                        self.log.info(f"Mapping, {mapping}, Map_item: {map_item}")
                        mapping_found = True
                        break
                if not mapping_found:
                    self.log.info(f"No mapping found for Mapping: {mapping}")
                    data[mapping['to']] = 'NO_MAPPING_FOUND'
