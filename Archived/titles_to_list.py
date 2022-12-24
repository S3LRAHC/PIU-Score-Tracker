import pickle

titles = []
with open("songTitlesStripped.txt", "r") as f:
    titles = f.read().splitlines()

i = 0
for title in titles:
    titles[i] = title.casefold().split()
    i += 1

# PICKLING
with open("songTitlesList.pickle", "wb") as fp:
    pickle.dump(titles, fp)

with open("songTitlesList.pickle", "rb") as fp:
    test = pickle.load(fp)

# TESTING ALL() FUNCTION
a = ["jonathan's", "dream"]
b = ["jonathan's", "dream", "blah"]

if all(elem in b for elem in a):
    print(True)
else:
    print(False)
