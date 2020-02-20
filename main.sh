for f in ../Data/F001/Angry/* ; do
    echo -e "${f}\nAngry" | python3 main.py
    done

for f in ../Data/F001/Disgust/* ; do
    echo -e "${f}\nDisgust" | python3 main.py
    done

for f in ../Data/F001/Fear/* ; do
    echo -e "${f}\nFear" | python3 main.py
    done

for f in ../Data/F001/Happy/* ; do
    echo -e "${f}\nHappy" | python3 main.py
    done

for f in ../Data/F001/Sad/* ; do
    echo -e "${f}\nSad" | python3 main.py
    done

for f in ../Data/F001/Surprise/* ; do
    echo -e "${f}\nSurprise" | python3 main.py
    done