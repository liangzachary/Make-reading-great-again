import requests #install from: http://docs.python-requests.org/en/master/
Your_X_RapidAPI_Key = "TxUEFxYWf2mshMi8ewP7Ydfru7lVp1cubBvjsn8YMHwuF7SOls";

def imagesearch(text):
  #The query parameters: (update according to your search query)
  q = text #the search query
  pageNumber = 1 #the number of requested page
  pageSize = 1 #the size of a page
  autoCorrect = True #autoCorrectspelling
  safeSearch = True #filter results for adult content
  imageUrl = ""

  response=requests.get("https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI?q={}&pageNumber={}&pageSize={}&autocorrect={}&safeSearch={}".format(q, pageNumber, pageSize, autoCorrect,safeSearch),
  headers={
  "X-RapidAPI-Key": Your_X_RapidAPI_Key
  },timeout=3
  ).json()

  #Get the numer of items returned
  totalCount = response["totalCount"]
  
  #Go over each resulting item
  for image in response["value"]:

    # Get the image
    imageUrl = image["url"]
    imageHeight = image["height"]
    imageWidth = image["width"]

    # Get the image thumbail
    thumbnail = image["thumbnail"]
    thumbnailHeight = image["thumbnailHeight"]
    thumbnailWidth = image["thumbnailWidth"]
    #An example: Output the webpage url, title and published date:
    print("imageUrl: %s. imageHeight: %s. imageWidth: %s." % (imageUrl, imageHeight, imageWidth))
    
  
  return imageUrl