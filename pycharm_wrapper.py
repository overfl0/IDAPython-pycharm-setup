import argparse

import jupyter_client
from jupyter_client.manager import KernelManager

"""
Set this file as "interpreter options" in your "Run/Debug configurations"
template. This way, all your files you'll execute will be executed through
the jupyter kernel, running in IPyIDA.

To spawn a separate console to see the results, open cmd and run:

############################################################################################
python -m IPython console --existing --ZMQTerminalInteractiveShell.include_other_output=true
############################################################################################
"""

parser = argparse.ArgumentParser(description='Execute a file inside a running ipython kernel')
parser.add_argument('path', type=str, help='path to the file being executed')
parser.add_argument('rest', nargs=argparse.REMAINDER)

args = parser.parse_args()


def escape_string(txt):
    """Poor man's escaping"""
    return txt.replace('\\', '\\\\').replace('"', '\\"')


command = f'%run -G -e "{escape_string(args.path)}" ' + ' '.join(args.rest)
print(f'Connecting to ipython\'s kernel and executing {command}...')

connection_file = jupyter_client.connect.find_connection_file()
manager = KernelManager(connection_file=connection_file)
manager.load_connection_file()
manager.client().execute(f'%reset -f --aggressive', store_history=False)
manager.client().execute(command, store_history=True, allow_stdin=True, reply=True)
