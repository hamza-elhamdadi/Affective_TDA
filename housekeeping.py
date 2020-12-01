from sklearn.manifold import MDS, TSNE
import umap.umap_ as umap

valid = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']

def extend_frame(frame_index):    
    return "{0:0=3d}".format(int(frame_index))

def get_relative_index(selected_emotions, focal_emotion, frame_indices, key):
    index = 0
    focal_index = key[valid[focal_emotion]][3] 
    for i in range(len(selected_emotions)):
        if selected_emotions[i] != None and i < focal_index:
            index += key[selected_emotions[i]][2]
    index += int(frame_indices[focal_emotion])
    return index

def get_emotion_indices(emotions, key):
    indices = []
    for e in emotions:
        if e:
            indices += range(key[e][0],key[e][1])
    return indices


"""
specs = {
    perplexity:                 *ex: 30*
    key:                        *dict of keys*
    focal_emotion:              *ex: 1*
    frame_indices:              *list of frame indices*
    embedding_type:             *mds, tsne, or reld*
    dimension:                  *1 or 2*,
    emotions:                   *list of selected emotions*
    dissimilarities:            *diss matrix*
}
"""
def embed(specs):
    if specs.get('embedding_type') == 'reld':
        return specs.get('dissimilarities')[get_relative_index(
            specs.get('emotions'), 
            specs.get('focal_emotion'), 
            specs.get('frame_indices'), 
            specs.get('key'))]
    elif specs.get('embedding_type') == 'mds':
        return MDS(n_components=specs.get('dimension'),dissimilarity='precomputed', random_state=0)
    elif specs.get('embedding_type') == 'tsne':
        return TSNE(n_components=specs.get('dimension'),metric='precomputed', perplexity=specs.get('perplexity'), random_state=None)
    else:
        return umap.UMAP(n_components=specs.get('dimension'), n_neighbors=2, metric='precomputed')

def filter_data(dissimilarities_before, emotion_indices):
    dissimilarities = []
    for i in range(len(dissimilarities_before)):
        line = []
        for j in range(len(dissimilarities_before)):
            if i in emotion_indices and j in emotion_indices:
                line.append(dissimilarities_before[i][j])
        if line != []:
            dissimilarities.append(line)
    return dissimilarities

def read_matrix_file(filepath, non_metric):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    return list(
        map(
            lambda elem : list(
                map(
                    lambda l: float(l), 
                    elem.split(' ')
                )
            ), 
            lines
        )
    )

