# MA-4012663
Git repo for survey platform used in the Master Thesis: Analyzing the influence of context and data processing transparency on sensitive and insensitive digital advertisement.

## How to install
In order to install this app locally python must be installed on the machine.
Once python is installed follow these steps (for mac/linux) to clone the repo:
```
mk survey_app
cd survey_app
git clone PASTE_HERE_REPO_LINK
```

Install a virtual enviroment and all the requirements:
```
pip install virtualenv
python -m venv venv
source venv/bin/activate
cd MA-4012663
pip install -r requirements.txt
```

Start django:
```
python manage.py runserver
```
