# IDAPython-pycharm-setup
How to setup Pycharm to run scripts in IDA using the Run menu (or a keybind)

This is just a placeholder Readme. FIXME: Improve me

## Running your code directly from PyCharm

Note: you need to install and configure [IPyIDA](https://github.com/eset/ipyida) first.

TL;DR: Set the pycharm_wrapper.py file as as Run/Debug Configuration template
using the appropriate options and then just use Shift+F10 to (re-)run your
python script in IDA while seeing the output in a separate terminal.

![](template.png)

## Configuring autocompletion

Open the settings window, navigate to your interpreter and add IDAPython
directory to the interpreter paths

![](paths.png)

Autocompletion and docstrings in PyCharm should now be working!

![](autocompletion.png)

![](docstring.png)
