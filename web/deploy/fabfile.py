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

from fabric.api import run, put, sudo, env, cd, local
import os

env.hosts = ['8planes.com']
env.user = 'llexchange'
env.base_dir = '/home/{0}'.format(env.user)

def _command(cmd):
    def f(arg):
        run("%s %s" % (cmd, arg))
    return f

def update_swf():
    with cd('{0}/llexchange/web/deploy'.format(env.base_dir)):
        run('git pull')
        run('{0}/env/bin/python compile_flash.py'.format(env.base_dir))
        run('touch {0}.wsgi'.format(env.user))

def update_js():
    with cd('{0}/llexchange/web/deploy'.format(env.base_dir)):
        run('git pull')
        run('{0}/env/bin/python compile_closure.py'.format(env.base_dir))
        run('touch {0}.wsgi'.format(env.user))

def sudo():
    env.user = 'ubuntu'

def bounce():
    # to be used like "fab sudo bounce"
    sudo('/etc/init.d/apache restart')

def update_web():
    with cd('{0}/llexchange/web'.format(env.base_dir)):
        run('git pull')
        env.warn_only = True
        run("find . -name '*.pyc' -print0 | xargs -0 rm")
        env.warn_only = False
        run('touch deploy/{0}.wsgi'.format(env.user))

def update():
    update_web()
    update_swf()
    update_js()

def syncdb(app_name=''):
    with cd('{0}/llexchange/web'.format(env.base_dir)):
        run('{0}/env/bin/python manage.py syncdb {1} --settings=llexchange-settings'.format(env.base_dir, app_name))

def run_command(command):
    with cd('{0}/llexchange/web'.format(env.base_dir)):
        run('{0}/env/bin/python manage.py {1} --settings=llexchange-settings'.format(env.base_dir, command))

def migrate_fake(app_name):
    """Unfortunately, one must do this when moving an app to South for the first time.

    See http://south.aeracode.org/docs/convertinganapp.html and
    http://south.aeracode.org/ticket/430 for more details. Perhaps this will be changed 
    in a subsequent version, but now we're stuck with this solution.
    """
    with cd('{0}/llexchange/web'.format(env.base_dir)):
        run('yes no | {0}/env/bin/python manage.py migrate {1} 0001 --fake --settings=llexchange-settings'.format(env.base_dir, app_name))

def migrate(app_name=''):
    with cd('{0}/llexchange/web'.format(env.base_dir)):
        run('yes no | {0}/env/bin/python manage.py migrate {1} --settings=llexchange-settings'.format(env.base_dir, app_name))
