# wildfire_tracker

## Installation
Create a copy of this repo to your GitHub account, then clone or download the new repo onto your local computer (for example, in GitHub Desktop), and navigate there from the command-line:

```sh
cd desktop/GitHub/wildfire_tracker
# the path may be different depending on where you saved the repo locally
```

Use Anaconda to create and activate a new virtual environment, perhaps called "wildfire-env":

```sh
conda create -n wildfire-env python=3.8
conda activate wildfire-env
```

Then, within an active virtual environment, install package dependencies (included in the requirements.txt file):

```sh
pip install -r requirements.txt
```

## Usage Locally
From the command line, run the app. If installation worked, this should prompt a new browser to open and display a map of the wildfires.

```sh
python -m wildfire_map
```

## Running the web app
Use the following from the command line to run the web app.

For windows users:

```sh
export FLASK_APP=web_app
flask run
```

For MAC users:

```sh
FLASK_APP=web_app flask run
```