import json

from plotly.graph_objs import Layout
from plotly import offline

filename = 'data/fire_data_gm1.json'
with open(filename, encoding='utf-8') as f:
    all_fire_data = json.load(f) # Write the entire data
    
all_fire_dicts = [
    fire for fire in all_fire_data 
    if float(fire['brightness']) > 330 and fire['confidence'] in ['n', 'h'] # Filter the fire data
    ]

# set the hover texts
hover_texts = [
    f"Date: {fire['acq_date']}<br>Brightness: {fire['brightness']}<br>Confidence: {fire['confidence']}"
    for fire in all_fire_dicts
]


lats, lons, brightness, scans = [], [], [], []
for fire_dict in all_fire_dicts:
    lats.append(float(fire_dict['latitude']))
    lons.append(float(fire_dict['longitude']))
    brightness.append(fire_dict['brightness'])
    scans.append(fire_dict['scan'])


# Settings the data for the map
data = [
    {
        'type': 'scattergeo', 
        'lon': lons,
        'lat': lats,
        'text': hover_texts,
        'hoverinfo': 'text',
        'marker': {
            'size': [scan * 6 for scan in scans],
            'color': scans,  # Determines colour used
            'colorscale': 'Bluered',  # Determines which color to display
            'reversescale': True,  # Determines how the color will be reversed
            'colorbar': {
                'title': 'Fire Detected in The Gambia'  # Display title on the sidebar color
                    },
    
        },
    }
    
]

my_layout = Layout(
    title='Fire detected in The Gambia from January to July 2025',
    geo=dict(
        scope='africa',
        projection=dict(type='mercator'),
        showland=True,
        landcolor='rgb(195,228,243)',
        showcountries=True, # display country border
        lonaxis=dict(range=[-17, -13]),
        lataxis=dict(range=[12, 14.5]),
        resolution=50,

    )

    )

fig = {
    'data': data, 
    'layout': my_layout,
}
offline.plot(fig, filename='gam_fire_data.html')