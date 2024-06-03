import argparse
import textwrap

import jupyter_client
from jupyter_client.manager import KernelManager

"""
Set this file as "interpreter options" in your "Run/Debug configurations"
template. This way, all your files you'll execute will be executed through
the jupyter kernel, running in IPyIDA.

To spawn a separate console to see the results, open cmd and run:

############################################################################################
python -m jupyter_console --existing --ZMQTerminalInteractiveShell.include_other_output=true
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
client = manager.client()
client.execute_interactive(f'%reset -f --aggressive', store_history=False)

# Check if we're calling the PyCharm debugger
if 'helpers/pydev/pydevd.py' in args.path:
    # Remove the pydev module vendored in debugpy because it clashes with the
    # one from PyCharm and hope it doesn't break anything
    # Otherwise, we get:
    # ModuleNotFoundError: No module named '_pydevd_bundle.pydevd_collect_try_except_info'
    remove_debugpy_pydevd = textwrap.dedent("""\
        import sys
        import os

        __blacklisted_path = f'{os.sep}debugpy{os.sep}_vendored{os.sep}'

        for name in sys.modules.copy():
            if 'pydev' in name and __blacklisted_path in getattr(sys.modules[name], '__file__', ''):
                del sys.modules[name]
        """)
    client.execute_interactive(remove_debugpy_pydevd, store_history=True, allow_stdin=True)

client.execute_interactive(command, store_history=True, allow_stdin=True)
