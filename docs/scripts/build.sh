#!/bin/bash

bundle exec jekyll build
npx pagefind --site _site
echo "Build complete with search index!"
