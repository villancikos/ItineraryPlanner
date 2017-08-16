# Itinerary Planner

## Cloning this Repo

In order to clone this repository there are some preliminary steps you will need to do.
You will need to install all the requirements on a Linux Ubuntu.
The reason behind this is because the OPTIC Planner developed by Amanda Coles and Andrew Coles only runs on Linux and Windows.
However, this project was not tested on Linux.

### Installing Optic
The easiest way to install OPTIC is just to follow all the instructions at the KCL [Optic Website](https://nms.kcl.ac.uk/planning/software/optic.html).
Make sure to install the CPLEX version because Temporal Planners need it. Otherwise you will probably run into issues.

#### Virtual Environments and Pyenv
First of all, make sure you have virtualenvironments.
I recommend installing pyenv and pyenv virtualenvwrapper from their respective github 
Create a virtualenvironment with python 3.X installed and proceed to the next step.

#### Installing Python Requirements
On the root of the repository type 
`pip install -r requirements/local.txt` to install Django and all the batteries that come with it.
This is a cookiecutter solution from the guys that created Two Scoops of Django. So make sure to check his [repo](https://github.com/pydanny/cookiecutter-django) if you want to learn more.


install nvm
    install node v6.2.2
npm install -g gulp

install pyenv
install pyenv virtualenvwrapper
create virtual environment
install psql
create databse with same name as project


pip install -r requierements/base.txt
./manage.py createsuperuser ...
./manage.py migrate
gulp or gulp plus for extra features.


### Resources

>[Markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)


>[Useful for Database manipulation using Postgres in Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)


