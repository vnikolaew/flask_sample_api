#!/bin/sh

openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -subj "/C=US/CN=localhost" -days 365