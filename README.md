


## How to run locally?
* Make a virtual environment `python -m venv <envname>`
* Run `source <envname>/bin/activate` to activate the virtual environment.
* Run `pip install -r requirements.txt` to install the dependencies.
* Install **redis**.
* Run `sudo npm install peer -g`. You will also need to install **npm** if it's not already there.
* Run `python manage.py makemigrations`.
* Run `python manage.py migrate`.
* Run `python manage.py runserver` to start the server.
* On another terminal, run `peerjs --port 8001` to start peerjs server.
* Now you are good to go, visit `http://localhost:8000`.

* How to run on windows
* cd C:\path\to\project
* python -m venv articvenv
* articvenv\Scripts\activate
* pip install -r requirements.txt
* npm install peer -g
* Run `python manage.py makemigrations`.
* Run `python manage.py migrate`.
* Run `python manage.py runserver` to start the server.
* On another terminal, run `peerjs --port 8001` to start peerjs server.
* Now you are good to go, visit `http://localhost:8000`.