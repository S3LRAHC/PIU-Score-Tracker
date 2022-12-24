# gets difficulty value from text_data in main
def getDiffNum(text_data):
    diffNum = 0
    for output in text_data:
        try:
            if int(output) >= 15 and int(output) <= 22 and len(output) == 2:
                diffNum = int(output)
        except ValueError or TypeError:
            pass
    
    return diffNum
