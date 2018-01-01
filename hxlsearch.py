'''
    You must install the requests library to use this script. Example:
        pip install requests

    Specify your HXL query as a command-line argument, e.g.:
        python hxlsearch.py '#population+refugees'
'''

from __future__ import unicode_literals, print_function

# From https://YOUR_KPI/token/
# NB: That endpoint will not generate a token automatically; if it responds
# with 404, send an empty POST to create a new token
AUTH_TOKEN = '91fc5c666510c3a093a52ff796aacc6aa33e4863'

### Configure all your URLs to end with slashes ###

# URL of a *DEPLOYED* asset, i.e. https://YOUR_KPI/assets/ASSET_UID
KPI_ASSET_URL = 'https://kf.master.kbtdev.org/assets/aoTxJTRyPXVLeeG45W67E4/'

# KC URL must not include a form-specific identifier (this will be appended)
KC_API_URL = 'https://kc.master.kbtdev.org/api/v1/'

def check_for_match(candidate, query):
    '''
    Perhaps exact matches, or some other kind of fuzzy comparison, are more
    desirable?
    '''
    return query.lower() in candidate.lower()

###############################################################################

import sys
import json
import logging
import requests
import posixpath

logging.basicConfig(level=logging.INFO) # the default is WARNING

if len(sys.argv) != 2:
    logging.error('Usage: python {} hxl_query\n'.format(sys.argv[0]))
    sys.exit(1)
query = sys.argv[1]

# This 'Authorization' header is used for both KPI and KC
request_headers={'Authorization': 'Token ' + AUTH_TOKEN}

# Get the form's JSON definition from KPI
response = requests.get(
    KPI_ASSET_URL + '?format=json',
    headers=request_headers
)
response.raise_for_status()
asset = response.json()
survey = asset['content']['survey']

# It's not necessary to store a full mapping between all the survey's HXL tags
# and question names, but having that might be useful for a future application
hxl_to_question_name = []
for question in survey:
    tags = question.get('tags')
    if not tags:
        continue
    hxl = ''.join(
        [tag.lstrip('hxl:') for tag in tags if tag.startswith('hxl:')])
    if not hxl:
        continue
    hxl_to_question_name.append((hxl, question['name']))

# Find the names of all the questions whose HXL tags match the query
matches = [
    name for hxl, name in hxl_to_question_name if check_for_match(hxl, query)]
if not matches:
    logging.info(
        'Your query, "{query}", does not match any questions in this '
        'form'.format(query=query)
    )
    sys.exit(1)

logging.info(
    'Your query, "{query}", matches the following question names:'.format(
        query=query)
)
for match in matches:
    logging.info('\t' + match)

# Now, construct the KC URL for retrieving form data. This is convoluted, and a
# simpler, KPI-only solution will be available soon
kc_id_string = posixpath.split(asset['deployment__identifier'])[-1]
response = requests.get(
    '{kc_url}forms?format=json&id_string={id_string}'.format(
        kc_url=KC_API_URL, id_string=kc_id_string),
    headers=request_headers
)
response.raise_for_status()
kc_forms = response.json()
if len(kc_forms) > 1:
    raise Exception(
        'Oops, a particular id_string should only ever match one KC form!')
kc_form = kc_forms[0]
kc_data_url = kc_form['url'].replace('/api/v1/forms/', '/api/v1/data/')
assert kc_data_url.endswith('?format=json')

# Instruct KC to retun data only for questions whose HXL tags matched the query
# NB: KC always returns "_id" for each submission in addition to any specified
# fields
kc_data_url += '&fields=' + json.dumps(matches)

# Retrieve the data from KC
response = requests.get(kc_data_url, headers=request_headers)
response.raise_for_status()

# Just print the data to the screen for this example
logging.info('******* BEGIN JSON SUBMISSION OUTPUT *******')
print(json.dumps(response.json(), indent=2, sort_keys=True))
