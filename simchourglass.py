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
import json
import matplotlib.pyplot as plt

# Constants

SIMC_PATH = os.path.join('C:\\', 'Simulationcraft(x64)', '735-01')
SIMC_BIN = os.path.join(SIMC_PATH, 'simc.exe')
PROFILES_PATH = os.path.join(SIMC_PATH, 'profiles', 'Tier21')
JSON_FOLDER = os.path.join('json')

TANK_PROFILES = [
    'Death_Knight_Blood',
    'Druid_Guardian',
    'Monk_Brewmaster',
    'Paladin_Protection',
]

PROFILES = [p for p in os.listdir(PROFILES_PATH)
            if os.path.isfile(os.path.join(PROFILES_PATH, p))
            and not any(tank in p for tank in TANK_PROFILES)]

MIN_DURATION = 60
MAX_DURATION = 720
DURATION_STEP = 10
DURATIONS = range(MIN_DURATION, MAX_DURATION+DURATION_STEP, DURATION_STEP)

COLORS = {
    'Death_Knight': '#C41F3B',
    'Demon_Hunter': '#A330C9',
    'Druid':        '#FF7D0A',
    'Hunter':       '#ABD473',
    'Mage':         '#69CCF0',
    'Monk':         '#00FF96',
    'Paladin':      '#F58CBA',
    'Priest':       '#EEEEEE',
    'Rogue':        '#FFF569',
    'Shaman':       '#0070DE',
    'Warlock':      '#9482C9',
    'Warrior':      '#C79C6E',
}

LINE_STYLES = ['-', '--', '-.', ':', (0, (3, 5, 1, 5, 1, 5)), (0, (1, 1))]

# Executing simc

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

# Plotting

fig = plt.figure()
ax = plt.subplot(111)

class_line_style = {class_: 0 for class_ in COLORS.keys()}

for profile in PROFILES:
    json_file = os.path.join(JSON_FOLDER, profile[:-5] + '.json')
    class_ = [class_ for class_ in COLORS.keys() if class_ in profile][0]
    spec = profile[len(class_) + profile.index(class_) + 1:-5]

    if os.path.exists(json_file):
        with open(json_file) as jf:
            json_export = json.load(jf)

        results = json_export['sim']['profilesets']['results']

        [x, y] = zip(*sorted(
            [(int(res['name'][8:])/60, res['mean']) for res in results],
            key=lambda x: x[0]))

        color = COLORS[class_]
        line_style = LINE_STYLES[class_line_style[class_]]
        ax.plot(x, y,
                color=color,
                linestyle=line_style,
                label=f'{class_}:{spec}',
                linewidth=1)
        class_line_style[class_] += 1

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
