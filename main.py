import os, io
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bold-kit-371901-7d62ca675d64.json"

client = vision.ImageAnnotatorClient()

# just testing the API right now. 
# once i want to start accounting for pictures I take, 
# I would have to incorporate a loop here to iterate through my picture file names
FILE_NAME = "test_image3.jpeg"
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

i = 0
for word in response.text_annotations:
    # first text description is always text of whole image combined. needs to be removed
    if i == 0:
        i += 1
        continue
    text_data.append(word.description)
    print(word.description)


