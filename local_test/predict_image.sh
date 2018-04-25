#!/bin/sh

file=$1

curl -X POST --data-binary @${file} -H "Accept: application/json" -H "Content-Type: application/x-image" http://localhost:8080/invocations 
