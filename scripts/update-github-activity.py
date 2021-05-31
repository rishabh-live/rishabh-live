import urllib.request
import json

USERNAME = "rishabh-live"

f = open("./README.md", "r")

fileArray = f.read().split('\n')
f.close()

indexPos = fileArray.index("<!-- START:github_activity -->")
endPos = fileArray.index("<!-- END:github_activity -->")
# print(fileArray)
del fileArray[indexPos+1:endPos]
# print(fileArray)
# print(indexPos)

writeData = "<!-- START:github_activity -->\n<table><tr><td><b>Commit</b></td><td><b>Repository</b></td><td><b>Commit Head</b></td></tr>\n"
url = "https://api.github.com/users/"+USERNAME+"/events"

response = urllib.request.urlopen(url)

data = json.loads(response.read())
i = 1
for x in data:
    if i >= 11:
        break
    try:
        if x["type"] == "WatchEvent":
            continue
        event = x["payload"]["commits"][0]["message"]
        repoName = x["repo"]["name"]
        url = "https://github.com/"+repoName
        hashKey =  x["payload"]["head"]
        hashUrl = "https://github.com/"+repoName+"/commit/"+hashKey

        writeData = writeData +"<tr><td>"+event+"</td><td><a href=\"" +url+"\">"+repoName+"</a></td><td><a href=\"" +hashUrl+"\">"+hashKey+"</a></td></tr>\n"
        i = i + 1
    except:
        pass

fileArray[indexPos] = writeData+"</table>\n"
# print(fileArray)

theData = ""
for words in fileArray:
    theData = theData + words + "\n"

theData = theData.strip()

f = open("./README.md", "w")
f.write(theData)
f.close()
print(theData)
