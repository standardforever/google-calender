#!/usr/bin/env bash

# Define the desired Python version
PYTHON_VERSION="3.8.12"

# Install pyenv
curl https://pyenv.run | bash

# Set up pyenv in the current shell
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install the desired Python version
pyenv install "$PYTHON_VERSION"
pyenv global "$PYTHON_VERSION"

# Create and activate a virtual environment
# python -m venv venv
# source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

pip install --target . django
# Install the required dependencies
pip install -r requirements.txt
python -m pip install  --target . django
# Run the migrations
python manage.py migrate

# # Run the Django server
# python manage.py runserver
