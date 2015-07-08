"""
Writes highlighted sources to ./highlighted for use in Keynote
"""

from glob import glob
import shutil
import os

import pygments
from pygments.lexers import PythonLexer, YamlLexer
from pygments.formatters import RtfFormatter

service_dir = './services'
config_dir = './conf'
highlight_dir = './highlighted'


def highlight_all():
    force_mkdir(highlight_dir)
    for path in get_files():
        highlight_file(path)


def force_mkdir(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        pass
    os.mkdir(path)


def get_files():
    return glob(service_dir + '/*.py') + glob(config_dir + '/*.yml')


def highlight_file(path):
    content = highlight(path)
    highlight_filename = os.path.join(highlight_dir, os.path.basename(path))
    with open(highlight_filename, 'w') as output_file:
        output_file.write(content)


def highlight(path):
    lexer = get_lexer(path)
    formatter = RtfFormatter()
    with open(path, 'r') as code:
        return pygments.highlight(code.read(), lexer, formatter)


def get_lexer(path):
    if path.endswith('.py'):
        return PythonLexer()
    elif path.endswith('.yml'):
        return YamlLexer()


if __name__ == '__main__':
    highlight_all()
