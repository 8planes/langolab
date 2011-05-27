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

#!/user/bin/env python

import sys
import os
import subprocess
import logging

BASE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE, ".."))
from scriptlists import JS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

JS_LIB = os.path.join(BASE, "../media/js")
CLOSURE_DIR = os.path.join(JS_LIB, 'closure')

def compile(js_list, compiled_name):
    logging.info('starting compilation of {0}'.format(compiled_name))
    command = [os.path.join(CLOSURE_DIR, 'bin/calcdeps.py')]
    for f in js_list:
        command.extend(['-i', os.path.join(JS_LIB, f)])
    command.extend(
        ['-p', CLOSURE_DIR,
         '-o', 'compiled',
         '-c', 'compiler.jar',
         '-f', '--define=goog.DEBUG=false',
         '-f', '--output_wrapper=(function(){%output%})();',
         '-f', '--compilation_level=ADVANCED_OPTIMIZATIONS'])

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, err = process.communicate()
    logging.info(err)
    with open(os.path.join(JS_LIB, compiled_name), "w") as f:
        f.write(output)

compile(JS, 'llexchange-compiled.js')
