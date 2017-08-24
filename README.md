# Itinerary Planner

### Cloning this Repo

In order to clone this repository there are some preliminary steps you will need to do.
You will need to install all the requirements on a Linux Ubuntu.
The reason behind this is because the OPTIC Planner developed by J. Benton, Amanda Coles and Andrew Coles only runs on Linux and Windows.
However, this project was only tested on Linux.

### Installing Optic
The easiest way to install OPTIC is just to follow all the instructions at the KCL [Optic Website](https://nms.kcl.ac.uk/planning/software/optic.html).
Make sure to install the CPLEX version because Temporal Planners need it. Otherwise you will probably run into issues with prefereces.

#### Virtual Environments and Pyenv
First of all, make sure you have virtualenvironments.
I recommend installing pyenv and pyenv virtualenvwrapper from their respective github to manage different versions of Python.
Create a virtualenvironment with python 3.X installed and proceed to the next step.

#### Installing Python Requirements
On the root of the repository after activating your custom virtual environment  (you will see a $(my_virtual_env) prefixed to the terminal prompt).
`pip install -r requirements/local.txt` to install Django and all the batteries that come with it.
This is a cookiecutter solution from the guys that created Two Scoops of Django. So make sure to check his [repo](https://github.com/pydanny/cookiecutter-django) if you want to learn more.

### Running the solution
If everything went well you must create the database using PSQL.
The database name should be "itineraryplanner".
After installing it. Go to the itineraryplanner folder (the project folder) and look for the manage.py file.
Run `$./manage.py migrate` to install all the migrations needed by the project. If this doesn't work try running `$./manage.py makemigrations` first.
 
If everything went well you can now run `$/.manage.py runserver` or `$/.manage.py runserver_plus` if you prefer the extra tools.

#### EXTRAS
To run gulp you must install either node.js and npm or `nvm` (Node Version Manager)[https://github.com/creationix/nvm].
You may first need to do `npm install` to install all the dependencies mentioned on the `package.json` file on the root as well.
Gulps helps develop the front-end easily through the `gulpfile.js` command added at the root of this project.


#### Resources

>[Markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

>[Useful for Database manipulation using Postgres in Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)


