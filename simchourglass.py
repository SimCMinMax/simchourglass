#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
simchourglass
A simple script to run simc with different fight durations and plot the DPS
against time.
Created by Romain Mondon-Cancel on 2018-05-09 15:52:14
"""

import subprocess
import os

from contants import PROFILES, JSON_FOLDER, SIMC_BIN, PROFILES_PATH, DURATIONS

for profile in PROFILES:
    json_file = os.path.join(JSON_FOLDER, profile[:-5] + '.json')
    subprocess.check_output([
        SIMC_BIN,
        os.path.join(PROFILES_PATH, profile),
        'fixed_time=1',
        'vary_combat_length=0.0',
        'json2={file}'.format(file=json_file),
        *[f'profileset.duration{d}=max_time={d}' for d in DURATIONS]
    ])
