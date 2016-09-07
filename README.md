# XQZES - XQZ Selection Engine

## About
I started xqzes as a side project to allow users on
slack to randomly insert excuses in to their chats.
It selects an excuse randomly from a backing database.
As a side-feature, it can present the same excuses in HTML.

## Usage
If you have a particular reason to host xqz.es yourself, you
are more than welcome to do so, by default, you can visit
[xqz.es](https://xqz.es/) in order to get excuses on the web
and to add to slack via the 'add to slack' button there.

## Contributing
Contributions are welcome as PR's, there is currently
no particular policy and will be dealt with on a case-by-case
basis. Generally good practice is recommended off of a recent
version of master.

## Self-Hosting / Development Setup
### Installation
In order to install all the pre-requisites for xqz.es you must run
`pip install -r requirements.txt` - you will likely have some other
OS dependencies if you don't do much python development. Off
the top of my head you will need the python development libraries
(`python3-dev`) and Postgres' `libpq`. If you'd like to use
MySQL or another database instead, you may have to install your own
python and system packages.

### Configuration
In order to be an open source project, xqz.es must not check in
secrets or API keys or assume things like emails or passwords,
which is why we configure a lot of the `settings.py` file with
environment variables. These are explained below:

| Env Var Name | Default Value | Value description |
| --- | --- | ------- |
|`XQZES_DATABASE_CONNECTION_STRING`|`sqlite:///excuses.sqlite`|local sqlite file called `excuses.sqlite`|SQLAlchemy connection url, see SQLAlchemy documentation [here](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)|
|`XQZES_BOTTLE_STATIC_PATH`|`./media`|Absolute path on system to your static/media files. I.e: full path to the `media` folder at this project's root.'|
|`XQZES_BOTTLE_TEMPLATE_PATH`|`./templates`|Absolute path on system to the `templates` folder.|
|`XQZES_ADMIN_EMAIL`|None|Gmail address used to send and receive application generated emails as well as the contact email|
|`XQZES_ADMIN_EMAIL_PASSWORD`|None|Password for that address (Use Gmail app-specific passwords)|
|`SLACK_VERIFICATION_TOKEN`|None|The token provided by slack that allows us to verify that it is indeed your Slack app making an API request.[1]|
|`XQZES_SLACK_OAUTH_CLIENT_ID`|None|Your applications OAuth client id, used for the Add to Slack button as well as the OAuth process.|
|`XQZES_SLACK_OAUTH_CLIENT_SECRET`|None|Your applications OAuth client secret, used for the OAuth process.|
|`XQZES_RECAPTCHA_SITE_KEY`|None|Site key to access google's Recaptcha API, used currently to protect the Contact Us form. Can be obtained [here](https://www.google.com/recaptcha/). Also see[2]|
|`XQZES_RECAPTCHA_SECRET_KEY`|None|Site key to access google's Recaptcha API, used currently to protect the Contact Us form. Obtained with Site key. Also see [2]|

### Initialization (one-time)
Once you have gathered all your environment variables and set up
your system
You need to initialize your selected database with some initial data
in order for xqz.es to work, you must do this from a python shell:
```
import admin
from server import Excuse

admin.initialize_database_for_model(Excuse)
admin.load_excuses()
```

### Running
Once you have been through all the prior steps, running
xqz.es is like running any other bottle app, in particular,
it should be as simple as `./server.py`.


# Footnotes
[1] - Slack sends this key with every API request they make in order for us to
 be able to verify that Slack is the sender of the request. Otherwise
 Anybody could make API calls to your API and trigger commands on behalf of
 other teams. Dangerous.

[2] - You may enter dummy data for development purposes, however, the
Contact Us page will fail to render a Captcha and will not be submittable.
