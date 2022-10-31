from scrapper import get_results
import json
results = get_results()

with open('results.json', 'w') as f:
    json.dump(results, f)