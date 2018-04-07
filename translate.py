#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse
from urllib.request import Request, urlopen
import json
import random
import time
import atexit

# function that fetches a new language
def fetchTargetLangCode(_sourceLangCode, _targetLangCode):
    while True:
        ind = random.randint(0, len(supportedLanguages)-1)
        newLanguageCode = supportedLanguages[ind]["languageCode"]
        if supportedLanguages[ind]["use"]:
            if newLanguageCode != _sourceLangCode and newLanguageCode != _targetLangCode:
                break
    return ind

# function that performs the translation
def translate(_sourceLang, _targetLangCode, _sourceString):
    #print(_sourceString)
    _sourceString = urllib.parse.quote(_sourceString)
    #print(_sourceString)
    urlString = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + _sourceLang + "&tl=" + _targetLangCode + "&dt=t&q=" + _sourceString
    #print(urlString)
    urlRequest = Request(urlString, headers={'User-Agent': 'your bot 0.1'})
    translateRes = urlopen(urlRequest).read().decode('utf8')
    translateData = json.loads(translateRes)
    translation = translateData[0][0][0]
    return translation


## MAIN PROGRAM ##
numTranslations = 5

sourceText = "Je viens de dévorer un coulommiers sur des tranches de pain noir."
startLangCode = 'fr'
fileName = "Hamon01.json"

outputData = {}
outputData["translation"] = []

# load json with supported languages
supportedLanguages = json.load(open("supportedLanguagesJSON.json"))
supportedLanguages = supportedLanguages["languages"]

# function that get a name of a language from a code
def fetchNameFromCode(_code):
    for el in supportedLanguages:
        if(el["languageCode"] == _code):
            return el["languageName"]

# function that saves results
def saveJSONFile():
    with open("data/" + fileName, 'w') as outfile:
        json.dump(outputData, outfile, sort_keys=True)

startLangName = fetchNameFromCode(startLangCode)
atexit.register(saveJSONFile)

print("[" + startLangName + "] => " + sourceText)

sourceLangCode = startLangCode
sourceLangName = startLangName
targetLangCode = ''
newTargetLangInd = 0

for num in range(0, numTranslations):
    # fetch new language
    targetLangCode = ''
    if num == numTranslations-1:
        targetLangCode = startLangCode
        targetLangName = startLangName
    else:
        newTargetLangInd = fetchTargetLangCode(sourceLangCode, targetLangCode)
        targetLangCode = supportedLanguages[newTargetLangInd]["languageCode"]
        targetLangName = supportedLanguages[newTargetLangInd]["languageName"]

    # perform translation
    translatedText = translate(sourceLangCode, targetLangCode, sourceText)
    time.sleep(0.5)
    startLangTranslate = translate(targetLangCode, startLangCode, translatedText)

    # write json
    outputData['translation'].append({
        'ind' : num+1,
        'sourceLanguageCode' : sourceLangCode,
        'sourceText' :  sourceText,
        'targetLanguageCode' : targetLangCode,
        'translatedText' : translatedText,
        'startLanguageText' :  startLangTranslate
    })

    print("\n#" + str(num+1))
    print("[" + sourceLangName + "->" + targetLangName + "] => " + translatedText)
    print("[" + targetLangName + "->" + startLangName + "] => " + startLangTranslate)

    # update stuff
    sourceText = translatedText
    sourceLangCode = targetLangCode
    sourceLangName = targetLangName
    time.sleep(1)
