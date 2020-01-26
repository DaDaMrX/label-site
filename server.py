import json
import os
from collections import Counter

import flask


data_file_path = 'data.json'
score_file_path = 'score.json'


score = None


def init_data():
    """Load or create score file for global `score` variable.
    """
    global score
    if os.path.exists(score_file_path):
        with open(score_file_path) as f:
            score = json.load(f)
        print(f'Loaded {score_file_path}')
    else:
        with open(data_file_path) as f:
            data = json.load(f)
        counter = Counter(a['type'] for a in data)
        score = {}
        for data_type, num in counter.items():
            score[data_type] = [{'id': i} for i in range(num)]
            print(f'{data_type} has {num} items.')
        with open(score_file_path, 'w') as f:
            json.dump(score, f, indent=2)


app = flask.Flask(__name__, static_folder='')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<name>')
def score(name):
    with open('score.html') as f:
        html = f.read()
    html = html.replace('[[name]]', name)
    return html


@app.route('/result')
def result_page():
    return app.send_static_file('result.html')


@app.route('/data/<name>')
def get_data(name):
    with open(data_file_path) as f:
        data = json.load(f)
    global score
    for item in data:
        data_type, idx = item['type'], item['id']
        if score[data_type][idx].get(name) is not None:
            item['score'] = score[data_type][idx][name]
        else:
            item['score'] = '_'
    return flask.jsonify(data)


@app.route('/score', methods=['POST'])
def set_score():
    item = flask.request.get_json()
    print(item)
    global score
    data_type, idx = item['type'], item['id']
    name, s = item['name'], item['score']
    assert score[data_type][idx]['id'] == idx
    score[data_type][idx][name] = s
    with open(score_file_path, 'w') as f:
        json.dump(score, f, indent=2)
    return 'OK'


@app.route('/result_data')
def result_data():
    score_map = {
        1: 'score1', 2: 'score2', 3: 'score3',
        4: 'score4', 5: 'score5',
    }
    global score
    data = {}
    for data_type, data_scores in score.items():
        data[data_type] = {}
        for item in data_scores:
            for name, point in item.items():
                if name == 'id':
                    continue
                if name not in data[data_type]:
                    data[data_type][name] = {
                        'score1': 0, 'score2': 0, 'score3': 0,
                        'score4': 0, 'score5': 0, 'average': 0,
                        'finished': 0, 'progress': 0,
                    }
                data[data_type][name][score_map[point]] += 1
        for name, stat in data[data_type].items():
            for i in range(1, 6):
                stat['finished'] += stat[score_map[i]]
                stat['average'] += i * stat[score_map[i]]
            stat['average'] /= stat['finished']
            stat['progress'] = stat['finished'] / len(data_scores)
    return flask.jsonify(data)


if __name__ == '__main__':
    init_data()
    app.run(host='0.0.0.0', port=1234, debug=True)
