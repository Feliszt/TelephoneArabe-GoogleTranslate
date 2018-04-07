import json

outputData = {}
outputData['languages'] = []

languageFile = open("listSupportedLanguages", "r")

lines = languageFile.readlines()
numLines = int(len(lines) / 2)

for line in range(0, numLines):
    lanStr = lines[line + numLines].strip("\n")
    lanCode = lines[line].strip("\n")
    outputData['languages'].append({
        'languageName' : lanStr,
        'languageCode' : lanCode
    })


with open('supportedLanguagesJSON.json', 'w') as outfile:
    json.dump(outputData, outfile)
