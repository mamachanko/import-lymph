#!/bin/bash
cd ./public
rm -rf _site
cp ../README.md index.md
jekyll b
