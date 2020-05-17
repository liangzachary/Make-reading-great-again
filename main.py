
from flask import Flask
from flask import request, send_from_directory, render_template
from flask_cors import CORS
from textblob import TextBlob
from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from bs4 import BeautifulSoup

from msrest.authentication import CognitiveServicesCredentials
import imagesearch
import boto3  # https://www.w3schools.com/w3css/
import websearch
import pagegenerator
import audiogen
import time
import re

stopwords = ["a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along",  "yet", "you", "young", "younger", "youngest", "your", "yours", "z", "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", "anything", "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", "before", "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", "came", "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", "did", "differ", "different", "differently", "do", "does", "done", "down", "downed", "downing", "downs", "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts", "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further", "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in", "interest", "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps", "kind", 'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man',
             'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible', 'present', 'presented', 'presentin', 'presents', 'problem', 'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way,' 'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', "year", "years"]
app = Flask(__name__)
CORS(app)

subscription_key = "8357f85f67e347139e320820290c4bd0"
client = ImageSearchClient(
    endpoint="https://api.cognitive.microsoft.com",
    credentials=CognitiveServicesCredentials(subscription_key))


def is_substr(text, e_map):
    for key in e_map:
        if text in key:
            return True
    return False


def search_image(search_term):

    image_results = client.images.search(query=search_term)

    if image_results.value:
        first_image_result = image_results.value[0]
        print("Total number of returned: {}".format(len(image_results.value)))
        print("First image thumbnail url: {}".format(
            first_image_result.thumbnail_url))
        print("First image content url: {}".format(
            first_image_result.content_url))
        return first_image_result.thumbnail_url
    else:
        print("No image results returned!")
        return 'NA'


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/generate")
def generate_rich_book():
    input_text = request.args.get('text')
    print("Received text: ")
    print(input_text)

    # input_file = File_object = open(r"mydoc.txt","r")
    # input_text = File_object.readlines()
    # input_text = readableText

    page = '<p>'

    entity_map = {}
    entity_web_map = {}

    session = boto3.Session(
        aws_access_key_id='AKIAYFU3DBC6GP6IFQGL',
        aws_secret_access_key='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',
    )

    comp_client = session.client('comprehend', 'us-east-1')

    # Tokenizer
    my_list = []
    for word in input_text.split(" "):
        my_list.append(word)
    for item in my_list:
        if item in stopwords:
            my_list.remove(item)

    print("LIST: ", my_list)

    response = comp_client.detect_entities(
        Text=input_text,
        LanguageCode='en'
    )  # response returns a dictionary, response['Entities']=list
    # response = my_list

    print("RESPONSE: ", response)
    print()

    # response = dict()
    # for item in my_list:
    #   response['Entities'] = ['Text']

    audiogen.gen_audio(input_text)

    print("Getting images ... ")
    for entity in response['Entities']:
        print(entity['Text'])
        if entity['Text'] not in entity_map and not is_substr(entity['Text'], entity_map):
            try:
                # imageUrl = imagesearch.imagesearch(entity['Text'])
                print("getting images")
                imageUrl = search_image(entity['Text'])
                print("image url", imageUrl)
                entity_map.update({entity['Text']: str(imageUrl)})
            except:
                print("oof")
                entity_map.update({entity['Text']: "https://duckduckgo.com/?q=" +
                                   entity['Text'] + '&va=z&t=hk&iax=images&ia=images'})

    print("Getting web pages ... ")
    for entity in response['Entities']:
        print(entity['Text'])
        if entity['Text'] not in entity_web_map and not is_substr(entity['Text'], entity_web_map):
            try:
                url = websearch.websearch(entity['Text'])
                entity_web_map.update({entity['Text']: str(url)})
            except:
                print("oof")
                entity_web_map.update(
                    {entity['Text']: "https://en.wikipedia.org/wiki/" + entity['Text']})

    # print("my image map")
    # print(entity_map)

    # print("my web map")
    # print(entity_web_map)

    a = len(entity_map)

    for entity in entity_map:
        print("\n Replacing: " + entity + "\n")
        # input_text = input_text.replace(entity, '<a href="' + entity_map[entity] + '">' + entity + '</a>')
        input_text = input_text.replace(entity, '<a class="tooltip" href="' + entity_web_map[entity] + '">' + entity + '<span' +
                                        ' class="tooltiptext"><img src = "' + entity_map[entity] + '" style="width: 50%; height: 50%"></img></span></a>')

    page = page + input_text + '</p></div></body></html>'

    head_file = open('book_home/index_head.html', 'r')
    # Save the page into a file
    print(page)
    return page
    # h_file = open('book_home/index_' + str(int(time.time())) + '.html', 'w')
    # h_file.write(head_file.read())
    # h_file.write(page)

    # h_file.close()


@app.route("/audio")
def provide_audio():
    print("sending audio")
    return send_from_directory('book_home', 'bookaudio.mp3')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    # r.headers['Cache-Control'] = 'public, max-age=0'
    return r


app.run(host='0.0.0.0')
