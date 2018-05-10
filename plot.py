#!/usr/bin/env python
"""
plot
Displays the plot of the DPSes from the json exports
Created by Romain Mondon-Cancel on 2018-05-10 13:10:40
"""

import os
import json
import matplotlib.pyplot as plt

from contants import PROFILES, JSON_FOLDER, COLORS, LINE_STYLES

plt.style.use('dark_background')
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
        ax.plot(x[7:], y[7:],
                color=color,
                linestyle=line_style,
                label=f'{class_}:{spec}',
                linewidth=1)
        class_line_style[class_] += 1

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.xlabel('Killtime (min)')
plt.ylabel('DPS')

plt.show()
