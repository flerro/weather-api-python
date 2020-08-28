#!/usr/bin/env bash

cd `dirname $0`
cd ..

set -e

# Clean-up old dist
[ -f "dist.zip" ] && rm dist.zip
[ -d "dist" ] && rm -rf dist

mkdir dist
pip install -r requirements.txt --target dist
cp app/*.py dist/
cd dist
zip -r9 "../dist.zip" .
cd ..
