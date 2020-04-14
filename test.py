import re, nmf

string = '../Data/persistence/persistence_diagram_Angry_009.bnd'

pattern = re.compile(r"_\w{3,8}_\d{3}\.")

def function(string, pattern):
    val = pattern.search(string)
    return [val.start(), val.end()]
        
    
if __name__ == '__main__':
    for filename in nmf.getFileNames('../Data/F001', '.bnd'):
        print(filename)
        print(nmf.calculateDissimilaritiesFromCSV(filename, ['jawline']))