def get_selected_subsections(binary_selection):
    return [binary_selection.get(sec) for sec in ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline'] if binary_selection.get(sec) != None]

"""
specs = {
    person_data:                *ex: F001*
    difference_metric:          *bottleneck OR wasserstein*
    non_metric:                 *metric OR nonmetric*
    section_list:               *ex: ['leftEye']*
    is_two_dimensional:         *True OR False*
    data_type:                  *embedding, face, OR, persistence*
    emotion:                    *ex: Anger*
    frame_index:                *ex: 1*
    embedding_type:             *mds, tsne, or reld*
    dimension:                  *1 or 2*,
    focal_emotion:              *ex: 1*
    emotions:                   *list of selected emotions*
}
"""
def build_filepath(specs):
    sections = []
    if specs.get('data_type') != 'face':
        sections = '_'.join(specs.get('section_list')).replace('mouth', 'innermouth_outermouth') if specs.get('non_metric') == 'nonmetric' else '_'.join(specs.get('section_list'))
    if specs.get('data_type') == 'dissimilarity':
        if specs.get('non_metric') == 'geometry':
            return '/home/hamza/AffectiveTDA/outputData/geometry/{}/{}{}'.format(
                specs.get('person_data'),  
                sections, 
                '_2dimensional.csv' if specs.get('is_two_dimensional') else '.csv'
            )
        else:
            return '/home/hamza/AffectiveTDA/outputData/{}/{}/subsections/dissimilarities/{}/{}{}'.format(
                specs.get('non_metric'), 
                specs.get('person_data'), 
                specs.get('difference_metric'), 
                sections, 
                '_2dimensional.csv' if specs.get('is_two_dimensional') else '.csv'
            )
    elif specs.get('data_type') == 'diss_before':
        return '/home/hamza/AffectiveTDA/outputData/{}/{}/subsections/dissimilarities/{}/{}{}'.format(
                specs.get('non_metric'), 
                specs.get('person_data'), 
                specs.get('difference_metric'), 
                sections, 
                '_2dimensional_before.csv' if specs.get('is_two_dimensional') else '_before.csv'
            )
    elif specs.get('data_type') == 'face':
        return '/home/hamza/AffectiveTDA/Data/{}/{}/{}.bnd'.format(
            specs.get('person_data'), 
            specs.get('emotion'), 
            extend_frame(specs.get('frame_index'))
        )
    elif specs.get('data_type') == 'spearman':
        return '/home/hamza/AffectiveTDA/cache/{}/{}/spearman/{}_{}_{}_{}_{}{}'.format(
                specs.get('non_metric'), 
                specs.get('person_data'),
                specs.get('difference_metric'), 
                specs.get('embedding_type'), 
                sections, 
                '_'.join(specs.get('emotions')),
                '{}_{}Focus'.format(valid[specs.get('emotion')],specs.get('frame_indices')[specs.get('emotion')]) if specs.get('embedding_type') == 'reld' else '{}D'.format(specs.get('dimension')),
                '_2dimensional.json' if specs.get('is_two_dimensional') else '.json'
            )
    elif specs.get('data_type') == 'embedding':
        if specs.get('non_metric') == 'geometry':
            return '/home/hamza/AffectiveTDA/cache/geometry/{}/{}_{}_{}_{}{}'.format(
                    specs.get('person_data'),
                    specs.get('embedding_type'), 
                    sections, 
                    '_'.join(specs.get('emotions')),
                    '{}_{}Focus'.format(valid[specs.get('emotion')],specs.get('frame_indices')[specs.get('emotion')]) if specs.get('embedding_type') == 'reld' else '{}D'.format(specs.get('dimension')),
                    '_2dimensional.json' if specs.get('is_two_dimensional') else '.json'
                )
        else:
            return '/home/hamza/AffectiveTDA/cache/{}/{}/{}_{}_{}_{}_{}{}'.format(
                specs.get('non_metric'), 
                specs.get('person_data'),
                specs.get('difference_metric'), 
                specs.get('embedding_type'), 
                sections, 
                '_'.join(specs.get('emotions')),
                '{}_{}Focus'.format(valid[specs.get('emotion')],specs.get('frame_indices')[specs.get('emotion')]) if specs.get('embedding_type') == 'reld' else '{}D'.format(specs.get('dimension')),
                '_2dimensional.json' if specs.get('is_two_dimensional') else '.json'
            )
    else:
        return {
            'h0': '/home/hamza/AffectiveTDA/outputData/{}/{}/subsections/persistence/h0/{}/persistence_diagram_{}_{}_{}{}'.format(
                specs.get('non_metric'),
                specs.get('person_data'),
                sections, 
                sections,
                specs.get('emotion'),
                extend_frame(specs.get('frame_index')),
                '_2dimensional.txt' if specs.get('is_two_dimensional') else '.txt'
            ),
            'h1': '/home/hamza/AffectiveTDA/outputData/{}/{}/subsections/persistence/h1/{}/persistence_diagram_{}_{}_{}{}'.format(
                specs.get('non_metric'),
                specs.get('person_data'),
                sections, 
                sections,
                specs.get('emotion'),
                extend_frame(specs.get('frame_index')),
                '_2dimensional.txt' if specs.get('is_two_dimensional') else '.txt'
            )
        }

def prepare_data(emotions, embedding_type, embedding_data, dimension, key):
    data = []
    first = True
    last = 0
    for i in range(len(emotions)):
        if emotions[i]:
            a = last
            b = last + key[valid[i]][2]
            first = False
            last = b
            if dimension == 1:
                array = list(map(lambda e: float(e[0]) if embedding_type != 'reld' else float(e), embedding_data[a:b]))
                data.append([{'x': j, 'y': array[j]} for j in range(len(array))])
            else:
                array = list(map(lambda e: list(map(lambda l: float(l), e)), embedding_data[a:b]))
                data.append(list(map(lambda l: {'x': l[0], 'y': l[1]}, array)))
        else:
            data.append(None)
    return data

def read_persistence_file(filepaths):
    h_0 = []
    h_1 = []
    if isinstance(filepaths, dict):
        with open(filepaths['h0'], 'r') as file:
            for line in file.readlines():
                coords = line.split(' ')
                coordObj = {
                    'x':float(coords[0]),
                    'y':float(coords[1])
                }
                h_0.append(coordObj)
        with open(filepaths['h1'], 'r') as file:
            for line in file.readlines():
                coords = line.split(' ')
                coordObj = {
                    'x':float(coords[0]),
                    'y':float(coords[1])
                }
                h_1.append(coordObj)
    else:
        print('filepath invalid')
        return []
    return [h_0, h_1]