#!/usr/bin/env python
"""
plot
Displays the plot of the DPSes from the json exports
Created by Romain Mondon-Cancel on 2018-05-10 13:10:40
"""

import os
import json
import matplotlib.pyplot as plt

from statistics import stdev

from contants import PROFILES, JSON_FOLDER, COLORS, LINE_STYLES

# Absolute plot

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
        ax.plot(x[6:], y[6:],
                color=color,
                linestyle=line_style,
                label=f'{class_}:{spec}',
                linewidth=1)
        class_line_style[class_] += 1

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax.set_xticks(range(2, 13))
ax.xaxis.grid(alpha=0.5, linestyle='--')

plt.xlabel('Killtime (min)')
plt.ylabel('DPS')

plt.show()

# Relative

fig = plt.figure()
ax = plt.subplot(111)

class_line_style = {class_: 0 for class_ in COLORS.keys()}

profiles_data = []

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

        profiles_data += [[
            [x, y], 
            dict(color=color, linestyle=line_style, label=f'{class_}:{spec}', 
                 linewidth=1)
        ]]
        
        class_line_style[class_] += 1

dps_list = [d[0][1] for d in profiles_data]
mean_dps = [sum(dps) / len(dps) for dps in zip(*dps_list)]

for d in profiles_data:
    d[0][1] = [dps / mean for dps, mean in zip(d[0][1], mean_dps)]
    ax.plot(d[0][0], d[0][1], **d[1])

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax.set_xticks(range(2, 13))
ax.xaxis.grid(alpha=0.5, linestyle='--')

plt.xlabel('Killtime (min)')
plt.ylabel('DPS')

plt.show()

# Barplot time sensitivity

fig = plt.figure()

time_data = []

for d in profiles_data:
    dev = stdev(d[0][1])
    time_data += [[dev, d[1]['label'], d[1]['color']]]

[devs, labels, colors] = list(zip(*sorted(time_data, key=lambda x: x[0])))

plt.bar(range(len(devs)), devs, align='center', color=colors)
plt.xticks(range(len(devs)), labels)
fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
plt.ylabel('Time sensitivity')

plt.show()
