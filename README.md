# XQZES - XQZ Selection Engine

## About
I started xqzes as a side project to allow users on
slack to randomly insert excuses in to their chats.
It selects an excuse randomly from a backing database.
As a side-feature, it can present the same excuses in HTML.

Slack support was retired when when slack required API
changes and procedural hoops that I did not feel
like going through.

## Usage
If you have a particular reason to host xqz.es yourself, you
are more than welcome to do so, by default, you can visit
[xqz.es](https://xqz.es/) in order to get excuses on the web.

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

#### Note

There are a few small tweaks I've made that don't necessarily generalize,
these can be found on the `deploy` branch mostly.

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
[1] - You may enter dummy data for development purposes, however, the
Contact Us page will fail to render a Captcha and will not be submittable.
