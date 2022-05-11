import json
import re
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from datamodel_code_generator import InputFileType, generate
from pathlib import Path
from tempfile import TemporaryDirectory

VERSION = ('v0.0.37_', 'v0_0_37_', 'dbv0.0.37_')
PARAM_NAME_PATTERN = re.compile(r'(?P<param_name>\S+)( \(optional\))?')

URL = "https://slurm.schedmd.com/rest_api.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

def _parse_name(name):
    for v in VERSION:
        name = name.replace(v, '')
    return name.title().replace('_', '')

PREFIX = """from __future__ import annotations
from typing import *
from pydantic import BaseModel, Field
import requests


"""

REQUIRED_PARAM = re.compile(r'(?P<param_name>\S+) \(required\)')
OPTIONAL_PARAM = re.compile(r'(?P<param_name>\S+) \(optional\)')

FUNCTION_PARAM_TEMPLATE = ':param {param_name}: {param_doc}'
REQUEST_TEMPLATE = """
def {method_name}({parameters}) -> {return_type}:
    \"\"\"
    {method_doc}

    {params_doc}
    \"\"\"
    return requests.{http_method}('{url}')

"""
DEFINITIONS = {}

def _check_known_type_and_convert(type_):
    TYPE_CONVERTIONS = {
        'bigdecimal': 'integer',
        'long': 'integer',
        'double': 'number',
    }
    type_ = type_.lower()
    type_ = TYPE_CONVERTIONS.get(type_, type_)
    if type_.lower() in ('string', 'integer', 'boolean', 'object', 'number',):
        return type_
    return None

BLA = None
@dataclass
class Param:
    name: str
    optional: bool
    type: str
    description: str

    def _parse_type(self):
        ARRAY_PATTERN = re.compile(r'Array\[(?P<item_type>\S+)\]')
        if (match := re.match(ARRAY_PATTERN, self.type)):
            item_type = match.groupdict()['item_type']
            print(item_type)
            if item_type.lower() == 'string':
                global BLA
                BLA = self.name
            return 'array'

        if type_ := _check_known_type_and_convert(self.type):
            return type_
        
        DEFINITIONS[self.type] = {
            'properties': {
                'name': {
                    'type': 'string'
                }
            }
        }
        
        # print(self.type)
        # print(DEFINITIONS.keys())
        return 'object'

        return {'$ref': f'#/definitions/{self.type}'}
            
    def to_json(self):
        return {
            'name': self.name,
            'property': {
                'type': self._parse_type(),
                'description': self.description,
                'optional': self.optional,
            }
        }


@dataclass
class Model:
    title: str
    params: list[Param]
    description: str

    def to_json(self):
        return {
            'title': self.title,
            'type': 'object',
            'properties': {param.to_json()['name']: param.to_json()['property'] for param in self.params},
            # 'definitions': DEFINITIONS
        }


def _generate_model(json_schema):
    with TemporaryDirectory() as temporary_directory_name:
        temporary_directory = Path(temporary_directory_name)
        output = Path(temporary_directory / 'model.py')
        generate(
            json.dumps(json_schema),
            input_file_type=InputFileType.JsonSchema,
            input_filename="example.json",
            output=output,
            
        )
        model: str = output.read_text()
        return model

with open('slurm_rest_api.py', 'w') as slurm_rest_api_script:
    slurm_rest_api_script.write(PREFIX)

    models = soup.find_all("div", class_="model")
    for model in models:
        name = model.find('h3').find('code').text
        name = _parse_name(name)
        
        params = model.find_all('div', class_='param')
        params_desc = model.find_all('div', class_='param-desc')

        model = Model(
            title=name,
            params=[],
            description=model.find('div', class_='model-description').text,
        )
        for param, desc in zip(params, params_desc):
            param_type = desc.find('span', class_='param-type').text
            p = Param(
                name=re.match(PARAM_NAME_PATTERN, param.text).groupdict()['param_name'],
                optional='optional' in param.text,
                type=_parse_name(param_type),
                description=desc.text.replace(param_type, '').strip()
            )
            model.params.append(p)

        auto_code = _generate_model(model.to_json())
        auto_code = '\n'.join(filter(lambda line: not (line.startswith('#') or line.startswith('from')) and bool(line), auto_code.splitlines()))
        slurm_rest_api_script.write(f'{auto_code}\n\n\n')

        if BLA:
            import sys
            sys.exit(0)

    methods = soup.find_all("div", class_="method")
    for method in methods:
        method_name = method.find('span', class_='nickname').text
        http_method = method.find('span', class_="http-method").text
        url = method.find('code', class_="huge").text.replace(http_method, '').strip()
        method_doc = method.find('div', class_='method-summary').text
        
        if text := method.find('div', class_='return-type'):
            return_type = text.text.strip()
        else:
            return_type = 'None'
        return_type = _parse_name(return_type)

        parameters = {}
        for param in method.find_all('div', class_='field-items'):
            param_name = param.find('div', class_='param').text
            if match := re.match(REQUIRED_PARAM, param_name):
                key = match.groups()[0]
            elif match := re.match(OPTIONAL_PARAM, param_name):
                key = f'{match.groups()[0]}=None'
            else:
                print(param_name)

            parameters[
                key
            ] = param.find('div', class_='param-desc').text

        func = REQUEST_TEMPLATE.format(
            method_name=method_name,
            http_method=http_method,
            parameters=', '.join([param for param in parameters]),
            url=url,
            method_doc=method_doc,
            params_doc='\n'.join([FUNCTION_PARAM_TEMPLATE.format(param_name=param_name, param_doc=param_doc) for param_name, param_doc in parameters.items()]),
            return_type=return_type
        )
        slurm_rest_api_script.write(func)
