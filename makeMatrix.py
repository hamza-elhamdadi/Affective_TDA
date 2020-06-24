from ripser import ripser
import nmf, math, numpy as np, os, re, itertools

actionUnitsKey = {                                                                                                                                              # dictionary mapping parts of face
    "leftEye": (0,7),                                                                                                                                           # to a subset of the Action Units list
    "rightEye": (8,15),                                                                                 
    "leftEyebrow": (16,25),
    "rightEyebrow": (26,35),
    "nose": (36,47),
    "mouth": (48,67),
    "jawline": (68,82)
}

framePattern = re.compile(r"\d{3}\.")

def min_max(subsection):
    if subsection in actionUnitsKey.keys():                                                                                                                     # check if the subsection is valid
        return actionUnitsKey[subsection]                                                                                                                       # return the value for the subsection key
    else:                                                                                                                                                       # if it's invalid
        return None                                                                                                                                             # return None

def calcDissimilarity(filename, section_list, containsHeader):
    lines = open(filename, 'r').readlines()                                                                                                                     # read the lines in the input file into a list

    if containsHeader:                                                                                                                                          # if the file has a csv header line
        lines = lines[1:]                                                                                                                                       # remove it from the list
    
    temp = [[float(line.split(' ')[1]), float(line.split(' ')[2]), float(line.split(' ')[3])] for line in lines]                                                # create a list of x,y,z coordinates (float type)

    if len(section_list) == 0:                                                                                                                                  # check is list is empty   
        data = temp                                                                                                                                             # if it is set data to the list of x,y,z coordinates
    else:                                                                                                                                                       # otherwise
        extent = [min_max(subsection) for subsection in section_list]                                                                                           # create a list of the extents of each subsection in the section list
        data = [[float(line.split(' ')[1]), float(line.split(' ')[2]), float(line.split(' ')[3])] for e in extent for line in lines[ e[0] : e[1] ]]             # set data to the subset of the temp list containing all of the points
                                                                                                                                                                # that are part of the subsections in section_list

    mat = [[nmf.distance(data[i], data[j], 3) for j in range(len(data))] for i in range(len(data))]                                                             # create a matrix where mat[i][j] - dist(data[i], data[j])

    return mat


def build(filename, section_list, emotion, personID, dataDestination):
    sections = '_'.join(section_list)                                                                                                                           # join all of the sections in the section list with '_'
    mat = calcDissimilarity(filename, section_list, False)                                                                                                      # generate mat using calcDissimilarity 

    diagrams = ripser(np.asarray(mat), distance_matrix=True)['dgms']                                                                                            # generate persistence diagram for the matrix mat
    diagrams = diagrams[0].tolist() + diagrams[1].tolist()                                                                                                      # merge h0 and h1 into one list

    frameMatchObject = framePattern.search(filename)                                                                                                            # find the framenumber in the filename
    frameNumber = filename[frameMatchObject.start():frameMatchObject.end()-1]                                                                                   # cut it out of the filename

    if len(section_list) == 0:                                                                                                                                  # if no sections
        filepath = dataDestination + '/' + personID + '/persistence/persistence_diagram_' + emotion + '_' + frameNumber + '.txt'                                # filepath is not within the subsections directory
    else:                                                                                                                                                       # else
        filepath = dataDestination + '/' + personID + '/subsections/persistence/persistence_diagram_' + sections + '_' + emotion + '_' + frameNumber + '.txt'   # filepath is within subsections directory

    pFile = open(filepath, 'w')                                                                                                                                 # open the file

    for feature in diagrams:                                                                                                                                    # save diagrams in the file
        pFile.write(str(feature[0]) + ' ' + str(feature[1]) + '\n')

dataSource = '../Data'                                                                                                                                          # directory containing person data
dataDestination = 'Data'                                                                                                                                        # directory where we will save data 
person = 'F001'                                                                                                                                                 # id for the person

ret = []
files = nmf.getFileNames(dataSource, '.bnd')                                                                                                                    # strings containing the filenames in Data/F001
subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']                                                                # all of the useful subsections of the face
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']                                                                                             # emotions in dataset

for i in range(1,len(subsections)+1):
    ret += itertools.combinations(subsections, i)

ret = map(lambda l : list(l),ret)

if __name__ == '__main__':
    for filename in files:
        print(filename)
        for section_list in ret:
            print(section_list)
            for emotion in emotions:
                build(filename, section_list, emotion, person, dataDestination)
