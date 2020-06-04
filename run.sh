#!/bin/bash

if [[ $JWT_SECRET = "" ]]
    then
        echo "Json WEB secret is not initialized!"
        echo "Generating JWT secret..."
        export JWT_SECRET=$(python util/jwk.py)
        echo "JWT secret: " $JWT_SECRET
fi

exec gunicorn --bind=0.0.0.0:8080 --workers=1 wsgi:app
