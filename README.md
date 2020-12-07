# Tickets and Games

* Heroku Link: https://tickets-and-games.herokuapp.com/
* To use this repository, please follow the following steps:

## Google OAuth Signup

1) Sign up https://console.developers.google.com/
2) Click create project
3) Click new project
4) Name the project whatever you would like
5) Choose "no organization"
6) Click credentials
7) Click create credentials
8) Click OAuth client ID
9) Click Configure consent screen
10) Choose external
11) For the application name secify something similar to the project name, click save
12) Back to credentials, create credentials, OAuth Client ID, click web application 

## Setting up Stripe

1) Sign up by going to https://dashboard.stripe.com/register
2) Go to API Keys page by clicking on developers link on the left and then API keys link
3) Copy the publishable key and secret key and put them in the .env file (or in your environment variable somehow)
4) Go to Webhooks page by clicking on the webhooks link on the left
5) Click on "Add endpoint" and provide a PUBLIC url/ip (not localhost)
6) Add "payment_intent.succeeded" event by clicking on the dropdown below "Events to send"
7) It will prompt you to enter your password and then redirect you to the webhook details page.
8) Copy the signing secret and put it in your environment variable


## Installation 

You have to install the npm dependencies and some python modules. Do so by running the following commands.

```bash
git clone https://github.com/CS490-section03-group0/project3
npm install
pip install  -r requirements.txt
```

## Running for development

First, create `.env` file with all the required environment variables.

Then you have to have the server running
```bash
python -m flask db upgrade
python app.py
```

Change the proxy port in packages.json to  the port you're using for the server.
Then,  in a separate shell, run the client
```bash
npm run start
```

Then, go to http://localhost:3000
All the api calls should be automatically proxied to the flask server.

## Running on production

If you, for whatever reason, want to run the server on production without something like heroku, you first have to build the client by
```bash
npm run build
```

and then start the server by
```bash
python app.py
```

The server will automatically serve the client files from the build directory.

## Deploying to Heroku

1) git push heroku master
2) Navigate to the link and view your site

## Work Breakdown for Milestone 1 

* Samir Peshori 
  * Responsible for creating front/backend & unit tests for Leaderboard & Coinflip Game
  * Added Material UI to components to style
* Mohammad Khan 
  * Google OAuth
  * Cirle Ci, Heroku, README
* David Kim
  * Set up the python and react project and maintained it
  * Set up the server sided OAuth to let users log in
  * Fixed various issues as they came up (Bug with leaderboard, default state of profile view, etc)
* Allen Kung
  * Set up tables for postgresql database
  * Profile view, transaction history
  * Sign up, login through username/password, hash and salt passwords
  * Unfinished work:
    - Testing sign up
    - Testing login through username/password
