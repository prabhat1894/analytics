#!/usr/bin/env python
# Boiler plate to run our little app server
# Author: Ankur Srivastava

from app import app

app.run(debug=True,
        host='0.0.0.0' )#All interfaces
