import json
with open('/Users/thanakrit/Documents/Thai Music Thesis/(TO_CLEAN)_Phrase_1_Experiments.ipynb') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell.get('id') == 'f87293f3':
        print(f'Cell {i+1}, outputs count: {len(cell.get("outputs", []))}')
        for out in cell.get('outputs', []):
            print('Output type:', out.get('output_type'))
            if 'text' in out:
                print(''.join(out['text'])[:2000])
        break
