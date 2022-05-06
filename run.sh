#!/bin/bash

USAGE="[-u|--update] [-i|--initialize] [-r|--run]"

initialize_data() {
  cd initializing
  python3 init_data.py
  OK=$?
  rm tmp_data.csv > /dev/null
  cd ..
  if [ $OK ] ; then
    echo "Zainicjowano dane w bazie"
  else
    echo "Nieudana inicjalizacja"
  fi
}

install_dependencies() {
  pip -V > /dev/null
  if [ $? != 0 ] ; then 
    echo "Zainstaluj najpierw pip, np. z tego tutoriala:" ;
    echo "https://www.tecmint.com/install-pip-in-linux/" ;
    exit 1 ; 
  fi

  pip install --upgrade pip > /dev/null
  pip install --upgrade pandas > /dev/null
  pip install --upgrade numpy > /dev/null
  pip install --upgrade SQLAlchemy > /dev/null
  pip install --upgrade Flask > /dev/null
  pip install --upgrade Flask-Bootstrap > /dev/null
  echo "Zainstalowano wymagane biblioteki"
}

cd $(dirname $0)

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
