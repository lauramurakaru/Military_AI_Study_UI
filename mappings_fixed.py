# ----- Mapping Dictionaries (Generated from your dataset) -----

Target_Category_Map = {
    'Air Base': 3,
    'Airborne Unit': 3,
    'Airfield': 2,
    'Ammo Stockpile': 2,
    'Ammunition Depot': 2,
    'Armor Unit': 3,
    'Artillery Unit': 3,
    'Barracks': 1,
    'Battalion HQ': 4,
    'Battlegroup HQ': 4,
    'Bridging Unit': 3,
    'Brigade HQ': 3,
    'Cargo Aircraft': 3,
    'Chapel': -1,
    'Checkpoint': 1,
    'Command Post': 4,
    'Division HQ': 4,
    'Dummy Target': 1,
    'Electronic Warfare Installation': 3,
    'Enemy Personnel': 1,
    'Engineering Unit': 2,
    'Fighter Aircraft': 4,
    'Frigate': 4,
    'Fuel Depot': 2,
    'High-Value Target': 5,
    'Infantry Platoon': 2,
    'Infantry Squad': 1,
    'Inflatable Military Decoy': 1,
    'Logistics Unit': 2,
    'Mast Antennas': 3,
    'Medical Installation': -5,
    'Medical Vehicle': -5,
    'Military Equipment': 1,
    'Military Equipment CL I': 1,
    'Military Equipment CL II': 1,
    'Military Equipment CL IV': 1,
    'Military Installation': 1,
    'Mobile Command Vehicle': 4,
    'Motorized Unit': 2,
    'Naval Base': 3,
    'Observation Post': 1,
    'Radar Installation': 4,
    'Reconnaissance Unit': 2,
    'Ship Maintenance Facility': 1,
    'Signal Tower': 4,
    'Sniper Team': 2,
    'Training Centre': 1,
    'Unmanned Aerial Vehicle': 2,
    'Unmanned Ground Vehicle': 1,
    'Unmanned Maritime Systems': 1,
}

Target_Vulnerability_Map = {
    'High': 4,
    'Low': 2,
    'Medium': 3,
    'Very_High': 5,
    'Very_Low': 1,
}

Terrain_Type_Map = {
    'Agricultural Land': 4,
    'Border Region': 1,
    'Communication Infrastructure': 2,
    'Critical Infrastructure Area': 2,
    'Dam and Reservoir': -5,
    'Electric Power Grid Network': 1,
    'Forested Terrain': 5,
    'Hilly Terrain': 5,
    'Historical Site': 1,
    'Industrial Zone': 2,
    'Medical Facility': -5,
    'Public Area': -4,
    'Railway Infrastructure': 2,
    'Residential Area': -4,
    'Suburban Area': -2,
    'Transportation Hub': 1,
    'Tunnel and Cave': 1,
    'Urban Center': -4,
    'Village': -3,
}

Civilian_Presence_Map = {
    '1-10': -1,
    '11-29': -2,
    '0': 0,
    '100-200': -5,
    '30-49': -3,
    '50-99': -4,
}

Damage_Assessment_Map = {
    'High': 2,
    'Low': 1,
    'Medium': 2,
    'Very_High': 3,
    'Very_Low': -1,
}

Time_Sensitivity_Map = {
    'High': 3,
    'Immediate': 5,
    'Normal': 1,
}

Weaponeering_Map = {
    '120mm Mortar': 3,
    '155mm Artillery': 4,
    'Air-to-Surface Missile': 5,
    'Anti-Personnel Mine': 1,
    'Cluster Munition': 2,
    'Cyber Weapon': 5,
    'Incendiary Weapon': 1,
    'Killer Drone': 1,
    'Laser-Guided Rocket': 5,
    'Lethal Autonomous Weapons System': 1,
    'Precision Strike Missile': 5,
    'SOF Unit': 5,
    'Sniper': 5,
    'Surface-to-Air Missile': 5,
    'Thermobaric Munition': 1,
    'Torpedo': 4,
    'Unguided Bomb': 1,
    'White Phosphorus Bomb': 1,
}

Friendly_Fire_Map = {
    'High': -1,
    'Medium': 1,
    'Low': 2,
    'Very_High': -2,
    'Very_Low': 3,
}

Politically_Sensitive_Map = {
    'High': 1,
    'Medium': 1,
    'Low': 1,
    'Very_High': -1,
    'Very_Low': 2,
}

