# reads lines of song title text file
lines = []
with open("songTitles.txt", "r") as f:
    lines = f.readlines()

# strips whitespace from songtitles list
i = 0
for line in lines:
    lines[i] = line.strip()
    i += 1

print(lines)
# writes to new file
with open("songTitlesStripped.txt", "w") as f:
    for line in lines:
        f.write(line)
        f.write("\n")