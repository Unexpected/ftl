$env:FLASK_APP = "engine.py"
$env:FLASK_ENV = "development"
python -m flask run

$env:FLASK_APP = "other.py"