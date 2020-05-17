# import requests #install from: http://docs.python-requests.org/en/master/

# #Replace the following string value with your valid X-RapidAPI-Key.
# Your_X_RapidAPI_Key = "TxUEFxYWf2mshMi8ewP7Ydfru7lVp1cubBvjsn8YMHwuF7SOls";
# def websearch(text):
# #The query parameters: (update according to your search query)
#   q = text #the search query
#   pageNumber = 1 #the number of requested page
#   pageSize = 1 #the size of a page
#   autoCorrect = True #autoCorrectspelling
#   safeSearch = True #filter results for adult content
#   url = ""
#   response=requests.get("https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI?q={}&pageNumber={}&pageSize={}&autocorrect={}&safeSearch={}".format(q, pageNumber, pageSize, autoCorrect,safeSearch),
#   headers={
#   "X-RapidAPI-Key": Your_X_RapidAPI_Key
#   },timeout=3
#   ).json()

#   #Get the numer of items returned
#   totalCount = response["totalCount"];

#   #Get the list of most frequent searches related to the input search query
#   relatedSearch = response["relatedSearch"]

#   #Go over each resulting item
#   for webPage in response["value"]:
#   #Get the web page metadata
#     url = webPage["url"]
#     title = webPage["title"]
#     description = webPage["description"]
#     keywords = webPage["keywords"]
#     provider = webPage["provider"]["name"]
#     datePublished = webPage["datePublished"]

#     #Get the web page image (if exists)
#     imageUrl = webPage["image"]["url"]
#     imageHeight = webPage["image"]["height"]
#     imageWidth = webPage["image"]["width"]

#     thumbnail = webPage["image"]["thumbnail"]
#     thumbnailHeight = webPage["image"]["thumbnailHeight"]
#     thumbnailWidth = webPage["image"]["thumbnailWidth"]

#     #An example: Output the webpage url, title and published date:
#     print("Url: %s. Title: %s. Published Date:%s." % (url, title, datePublished))
#   return url
from azure.cognitiveservices.search.websearch import WebSearchClient
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials

def websearch(search_term):
    subscription_key = "8357f85f67e347139e320820290c4bd0"

    # Instantiate the client and replace with your endpoint.
    client = WebSearchClient(endpoint="https://api.cognitive.microsoft.com", credentials=CognitiveServicesCredentials(subscription_key))

    # Make a request. Replace Yosemite if you'd like.
    web_data = client.web.search(query=search_term)

    if hasattr(web_data.web_pages, 'value'):

        print("\r\nWebpage Results#{}".format(len(web_data.web_pages.value)))
        first_web_page = web_data.web_pages.value[0]
        print("First web page name: {} ".format(first_web_page.name))
        print("First web page URL: {} ".format(first_web_page.url))
        return first_web_page.url

    else:
        print("Didn't find any web pages...")
        return "N/A"

websearch("Zach")