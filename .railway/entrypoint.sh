#!/bin/sh
apt-get update && apt-get install -y \
    libgobject-2.0-0 \
    libffi-dev \
    libcairo2 \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    python3-cffi
exec waitress-serve --call 'app:create_app'
