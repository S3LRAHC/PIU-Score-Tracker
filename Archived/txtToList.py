lines = []

with open("ignoredWords.txt", "r") as f:
    lines = f.read().splitlines()

i = 0
for line in lines:
    lines[i] = line.strip()
    i += 1

print(lines)