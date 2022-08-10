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

## .env setup
In a .env file, you should add environment variables for the following:

```sh
api_key = "input your NASA api key here"
```

```sh
SENDGRID_API_KEY="input your sendgrid api key here"
```

```sh
SENDER_ADDRESS="input your sendgrid email here:
```

## Usage
From the command line, run the app. If installation worked, this should prompt a new browser to open and display a map of the wildfires. Sendgrid should also send an email with an image of the map attached.

```sh
python -m wildfire_map
```

## Heroku Scheduler
Source: https://github.com/csthomas1029/daily-briefings/blob/main/DEPLOYING.md
Follow these instructions to schedule the email to send automatically at a specified interval.
The server configuration variables should follow the .env setup above.
You will input the same python command as you use in the command line to run the app.