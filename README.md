# README

This Flask demo is used as a sandbox environment to test or to play with code. 
The demo application contains login page with mocked data and simple implementation of CI \ CD.

Current demo could be run locally after setup.


### Configure environment


Export Flask environment:
```
export FLASK_APP=run.py
export FLASK_ENV=development
```

### Run application

Run Flask demo localy: 
```flask run```


Run demo using gunicorn: 
```gunicorn -c gunicorn.conf.py run:app```
