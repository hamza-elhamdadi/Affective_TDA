import numpy as np, housekeeping

F001_key = {
    "Angry": (0,112, 112, 0),
    "Disgust": (112,220, 220-112, 1),
    "Fear": (220,331, 331-220, 2),
    "Happy": (331,442, 442-331, 3),
    "Sad": (442,556, 556-442, 4),
    "Surprise": (556,666, 666-556, 5)
}

M001_key = {
    "Angry": (0,111, 111, 0),
    "Disgust": (111,223, 223-111, 1),
    "Fear": (223,333, 333-223, 2),
    "Happy": (333,443, 443-333, 3),
    "Sad": (443,556, 556-443, 4),
    "Surprise": (556,667, 667-556, 5)
}

actionUnitsKey = {
    "leftEye": (0,7),
    "rightEye": (8,15),
    "leftEyebrow": (16,25),
    "rightEyebrow": (26,35),
    "nose": (36,47),
    "mouth": (48,67),
    "jawline": (68,82)
}

selections = ['selection_1', 'selection_2', 'selection_3']
valid = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']

"""
specs = {
    person_data:                *ex: F001*
    section_list:               *ex: ['leftEye']*
    difference_metric:          *bottleneck OR wasserstein*
    embedding_type:             *mds, tsne, or reld*
    emotions:                   *list of selected emotions*
    focal_emotion:              *ex: Anger*
    frame_indices:              *list of slider indices*
    non_metric:                 *metric OR nonmetric*
    perplexity:                 *ex: 30*
    dimension:                  *1 OR 2*
    return_dissimilarity:       *True OR False*
    is_two_dimensional:         *True OR False*
    selection:                  *ex: selection_1*
}
"""
def get_embedding_data(specs):
    specs['data_type'] = 'dissimilarity'
    filepath = housekeeping.build_filepath(specs)

    indices = housekeeping.get_emotion_indices(
        specs.get('emotions'), 
        F001_key if specs.get('person_data') == 'F001' else M001_key
    )

    print(indices)

    dissimilarities = housekeeping.filter_data(
        housekeeping.read_matrix_file(
            filepath, 
            specs.get('non_metric')
        ), 
        indices
    )

    print(len(dissimilarities))

    if specs.get('return_dissimilarity'):
        return dissimilarities
        
    embedding_data = housekeeping.embed(
        {
            'perplexity': int(specs.get('perplexity')),
            'key': F001_key if specs.get('person_data') == 'F001' else M001_key,
            'focal_emotion': specs.get('focal_emotion'),
            'frame_indices': specs.get('frame_indices'),
            'embedding_type': specs.get('embedding_type'),
            'dimension': 1 if specs.get('embedding_type') == 'reld' else 2,
            'emotions': specs.get('emotions'),
            'dissimilarities': dissimilarities
        }
    )

    if specs.get('embedding_type') != 'reld':
        embedding_data = embedding_data.fit_transform(np.asmatrix(dissimilarities))

    return housekeeping.prepare_data(
        specs.get('emotions'), 
        specs.get('embedding_type'), 
        embedding_data, 1 if specs.get('embedding_type') == 'reld' else 2, 
        F001_key if specs.get('person_data') == 'F001' else M001_key
    )

def get_face_data(person_data, emotion, frame_index):
    filepath = housekeeping.build_filepath(
        {
            'person_data': person_data,
            'emotion': emotion,
            'frame_index': frame_index,
            'data_type': 'face'
        }
    )
    with open(filepath, 'r') as file:
        data = [line[:-1].split(' ')[1:-1] for line in file.readlines()]
        data = [{"x":float(pair[0]), "y":float(pair[1])} for pair in data]

    return data

def get_persistence_diagram(section_list, person_data, emotion, frameNumber, nonMetric, twoD):
    filepaths = housekeeping.build_filepath(
        {
            'section_list': section_list,
            'person_data': person_data,
            'emotion': emotion,
            'frame_index': frameNumber,
            'is_two_dimensional': twoD,
            'non_metric': nonMetric,
            'data_type': 'persistence'
        }
    )
    return {
        'selection_1':housekeeping.read_persistence_file(filepaths['selection_1']),
        'selection_2':housekeeping.read_persistence_file(filepaths['selection_2']),
        'selection_3':housekeeping.read_persistence_file(filepaths['selection_3'])
    }
    