import os, io
from google.cloud import vision

ignoredWords = ['ch4rley', 'beginner', 'my', 'best', 'machine', 'best', 'feel', 'the', '$', 's', 'ss', 'sss', 'card', 
'scan', 'here', '(', 'p', ')', '||', 'p', 'the', 'rec', 'room', 'mississauga', 'square', 'one', 'double', 'single', 
'usb', 'port', 'game', 'option', 'command', 'full', 'mode', 'perfect', 'great', 'good', 'bad', 'miss', 'max', 'combo', 
'total', 'score', 'calorie', '(', 'kcal', ')', 'd', 'm', 'song', 'by', 'yak', 'wan', 'credit', '(', 's', ')', '0', 
'[', '0/1', ']', 'notice', 'kronyork', 'lx', 'roamiro', 'ext', 'mach', 'piu', 'andamiro', 'mach', 'generation']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bold-kit-371901-7d62ca675d64.json"

client = vision.ImageAnnotatorClient()

# just testing the API right now. 
# once i want to start accounting for pictures I take, 
# I would have to incorporate a loop here to iterate through my picture file names
FILE_NAME = "test_image2.jpeg"
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
    

for key, value in judges.items():
    print(key, value)
print("score: " + str(score))
print(text_data)
