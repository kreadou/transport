#The following will run waitress on port 8080 on all available IPv4 addresses, but not IPv6.
#.. code-block:: python
import os, sys
from waitress import serve
from transport.wsgi import application

if __name__ == "__main__":
    serve(application, host='*', port=8000, threads=100)
