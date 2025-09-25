#!/bin/bash
set -e


# Start Superset
exec gunicorn \
  -b 0.0.0.0:8088 \
  --workers 3 \
  --worker-class gevent \
  'superset.app:create_app()'
# exec superset run -p 8088 --with-threads --reload --debugger

