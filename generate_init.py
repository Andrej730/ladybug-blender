import os
import json
import pystache
import subprocess
from pathlib import Path
from typing import Any

class Generator():
    def __init__(self):
        self.json_dir = './dist/working/json/'
        self.out_dir = './dist/working/python/'

    @staticmethod
    def spec_process_nickname(spec: dict[str, Any]) -> None:
        nickname = spec["nickname"]
        nickname = nickname.replace("+", "Plus")
        nickname = nickname.replace(" ", "_")
        spec["nickname"] = nickname

    def generate(self):
        data = {
            'nodes': [],
        }
        for filename in Path(self.json_dir).glob('*.json'):
            if 'LB_Export_UserObject' in str(filename) \
                    or 'LB_Sync_Grasshopper_File' in str(filename) \
                    or 'LB_Versioner' in str(filename):
                continue # I think these nodes are just for Grasshopper
            with open(filename, 'r') as spec_f:
                spec = json.load(spec_f)
                Generator.spec_process_nickname(spec)
                filename = os.path.basename(filename)
                subcategory = spec['subcategory'].split(' :: ')[1]
                data['nodes'].append({
                    'node_module': filename[0:-5],
                    'node_classname': spec['nickname'],
                    'subcategory': subcategory
                })

        out_filepath = os.path.join(self.out_dir, '__init__.py')
        with open(out_filepath, 'w') as f:
            with open('init.mustache', 'r') as template:
                f.write(pystache.render(template.read(), data))

generator = Generator()
generator.generate()
