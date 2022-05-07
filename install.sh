#!/bin/bash

if [[ $(id -u) -ne 0 ]] ;
 then echo "Please run as root ( sudo )" ; exit 1 ; fi

echo - Creating virtual environment...
python3 -m venv venv
source venv/bin/activate
echo Done
echo

echo - Installing packages...
pip install -U pip -q
pip install -r requirements.txt -q
echo Done
echo

echo - Generating SECRET_KEY...
cd install || exit
python gen_sec_key.py
echo Done
echo

echo - Exiting install directory
cd ..
echo

echo - Loading fixtures...
./manage.py loaddata install/fixtures.json
echo Done
echo

while true; do
  read -rp "Create superuser? [y/n] : " superuser;
  if [ "$superuser" == "y" ]; then
    break
  elif [ "$superuser" == "n" ]; then
    break;
  fi;

done

echo

if [ "$superuser" == "y" ]; then
    echo - Creating superuser...
    ./manage.py createsuperuser
    echo Done
    echo
fi


echo - Clearing up...
rm -rf install/
rm -f install.sh
echo Done
echo