Legal_Advice_Map = {
    'It depends': 1,
    'Lawful': 3,
    'Legitimate': 2,
    'Neutral': 2,
    'Questionable': 1,
}

Ethical_Concerns_Map = {
    'Hypothetical': 1,
    'Immoral': -2,
    'It depends': 1,
    'No': 3,
    'Plausible': 1,
    'Potential': 1,
    'Realizable': 1,
    'Theoretical': 1,
    'Unlikely': 2,
    'Yes': -2,
}

Collateral_Damage_Potential_Map = {
    'High': -2,
    'Medium': 1,
    'Low': 1,
    'Very_High': -3,
    'Very_Low': 2,
}

AI_Distinction_Map = {
    '1': -5, '2': -5, '3': -5, '4': -5, '5': -5,
    '6': -5, '7': -5, '8': -5, '9': -5, '10': -5,
    '11': -4, '12': -4, '13': -4, '14': -4, '15': -4,
    '16': -4, '17': -4, '18': -4, '19': -4, '20': -4,
    '21': -3, '22': -3, '23': -3, '24': -3, '25': -3,
    '26': -3, '27': -3, '28': -3, '29': -3, '30': -3,
    '31': -2, '32': -2, '33': -2, '34': -2, '35': -2,
    '36': -2, '37': -2, '38': -2, '39': -2, '40': -2,
    '41': -1, '42': -1, '43': -1, '44': -1, '45': -1,
    '46': -1, '47': -1, '48': -1, '49': -1, '50': -1,
    '51': 1, '52': 1, '53': 1, '54': 1, '55': 1,
    '56': 1, '57': 1, '58': 1, '59': 1, '60': 1,
    '61': 2, '62': 2, '63': 2, '64': 2, '65': 2,
    '66': 2, '67': 2, '68': 2, '69': 2, '70': 2,
    '71': 3, '72': 3, '73': 3, '74': 3, '75': 3,
    '76': 3, '77': 3, '78': 3, '79': 3, '80': 3,
    '81': 4, '82': 4, '83': 4, '84': 4, '85': 4,
    '86': 4, '87': 4, '88': 4, '89': 4, '90': 4,
    '91': 5, '92': 5, '93': 5, '94': 5, '95': 5,
    '96': 5, '97': 5, '98': 5, '99': 5, '100': 5,
}

AI_Proportionality_Map = {
    '1': -5, '2': -5, '3': -5, '4': -5, '5': -5,
    '6': -5, '7': -5, '8': -5, '9': -5, '10': -5,
    '11': -4, '12': -4, '13': -4, '14': -4, '15': -4,
    '16': -4, '17': -4, '18': -4, '19': -4, '20': -4,
    '21': -3, '22': -3, '23': -3, '24': -3, '25': -3,
    '26': -3, '27': -3, '28': -3, '29': -3, '30': -3,
    '31': -2, '32': -2, '33': -2, '34': -2, '35': -2,
    '36': -2, '37': -2, '38': -2, '39': -2, '40': -2,
    '41': -1, '42': -1, '43': -1, '44': -1, '45': -1,
    '46': -1, '47': -1, '48': -1, '49': -1, '50': -1,
    '51': 1, '52': 1, '53': 1, '54': 1, '55': 1,
    '56': 1, '57': 1, '58': 1, '59': 1, '60': 1,
    '61': 2, '62': 2, '63': 2, '64': 2, '65': 2,
    '66': 2, '67': 2, '68': 2, '69': 2, '70': 2,
    '71': 3, '72': 3, '73': 3, '74': 3, '75': 3,
    '76': 3, '77': 3, '78': 3, '79': 3, '80': 3,
    '81': 4, '82': 4, '83': 4, '84': 4, '85': 4,
    '86': 4, '87': 4, '88': 4, '89': 4, '90': 4,
    '91': 5, '92': 5, '93': 5, '94': 5, '95': 5,
    '96': 5, '97': 5, '98': 5, '99': 5, '100': 5,
}

AI_Military_Necessity_Map = {
    'Open to Debate': 1,
    'Yes': 2,
}

Human_Distinction_Map = {
    '30': -5,
    '50': -4,
    '65': -3,
    '70': 1,
    '75': 2,
    '80': 3,
    '90': 4,
    '100': 5,
}

Human_Proportionality_Map = {
    '30': -5,
    '50': -4,
    '65': -3,
    '70': 1,
    '75': 2,
    '80': 3,
    '90': 4,
    '100': 5,
}

Human_Military_Necessity_Map = {
    'Open to Debate': 2,
    'Yes': 3,
}
