from flask import Flask, request, render_template, send_from_directory, send_file
from scipy.spatial import distance
from scipy.stats import spearmanr
from os import path
import getData, json, housekeeping

app = Flask(__name__)

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
selections = ['selection_1', 'selection_2', 'selection_3']
slidevalues = ['slideValue1', 'slideValue2', 'slideValue3', 'slideValue4', 'slideValue5', 'slideValue6']

def error(err):
    print(err)

@app.route('/')
def return_index():
    return send_file('index2.html')

@app.errorhandler(404)
def page_notfound(error):
    print('Error: ' + str(error))
    return 'This page does not exist', 404

@app.route('/shepard', methods=['GET'])
def get_shepard_diagram():
    spearman_file = housekeeping.build_filepath(
        {
            'person_data': request.args.get('personData'),
            'difference_metric': request.args.get('differenceMetric'),
            'non_metric': request.args.get('nonMetric'),
            'section_list': housekeeping.get_selected_subsections(request.args),
            'is_two_dimensional': False if request.args.get('twoD') == '3d' else True,
            'data_type': 'spearman',
            'emotion': int(request.args.get('focalEmotion')),
            'embedding_type': request.args.get('embeddingType'),
            'emotions': list(filter(lambda e: True if e != None else False, [e if request.args.get(e) == '1' else None for e in emotions]))
        }
    )

    if path.exists(spearman_file):
        with open(spearman_file, 'r') as file:
            spearmans = json.load(file)
        return json.dumps(spearmans)

    emotion_file = housekeeping.build_filepath(
        {
            'person_data': request.args.get('personData'),
            'difference_metric': request.args.get('differenceMetric'),
            'non_metric': request.args.get('nonMetric'),
            'section_list': housekeeping.get_selected_subsections(request.args),
            'is_two_dimensional': False if request.args.get('twoD') == '3d' else True,
            'data_type': 'embedding',
            'emotion': int(request.args.get('focalEmotion')),
            'embedding_type': request.args.get('embeddingType'),
            'emotions': [emotions[i] for i in range(len(emotions)) if request.args.get(emotions[i]) == '1']
        }
    )

    before_file = housekeeping.build_filepath(
        {
            'person_data': request.args.get('personData'),
            'difference_metric': request.args.get('differenceMetric'),
            'non_metric': request.args.get('nonMetric'),
            'section_list': housekeeping.get_selected_subsections(request.args),
            'is_two_dimensional': False if request.args.get('twoD') == '3d' else True,
            'data_type': 'diss_before',
            'emotion': int(request.args.get('focalEmotion')),
            'embedding_type': request.args.get('embeddingType'),
            'emotions': [emotions[i] for i in range(len(emotions)) if request.args.get(emotions[i]) == '1']
        }
    )

    with open(emotion_file, 'r') as file:
        embedded_data = [
            (m['x'],m['y']) 
            for l in json.load(file)        # iterate
            if l != None                    # remove None values
            for m in l                      # flatten
        ]
    
    matrix_before = getData.get_embedding_data(
        {
            'person_data': request.args.get('personData'),
            'section_list': housekeeping.get_selected_subsections(request.args), 
            'difference_metric': request.args.get('differenceMetric'), 
            'embedding_type': request.args.get('embeddingType'), 
            'emotions': [emotions[i] for i in range(len(emotions)) if request.args.get(emotions[i]) == '1'], 
            'focal_emotion': int(request.args.get('focalEmotion')), 
            'frame_indices': [request.args.get(slidevalues[i]) for i in range(len(slidevalues))], 
            'non_metric': request.args.get('nonMetric'), 
            'perplexity': request.args.get('perplexity'), 
            'return_dissimilarity': True, 
            'is_two_dimensional': False if request.args.get('twoD') == '3d' else True
        }
    )
    
    matrix_after = [[distance.euclidean(d, e) for d in embedded_data] for e in embedded_data] 
    spearmans = spearmanr([l for line in matrix_before for l in line],[l for line in matrix_after for l in line])

    with open(spearman_file, 'w') as file:
        file.write(json.dumps(spearmans))

    return json.dumps(spearmans)

@app.route('/embedding', methods=['GET'])
def get_embedding_data():
    emotionFile = housekeeping.build_filepath(
        {
            'person_data': request.args.get('personData'),
            'difference_metric': request.args.get('differenceMetric'),
            'non_metric': request.args.get('nonMetric'),
            'section_list': housekeeping.get_selected_subsections(request.args),
            'is_two_dimensional': False if request.args.get('twoD') == '3d' else True,
            'data_type': 'embedding',
            'frame_indices': [request.args.get(slidevalues[i]) for i in range(len(slidevalues))],
            'focal_emotion': int(request.args.get('focalEmotion')), 
            'emotion': int(request.args.get('focalEmotion')),
            'embedding_type': request.args.get('embeddingType'),
            'emotions': list(filter(lambda e: True if e != None else False, [e if request.args.get(e) == '1' else None for e in emotions]))
        }
    )
    
    if not path.exists(emotionFile):
        data = getData.get_embedding_data(
            {
                'person_data': request.args.get('personData'),
                'section_list': housekeeping.get_selected_subsections(request.args), 
                'difference_metric': request.args.get('differenceMetric'), 
                'embedding_type': request.args.get('embeddingType'), 
                'emotions': [e if request.args.get(e) == '1' else None for e in emotions], 
                'focal_emotion': int(request.args.get('focalEmotion')), 
                'frame_indices': [request.args.get(slidevalues[i]) for i in range(len(slidevalues))], 
                'non_metric': request.args.get('nonMetric'), 
                'perplexity': request.args.get('perplexity'), 
                'return_dissimilarity': False, 
                'is_two_dimensional': False if request.args.get('twoD') == '3d' else True
            }
        )
        with open(emotionFile, 'w') as file:
            file.write(json.dumps(data))
    else:
        with open(emotionFile, 'r') as file:
            data = json.load(file)

    return json.dumps(data)

@app.route('/face', methods=['GET'])
def get_face_data():
    requests = [int(request.args.get(x)) for x in emotions]
    return json.dumps([
        getData.get_face_data(
            request.args.get('personData'), 
            emotions[i], 
            request.args.get(slidevalues[i])
        ) if requests[i] == 1
        else None
        for i in range(len(requests))
    ])

@app.route('/persistence', methods=['GET'])
def get_persistence_diagram():
    requests = [int(request.args.get(x)) for x in emotions]
    x = json.dumps([
        getData.get_persistence_diagram(
            housekeeping.get_selected_subsections(request.args), 
            request.args.get('personData'),
            emotions[i], 
            request.args.get(slidevalues[i]), 
            request.args.get('nonMetric'), 
            False if request.args.get('twoD') == '3d' else True 
        ) if requests[i] == 1
        else None
        for i in range(len(requests))
    ]).replace('Infinity', '"Infinity"')
    return x

app.run(host='0.0.0.0', port=2500)
