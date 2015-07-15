#!/bin/bash
set -e

rm -rf out || exit 0
mkdir out

./scripts/build_pages.sh

cd out

cp -r ../public/_site out
cp ../public/CNAME ./CNAME

git init
git config user.name "Travis CI"

git add .
git commit -m "build github pages"
git push --force --quiet "https://${GITHUB_TOKEN}@github.com/mamachanko/import-lymph.git" master:gh-pages > /dev/null 2>&1
