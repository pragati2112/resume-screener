from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
import pandas as pd
import os
import numpy as np
import PyPDF2
from starlette.requests import Request
import json

async def homepage(request):

    req = await request.json()
    list = req["data"]

    currentDirectory = os.getcwd()
    os.chdir(os.getcwd()+"/static/pdf/")
    files = os.listdir()
    response = []
    for file in files:
        newCurrentDirectory = currentDirectory + "/static/pdf/"
        os.chdir(newCurrentDirectory)
        print(file)
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        number_of_pages = pdfReader.getNumPages()

        commaSeperatedValue = []
        for page_number in range(number_of_pages):
            pageObj = pdfReader.getPage(page_number)
            page1 = pageObj.extractText()
            page1 = str.splitlines(page1)

            for word in page1:
                if word == " " or word == "," or word == "-" or word == ":" or word == "/" or word == "." or word == "&":
                    continue
                else:
                    if ':' in word:
                        word = word.replace(':', "")
                    if '.' in word:
                        word = word.replace('.', "")
                    if '.com' in word:
                        word = word.replace('.com', "")
                    if ',' in word:
                        word = word.replace(',', "")
                    if '&' in word:
                        word = word.replace('&', " ")

                    splitWord = word.split(" ")
                    for singleWord in splitWord:
                        if singleWord == '':
                            continue
                        commaSeperatedValue.append(singleWord)

        print(commaSeperatedValue)

        df = pd.DataFrame(commaSeperatedValue)
        df.columns = ['list']
        os.chdir(currentDirectory+"/static/")
        df.to_csv('list.csv', index=False)
        data = pd.read_csv("list.csv")
        print(data)

        for value in list: 

# {
#   "data:" : ["HTMl","CSS"]  
# }
            if data['list'].str.contains(str(value)).any():
                response.append(file)

    print("All done here")
    return JSONResponse(json.dumps(response))
#['html', 'css', 'javascript']

routes = [
       Mount('/static', app=StaticFiles(directory='static'), name='static'),
       Route('/pdf', endpoint=homepage,methods=["POST"])
    ]


app = Starlette(debug=True, routes=routes)