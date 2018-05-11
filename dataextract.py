#!/usr/bin/env python
"""
dataextract
Extract raw data from json files
Created by Romain Mondon-Cancel on 2018-05-11 08:54:20
"""

import os
import json

from contants import PROFILES, JSON_FOLDER, COLORS

json_data = []

for profile in PROFILES:
    json_file = os.path.join(JSON_FOLDER, profile[:-5] + '.json')
    class_ = [class_ for class_ in COLORS.keys() if class_ in profile][0]
    spec = profile[len(class_) + profile.index(class_) + 1:-5]

    if os.path.exists(json_file):
        with open(json_file) as jf:
            json_export = json.load(jf)

        results = json_export['sim']['profilesets']['results']

        formatted_data = [(
            int(res['name'][8:]),
            res['mean'],
            res['min'],
            res['max'],
            res['stddev'],
            res['median'],
            res['first_quartile'],
            res['third_quartile'],
            res['iterations']
        ) for res in results]

        [
            duration,
            mean,
            min_,
            max_,
            stddev,
            median,
            q1,
            q3,
            iterations,
         ] = zip(*sorted(formatted_data, key=lambda x: x[0]))

        json_data += [{
            'file': json_file,
            'class': class_,
            'spec': spec,
            'duration': duration,
            'dps_mean': mean,
            'dps_min': min_,
            'dps_max': max_,
            'dps_stddev': stddev,
            'dps_median': median,
            'dps_first_quartile': q1,
            'dps_third_quartile': q3,
            'dps_iterations': iterations,
        }]

with open(os.path.join(JSON_FOLDER, 'export.json'), 'w') as jf:
    json.dump(json_data, jf, indent=4)
