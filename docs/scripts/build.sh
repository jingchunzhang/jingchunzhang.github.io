#!/bin/bash

bundle exec jekyll build
pagefind --site _site
cp -r _site/pagefind .
echo "Build complete! Search index generated and copied to source root."
