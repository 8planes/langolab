#!/bin/bash

python /opt/google-closure/closure/bin/build/depswriter.py \
    --root_with_prefix="public/js/conversations ../../js/conversations" > \
    public/js/conversations/dependencies.js
