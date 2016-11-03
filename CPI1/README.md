Command line instructions

Git global setup

git config --global user.name "David"
git config --global user.email "david.rigaux@eisti.fr"

Create a new repository

git clone git@gitlab.etude.eisti.fr:rigauxdavi/Big_Data.git
cd Big_Data
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

Existing folder or Git repository

cd existing_folder
git init
git remote add origin git@gitlab.etude.eisti.fr:rigauxdavi/Big_Data.git
git add .
git commit
git push -u origin master