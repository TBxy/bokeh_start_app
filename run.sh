#!/bin/sh
usage="% $(basename "$0")(1)
% Tobias Burgherr
% November 2016

\`$(basename "$0") [-h] [-d db cmd] [-f flask cmd] \`

Runs the web server.
By default it activates the virtual environment and starts the server:
>>> . venv/bin/activate
>>> flask run

Where:

  -h  show this help text
  -i  initiate application (-r, db init, migrate, upgrade, insertdb)
  -d  flask db commands
      ~ init
      ~ migrate
      ~ upgrade
  -f  flask command (see --help)
  -r  install requirements


Initialization:

The first time you should run run.sh -i, this installs all requirements and 
generates the database.
By default two users are created, admin and guest. The passwords are the usernames.
It is highly recommend to change them (with the admin user).
    "

# Variable
DB_CMD=""
FLASK_CMD=""
INSTALL_REQ=0
INIT=0
# Files

# Options
while getopts ':d:f:rhHi' option; do
  case "$option" in
    d) DB_CMD=$OPTARG
       ;;
    f) FLASK_CMD=$OPTARG
       ;;
    r) INSTALL_REQ=1
       ;;
    #h) echo "$usage" | pandoc -f markdown -s -t man  | man -l -
    h) echo "$usage"
       exit
       ;;
    H) echo "$usage"
       exit
       ;;
    i) INSTALL_REQ=1
       INIT=1
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done
shift $((OPTIND - 1))


echo

# First set correct settings variable
if [ -z "$BOKEH_START_APP_SECRET" ]; then
    echo "Add the env variable BOKEH_START_APP_SECRET!"
    export BOKEH_START_APP_SECRET='secret'
fi
MAIN_DIR=`dirname $0`
echo "Main directory: $MAIN_DIR"
cd $MAIN_DIR

export FLASK_APP=autoapp.py
export FLASK_DEBUG=1
export BOKEH_SECRET_KEY=$(date +%s | sha256sum | base64 | head -c 32 ; echo)
#export BOKEH_SIGN_SESSIONS=true

export BOKEH_MINIFIED=true
export BOKEH_RESOURCES=server

if [ ! -d venv ]; then
    echo "Create virtual environment 'venv'"
    virtualenv venv
fi

echo "Activate virtual environment 'venv'"
. venv/bin/activate

if [ $INSTALL_REQ -gt 0 ]; then
    echo "Install requirements (python)."
    pip install -r requirements/dev.txt
    echo "Install requirements (javascript)."
    bower install
    
    echo "copy bokeh js and css files to static folder"

    cp venv/lib/python2.7/site-packages/bokeh/server/static/css/* app/static/css/
    cp venv/lib/python2.7/site-packages/bokeh/server/static/js/* app/static/js/

    echo "copy fonts to static folder"
    mkdir -p app/static/fonts/roboto/
    cp -R -u  app/static/libs/materialize/fonts/roboto/ app/static/fonts/
fi

if [ ! $DB_CMD = "" ]; then
    echo "Run: flask db $DB_CMD"
    flask db $DB_CMD
    exit
fi

if [ ! $FLASK_CMD = "" ]; then
    echo "Run: flask $FLASK_CMD"
    flask $FLASK_CMD
    exit
fi

if [ $INIT -gt 0 ]; then
    echo "Run: flask db init"
    flask db init
    echo "Run: flask db migrate"
    flask db migrate
    echo "Run: flask db upgrade"
    flask db upgrade
    echo "Run: flask insertdb"
    flask insertdb
fi

# run after ^C -> save this command for as exit cmd
trap "echo \"\nShuting down, deactivate 'venv'.\n\n\"; deactivate; pkill bokeh" INT

echo "Start bokeh server"
echo "Run: bokeh serve --allow-websocket-origin=*:5000 ./app/bokeh_apps/* &"
# --session-ids=external-signed    # does not work yet
bokeh serve --allow-websocket-origin=*:5000  ./app/bokeh_apps/* &

echo "Run: flask run"
if [ $INIT -gt 0 ]; then
    echo "     You can login with admin:admin or guets:guest."
fi
flask run
