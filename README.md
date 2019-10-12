# WM workshop manager

Workshop manager (WM) is an open source software for repair businesses.

## Description

With WM you can:
- efficiently manage your jobs, invoices, and quotes
- keep vehicles history in cloud
- being ables to access your records anywhere and anytime
- monitor performance of you workshop and every employee

## Installation

Create a folder for project:

```bash
mkdir WM
cd WM
```

Setup virtual environment with Python ver 3.7 and activete it:

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

Fork & clone repository:

```bash
git clone <your-github-repo-url>/workshop-manager/
```

Install dependencies:

```bash
cd wm-django
pip install requirements.txt
```

Make migrations:

```bash
python manage.py migrate
```

Run server:

```bash
python manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)