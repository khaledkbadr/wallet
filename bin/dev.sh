#!/usr/bin/env bash
# bin/dev
# environment variables to be defined externally for security
DOMAIN=myproject.local
BUILD_ENV="dev" \
DJANGO_USE_DEBUG=1 \
SITE_HOST="$DOMAIN" \
POSTGRES_HOST="0.0.0.0" \
POSTGRES_PASSWORD="khaled" \
POSTGRES_USER="khaled" \
POSTGRES_DB="wallet_db" \
  docker-compose $*
