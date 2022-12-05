#!/bin/bash -l

conda activate impacts_toolbox
cd /net/home/h02/hadhy/PycharmProjects/esms_viz/
bokeh serve --allow-websocket-origin=vld389:5006 gwl_bokeh.py
