1. Install virtualenv package to your system.
  sudo apt-get install python3-virtualenv
  pip3 install virtualenv --user

2. Create virtual environment.
  virtualenv "venv_name"
  python3 -m venv "venv_name"

3. Activate virtual environment
  . "venv_name"/bin/activate
  "venv_name"\scripts\activate - for Windows
  type "deactivate" to leave virtual environment

4. Install goose package.
  pip3 install --editable . (from root project folder)

5. Type goose --help to view all available commands
