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

## Self-hosting
xqz.es is a bottle app that you can run with ./server.py,
it expects to be run in a python3 environment, there are
certain env vars that need to be configured for
successful usage, these can be found in `settings.py`

## Contributing
Contributions are welcome as PR's, there is currently
no particular policy and will be dealt with on a case-by-case
basis. Generally good practice is recommended off of a recent
version of master.
