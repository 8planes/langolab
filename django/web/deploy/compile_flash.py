"""
Langolab -- learn foreign languages by speaking with random native speakers over webcam.
Copyright (C) 2011 Adam Duston

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, os, re
import getopt
from os.path import join

DEPLOY_ROOT = os.path.abspath(os.path.dirname(__file__))

def rel(*x):
    return join(DEPLOY_ROOT, *x)

FLASH_ROOT = rel('..', '..', 'flash')
SWF_DIR = rel('..', 'media', 'swf')

def run(cmd):
    for line in os.popen(cmd).readlines():
        print(line)

def compile(mxml_path, output_name):
    command = 'mxmlc --output={0} -debug=true -target-player=10.0.0 -library-path+={1} {2}'.format(
        join(SWF_DIR, output_name), 
        join(FLASH_ROOT, 'lib', 'Stomp_06.swc'),
        mxml_path)
    print('running ' + command)
    run(command)

compile(join(FLASH_ROOT, 'src', 'llexchange.mxml'), 'llexchange.swf')
