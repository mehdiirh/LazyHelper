#!/bin/bash

if [[ $(id -u) -ne 0 ]] ;
 then echo "Please run as root ( sudo )" ; exit 1 ; fi

echo - Creating virtual environment...
python3 -m venv venv
source venv/bin/activate
echo Done
echo

echo - Installing packages...
pip install -U pip
pip install -r requirements.txt
echo Done
echo

echo - Creating migrations and loading static files...
./manage.py makemigrations
echo Done
echo

echo - Running tests...
if ./manage.py test --failfast; then
  echo Done;
  echo;
else
  echo;
  echo -e "\e[31mSome tests failed, please fix the problem and retry\e[0m";
  exit 0;
fi

echo - Generating SECRET_KEY...
cd install || exit
python gen_sec_key.py
echo Done
echo

echo - Exiting install directory
cd ..
echo

echo - Migrate database and loading static files...
./manage.py migrate
./manage.py collectstatic --noinput
echo Done
echo

echo - Loading fixtures...
./manage.py loaddata install/fixtures.json

while true; do
  read -rp "Load commands fixtures? ( pre-defined commands ) [y/n] : " fixtures;
  if [ "$fixtures" == "y" ]; then
    ./manage.py loaddata install/linux_commands.json
    break;
  elif [ "$fixtures" == "n" ]; then
    break;
  fi;
done

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
