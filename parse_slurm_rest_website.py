import json
import re
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from datamodel_code_generator import InputFileType, generate
from pathlib import Path
from tempfile import TemporaryDirectory
import autopep8

VERSION = '37'
PARAM_NAME_PATTERN = re.compile(r'(?P<param_name>\S+)( \(optional\))?')

URL = "https://slurm.schedmd.com/rest_api.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

PREFIX = """from __future__ import annotations
from typing import *
from pydantic import BaseModel, Field
import requests


"""
ARRAY_PATTERN = re.compile(r'Array\[(?P<item_type>\S+)\]')

REQUIRED_PARAM = re.compile(r'((?P<param_name>\S+) ){1,2}\(required\)')
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


def _parse_name(name):
    if VERSION in name:
        name = name.split(f'{VERSION}_')[1]
    return name.title().replace('_', '').replace(']', '')


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


@dataclass
class Param:
    name: str
    optional: bool
    type: str
    description: str

    def _parse_type(self):
        if (match := re.match(ARRAY_PATTERN, self.type)):
            item_type = match.groupdict()['item_type']
            if not _check_known_type_and_convert(item_type):
                return {
                    'type': 'array',
                    'items': {
                        '$ref': f'#/definitions/{item_type}'
                    }
                }
            return {
                'type': 'array',
                'items': {
                    'type': _check_known_type_and_convert(item_type)
                }
            }
        elif converted_type := _check_known_type_and_convert(self.type):
            return {'type': converted_type}
        return {'$ref': f'#/definitions/{self.type}'}

    def to_json(self):
        return {
            'name': self.name,
            'property': {
                'description': self.description,
                'optional': self.optional,
                **self._parse_type()
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


def generate_models():
    raw_models = soup.find_all("div", class_="model")

    models = []
    for raw_model in raw_models:
        name = raw_model.find('h3').find('code').text
        name = _parse_name(name)
        
        params = raw_model.find_all('div', class_='param')
        params_desc = raw_model.find_all('div', class_='param-desc')

        model = Model(
            title=name,
            params=[],
            description=raw_model.find('div', class_='model-description').text,
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
        models.append(model)
    return models
        

slurm_rest_api_script = PREFIX

definitions = {}
models = generate_models()
for model in models:
    definitions[model.title] = model.to_json()
for model in models:
    if model.title in slurm_rest_api_script:
        continue

    auto_code = _generate_model(dict(**model.to_json(), definitions=definitions))
    auto_code = '\n'.join(filter(lambda line: not (line.startswith('#') or line.startswith('from')) and bool(line), auto_code.splitlines()))
    slurm_rest_api_script += f'{auto_code}\n\n\n'

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
            raise NotImplementedError()
        
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
    slurm_rest_api_script += func


with open('slurm_rest_api.py', 'w') as f:
    f.write(autopep8.fix_code(slurm_rest_api_script))