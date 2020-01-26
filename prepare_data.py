import json
import random


data_file_path = 'data.json'


def prepare_data(data_types):
    data = []
    for data_type in data_types:
        with open(f'{data_type}.txt') as f:
            dialogs = f.read().split('\n\n')
        data_dialog = []
        for idx, dialog in enumerate(dialogs):
            utters = []
            for utter in dialog.splitlines():
                if utter.startswith('A: ') or utter.startswith('B: '):
                    utters.append(utter[3:])
                elif utter.startswith('Pred-A: ') or utter.startswith('Pred-B: '):
                    utters.append(utter[8:])
            data_dialog.append({
                'id': idx,
                'type': data_type,
                'utters': utters,
                'score': None,
            })
        print(f'Loaded {data_type}.txt, {len(data_dialog)} dialogs')
        data.extend(data_dialog)
    random.shuffle(data)
    with open(data_file_path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    prepare_data(['seq2seq', 'kw-seq2seq'])
