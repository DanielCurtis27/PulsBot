to start the program, first run the following commands (assumes you already have python3 and pip installed):
python3 -m pip install -r install.txt
python3 -m pip install .\tensorflow-2.14.0-cp311-cp311-win_amd64.whl (if you are not running on windows, find the correct build for your system here: https://pypi.org/project/tensorflow/#files)
then start the program with the following:
python3 Main.py 'number of plots to search' 'username' 'password'