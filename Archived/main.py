import os, io, pickle
import Archived.getDiff as getDiff
from google.cloud import vision

# used to filter text_data list to find song title easier
ignoredWords = ['ch4rley', 'beginner', 'my', 'best', 'machine', 'best', 'feel', 'the', '$', 's', 'ss', 'sss', 'card', 
'scan', 'here', '(', 'p', ')', '||', 'p', 'the', 'rec', 'room', 'mississauga', 'square', 'one', 'double', 'single', 
'usb', 'port', 'game', 'option', 'command', 'full', 'mode', 'perfect', 'great', 'good', 'bad', 'miss', 'max', 'combo', 
'total', 'score', 'calorie', '(', 'kcal', ')', 'd', 'm', 'song', 'by', 'yak', 'wan', 'credit', '(', 's', ')', '0', 
'[', '0/1', ']', 'notice', 'kronyork', 'lx', 'roamiro', 'ext', 'mach', 'piu', 'andamiro', 'mach', 'generation']

# gets grade rank (A, S, SS, etc.) from text_data **should try to replace this method if i ever think of something better**
def getRank(text_data):
    letterCount = {'f': 0, 'd': 0, 'c': 0, 'b': 0, 'a': 0, 's': 0, 'ss': 0, 'sss': 0}
    for output in text_data:
        if output == 'f':
            letterCount['f'] += 1
        elif output == 'd':
            letterCount['d'] += 1
        elif output == 'c':
            letterCount['c'] += 1
        elif output == 'b':
            letterCount['b'] += 1
        elif output == 'a':
            letterCount['a'] += 1
        elif output == 's':
            letterCount['s'] += 1
        elif output == 'ss':
            letterCount['ss'] += 1
        elif output == 'sss':
            letterCount['sss'] += 1

    return max(letterCount, key=letterCount.get)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bold-kit-371901-7d62ca675d64.json"

client = vision.ImageAnnotatorClient()

# just testing the API right now. 
# once i want to start accounting for pictures I take, 
# I would have to incorporate a loop here to iterate through my picture file names
FILE_NAME = "test_image4.jpeg"
# r is put before path as 'raw', so backslashes aren't seen as special characters
FOLDER_PATH = r"C:\Users\Charles\Documents\GitHub\PIU-Score-Tracker\pictures"

# io.open() is the same as open()
# os.path.join() adds the file name to the folder path
# read type is binary since an AI is reading the image, not a human
with io.open(os.path.join(FOLDER_PATH, FILE_NAME), "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)

text_data = []
judges = {}
score = 0

rightOrLeft = int(input("Are scores on right side of left side of screen? (0 for L/1 for R): "))

i = 0
for word in response.text_annotations:
    # first text description is always text of whole image combined. needs to be removed
    if i == 0:
        i += 1
        continue

    # gathering judge data
    if i == 2:
        judges["perfect"] = word.description
    elif i == 3:
        judges["great"] = word.description
    elif i == 4:
        judges["good"] = word.description
    elif i == 5:
        judges["bad"] = word.description
    elif i == 6:
        judges["miss"] = word.description
    elif i == 7:
        judges["max_combo"] = word.description
    i += 1
    
    # gathering relevant text entries
    if word.description.casefold() not in ignoredWords:
        text_data.append(word.description.casefold())

    # gathering score
    try:
        if int(word.description) > 500000:
            score = int(word.description)
    except ValueError or TypeError:
        pass

# extract difficulty level
diff = getDiff.getDiffNum(text_data)

# loads song titles list from file
allTitles = []    
with open("songTitlesList.pickle", "rb") as fp:
    allTitles = pickle.load(fp)

# checking if song title in OCR output
songTitle = ""
for title in allTitles:
    if all(elem in text_data for elem in title):
        songTitle = " ".join(title)

if songTitle == "":
    print("No song title found!")
else:
    print("-----------{}------------".format(songTitle))

for key, value in judges.items():
    print(key, value)
print("score: " + str(score))
print(text_data)
