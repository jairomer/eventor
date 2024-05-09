#!/bin/bash 

sed -i '/API_MASTER_KEY/d' .env 
export HASH=$(dd if=/dev/urandom bs=1 count=32 2>/dev/null | sha256sum | awk '{ print $1 }')
echo API_MASTER_KEY=$HASH >> .env
