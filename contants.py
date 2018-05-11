# -*- coding=utf-8 -*-
"""
contants
Constants for simc hourglass
Created by Romain Mondon-Cancel on 2018-05-10 13:12:38
"""

import os

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

PROFILES_BLACKLIST = [
    'T21_Warlock.simc',
]

PROFILES = [p for p in os.listdir(PROFILES_PATH) if (
    os.path.isfile(os.path.join(PROFILES_PATH, p))
    and not any(tank in p for tank in TANK_PROFILES)
    and p not in PROFILES_BLACKLIST
)]

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
    'Priest':       '#FFFFFF',
    'Rogue':        '#FFF569',
    'Shaman':       '#0070DE',
    'Warlock':      '#9482C9',
    'Warrior':      '#C79C6E',
}

LINE_STYLES = ['-', '--', '-.', ':',
               (0, (3, 3, 1, 3, 1, 3)),  (0, (3, 3, 3, 3, 1, 3))]
