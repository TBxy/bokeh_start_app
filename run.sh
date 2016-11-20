#!/bin/sh
usage="% $(basename "$0")(1)
% Tobias Burgherr
% November 2016

\`$(basename "$0") [-h] [-d db cmd] [-f flask cmd] \`

Runs the webserver

**where:**

*  -h  show this help text
*  -d  flask db commands
    *  init
    *  migrate
    *  update
*  -f  flask command (eg. --help)
*  -r  install requirements
    "

# Variable
DB_CMD=""
FLASK_CMD=""
INSTALL_REQ=0
ROTATE=0
# Files

# Options
while getopts ':d:f:rhHc:r' option; do
  case "$option" in
    d) DB_CMD=$OPTARG
       ;;
    f) FLASK_CMD=$OPTARG
       ;;
    r) INSTALL_REQ=1
       ;;
    h) echo "$usage" | pandoc -f markdown -s -t man  | man -l -
       exit
       ;;
    H) echo "$usage"
       exit
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

# First set coorect settings variable
if [ -z "$BOKEH_START_APP_SECRET" ]; then
    echo "Add the env variable BOKEH_START_APP_SECRET!"
    export BOKEH_START_APP_SECRET='secret'
fi
MAIN_DIR=`dirname $0`
echo "Main directory: $MAIN_DIR"
cd $MAIN_DIR

export FLASK_APP=autoapp.py
export FLASK_DEBUG=1

if [ ! -d venv ]; then
    echo "Create virtual environment 'venv'"
    virtualenv venv
fi

echo "Activate virtual environment 'venv'"
. venv/bin/activate

if [ $INSTALL_REQ -gt 0 ]; then
    echo "Install requirements."
    pip install -r requirements/dev.txt
fi

if [ ! $DB_CMD = "" ]; then
    echo "Run: flask db $DB_CMD"
    flask db $DB_CMD
    exit
fi

if [ ! $FLASK_CMD = "" ]; then
    echo "Run: flask db $FLASK_CMD"
    flask $FLASK_CMD
    exit
fi

echo "Run: flask run"
flask run

