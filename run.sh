#!/bin/bash

USAGE="[-u|--update] [-i|--initialize] [-r|--run]"

initialize_data() {
  cd initializing
  python3 init_data.py
  rm tmp_data.csv
  cd ..
}

install_dependencies() {
  pip -V
  if [$? != 0] ; then 
    echo "Zainstaluj najpierw pip, np. z tego tutoriala:" ;
    echo "https://www.tecmint.com/install-pip-in-linux/" ;
    exit 1 ; 
  fi

  pip install --upgrade pip
  pip install --upgrade pandas
  pip install --upgrade numpy
  pip install --upgrade SQLAlchemy
  pip install --upgrade Flask
  pip install --upgrade Flask-Bootstrap
}

ARGS=$(getopt -o uir --long update,initialize,run -- "$@" 2> /dev/null)
if [ $? != 0 ] ; then echo "Użycie:" $0 $USAGE ; exit 1 ; fi

eval set -- "$ARGS"

[ $# != 1 ] ; RUN=$?

while true; do
  case "$1" in 
    -u | --update ) 
      install_dependencies
      shift ;;
    -i | --initialize ) 
      initialize_data
      shift ;;
    -r | --run ) 
      RUN=1
      shift ;;
    -- )
      break ;;
  esac
done

if [ $RUN == 1 ] ; then
  FLASK_APP=main.py FLASK_DEBUG=1 flask run 
  echo ""
fi
