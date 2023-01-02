import os, io, pickle, datetime
import pandas as pd
from google.cloud import vision

# used to filter text_data list to find song title easier
ignoredWords = ['ch4rley', 'beginner', 'my', 'best', 'machine', 'best', 'feel', 'the', '$', 'card', 
'scan', 'here', '(', 'p', ')', '||', 'p', 'the', 'rec', 'room', 'mississauga', 'square', 'one', 'double', 'single', 
'usb', 'port', 'game', 'option', 'command', 'full', 'mode', 'perfect', 'great', 'good', 'bad', 'miss', 'max', 'combo', 
'total', 'score', 'calorie', '(', 'kcal', ')', 'd', 'm', 'song', 'by', 'yak', 'wan', 'credit', '(', ')', '0', 
'[', '0/1', ']', 'notice', 'kronyork', 'lx', 'roamiro', 'ext', 'mach', 'piu', 'andamiro', 'mach', 'generation']

# function to get difficulty value from text_data
# CURRENT RECORDED DIFFICULTYS: 15-22
# Do not make the range of difficulty's too large
def getDiffNum(text_data):
    diffNum = 0
    for output in text_data:
        try:
            if int(output) >= 15 and int(output) <= 22 and len(output) == 2:
                diffNum = int(output)
        except ValueError or TypeError:
            pass
    
    return diffNum

# function to get rank from judge data
def getRank(judges):
    if judges["miss"] == 0 and judges["bad"] == 0 and judges["good"] == 0 and judges["great"] == 0:
        rank = 'sss'
    elif judges["miss"] == 0 and judges["bad"] == 0 and judges["good"] == 0:
        rank = 'ss'
    elif judges["miss"] <= 0:
        rank = 's'
    else:
        rank = 'a'
    return rank

# authenticate service account with cloud vision API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bold-kit-371901-6900c40b30bb.json"

# initialize client
client = vision.ImageAnnotatorClient()

# gather all image file names
FOLDER_PATH = os.path.abspath(os.getcwd())
rightOrLeft = int(input("Extract scores from lsScores or rsScores? (0 for L/1 for R): "))
if rightOrLeft == 0:
    FOLDER_PATH = FOLDER_PATH + r"\pictures\lsScores"
else:
    FOLDER_PATH = FOLDER_PATH + r"\pictures\rsScores"
allPicsList = os.listdir(FOLDER_PATH)

# for loop to repeat text extraction process for all files in the folder
for FILE_NAME in allPicsList:
    # read type is binary since an AI is reading the image, not a human
    with io.open(os.path.join(FOLDER_PATH, FILE_NAME), "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    text_data = []
    judges = {}
    score = 0
    scoreIndex = 0
    i = 0

    # extract image text
    for word in response.text_annotations:
        # first text description is always text of whole image combined. needs to be removed
        if i == 0:
            i += 1
            continue

        # gathering judge data for left side score
        if rightOrLeft == 0:
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

        # gathering relevant text entries
        if word.description.casefold() not in ignoredWords:
            text_data.append(word.description.casefold())
            i += 1

        # gathering score
        try:
            if int(word.description) > 500000:
                score = int(word.description)
                scoreIndex = i - 2
        except ValueError or TypeError:
            pass

    # gets judge data from scoreIndex for right side scores
    if rightOrLeft == 1:
        judges["perfect"] = text_data[scoreIndex - 6]
        judges["great"] = text_data[scoreIndex - 5]
        judges["good"] = text_data[scoreIndex - 4]
        judges["bad"] = text_data[scoreIndex - 3]  
        judges["miss"] = text_data[scoreIndex - 2]
        judges["max_combo"] = text_data[scoreIndex - 1]

    # converts judges values to int. skips if value is not an int
    # wordTo_ converts certain strings to integers when API reads wrong
    wordTo0 = ['oot']
    for key, value in judges.items():
        try:
            judges[key] = int(value)
        except ValueError:
            # for future data processing, i will ignore -1 values if text cannot be extracted properly
            if value.casefold() in wordTo0:
                judges[key] = 0
            else:
                judges[key] = -1

    # extract difficulty level
    diff = getDiffNum(text_data)

    # gather grade rank from score data
    rank = getRank(judges)

    # loads song titles list from file
    allTitles = []    
    with open("songTitlesList.pickle", "rb") as fp:
        allTitles = pickle.load(fp)

    # checking if song title in OCR output
    songTitle = ""
    for title in allTitles:
        if all(elem in text_data for elem in title):
            songTitle = " ".join(title)

    # gathering RGB information of dominant colours
    colour_data = []
    response_image = client.image_properties(image=image)
    for i in response_image.image_properties_annotation.dominant_colors.colors:
        colours = str(i.color)
        rgbList = colours.splitlines()
        for x in range(3):
            colonIndex = rgbList[x].rfind(':')
            rgbList[x] = int(rgbList[x][colonIndex + 2:])
        colour_data.append(rgbList)

    # checking precense of gray A colour (stage passed or failed)
    grayPresent = False
    rValue = 90
    gValue = 130
    bValue = 170
    for i in range(len(colour_data)):
        if colour_data[i][0] > rValue and colour_data[i][1] > gValue and colour_data[i][2] > bValue:
            grayPresent = True
    passOrFail = ""
    if grayPresent == True:
        passOrFail = "-"
    rank = rank + passOrFail

    # PRINT ALL RELEVANT INFORMATION BELOW
    if songTitle == "":
        print("---------------------No song title found!-----------------------")
    else:
        print("-----------{}------------".format(songTitle))

    for key, value in judges.items():
        print(key, value)
    print("score: " + str(score))
    print("difficulty: {}".format(diff))
    print("grade: {}".format(rank))
    print(text_data)

    # appending data to Scores.csv 
    # data = {
    #     'Date': [str(datetime.date.today())],
    #     'File Name': [FILE_NAME],
    #     'Song': [songTitle.title()],
    #     'Difficulty': [diff],
    #     'Perfect': [judges['perfect']],
    #     'Great': [judges['great']],
    #     'Good': [judges['good']],
    #     'Bad': [judges['bad']],
    #     'Miss': [judges['miss']],
    #     'Max Combo': [judges['max_combo']],
    #     'Score': [score],
    #     'Grade': [rank.upper()]
    # }
    # df = pd.DataFrame(data)
    # df.to_csv('Scores.csv', mode='a', index=False, header=False)
