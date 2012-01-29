#!/bin/bash

python media/js/closure/bin/build/depswriter.py  --root_with_prefix="media/js ../.." > media/js/ll-deps.js
