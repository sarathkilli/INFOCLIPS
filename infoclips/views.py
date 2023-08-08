from django.http import HttpResponseRedirect
from django.shortcuts import render
import re
from .forms import UrlForm, SearchForm, TextForm
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import youtube_transcript_api
import re
import json
from gensim.summarization import summarize
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import openai
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize




def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_name(request):
    summ = ""
    test = []
    global in_url

    # if this is a POST request we need to process the form data
    form1 = UrlForm(request.POST or None)
    form2 = SearchForm(request.POST or None)

    if request.method == "POST":
        if 'form1-submit' in request.POST:
            if form1.is_valid():
                in_url = form1.cleaned_data.get('url')
                match = re.search(r'(?<=v=)[\w-]+', in_url)
                if match:
                    video_id = match.group()
                    createfile(video_id)
                    # summ = testi(video_id)

        # if 'form2-submit' in request.POST:
        #     if form2.is_valid():
        #         in_key = form2.cleaned_data.get('search')
        #         key_seq = search(in_key)
        #         key_seq = [str(i) for i in key_seq]
        #         test = key_seq

    context = {
        'form1': form1,
        'form2': form2,
        'output_data': summ,
        'test_data': test,
    }
    return render(request, 'home.html', context)


def get_summy(request):
    form5 = TextForm(request.POST or None)
    summ = ""
    if request.method == "POST":
        if 'form5-submit' in request.POST:
            if form5.is_valid():
                text = form5.cleaned_data.get('text')
                summ = summy(text)
        
    context = {
        'form5' : form5,
        'output_data' : summ
    }
    return render(request, 'summy.html', context)


def get_team(request):
    return render(request, 'team.html')



def get_text(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract the transcript text from the transcript
    transcript_text = ""
    for segment in transcript:
        transcript_text += " " + segment["text"]

    # Summarize the transcript using Gensim
    return transcript_text


def testi(video_id):

    prompt = "summarize the following: " + get_text(video_id)
    model = "text-davinci-002"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100
    )

    answer = response.choices[0].text.strip()
    return answer

    # summary = summarize(get_text(video_id))
    # return summary

openai.api_key = ""#yourApikey

def summy(text):
    prompt = "summarize the following into less than 4-5 lines: " + text
    model = "text-davinci-002"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100
    )

    answer = response.choices[0].text.strip()
    return answer


def createfile(video_id):
    try:
        # get transcripts from youtube video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # format json
        formatter = JSONFormatter()
        json_formatted = formatter.format_transcript(transcript)

        # write to json file
        with open('transcript.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_formatted)

    # for API Errors
    # print(youtube_transcript_api._errors)
    except youtube_transcript_api._errors.TranscriptsDisabled:
        print("Hello")


def search(key):
    time_sequence = []

    # open json_file
    with open('transcript.json') as json_file:
        data = json.load(json_file)

    # search key
    for i in data:
        if key in i["text"]:
            time_sequence.append(i["start"])

    return time_sequence


def ajax_summary(request):
    if is_ajax(request=request):
        url = request.POST.get('id_url', None)
        url_id = get_id(url)
        # output = testi(url_id)
        # output = testi((get_text(url_id)))
        output = test_summary(testi(url_id))
        response = {
            'msg': output
        }
        return JsonResponse(response)


def ajax_search(request):
    if is_ajax(request=request):
        key = request.POST.get('id_search', None)

        output = search(key)

        response = {

            'msg': output
        }

        return JsonResponse(response)


def ajax_sentiment(request):
    if is_ajax(request=request):
        url = request.POST.get('id_url', None)
        url_id = get_id(url)
        result = sentiment(get_text(url_id))
        p_label = "Positive"
        p_output = result

        response = {
            'label': p_label,
            'score': p_output
        }

        return JsonResponse(response)


def get_id(url):
    # url = "https://www.youtube.com/watch?v=9QiE-M1LrZk&ab_channel=BetterThanYesterday"

    # regex to get id
    match = re.search(r'(?<=v=)[\w-]+', url)
    # outputs <re.Match object; span=(32, 43), match='9QiE-M1LrZk'>

    if match:
        video_id = match.group()
        # print(video_id)
        return video_id


def sentiment(paragraph):

    # Create a sentiment analyzer object
    analyzer = SentimentIntensityAnalyzer()

    # Input paragraph

    # Analyze sentiment using Vader module
    scores = analyzer.polarity_scores(paragraph)

    # Print sentiment scores
    return scores['pos']
    # print(f"Positive score: {scores['pos']}")
    # print(f"Negative score: {scores['neg']}")
    # print(f"Neutral score: {scores['neu']}")
    # print(f"Compound score: {scores['compound']}")


def test_summary(text):

    # Input your text for summarizing below:

    # Next, you need to tokenize the text:

    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Now, you will need to create a frequency table to keep a score of each word:

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Next, create a dictionary to keep the score of each sentence:

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Now, we define the average value from the original text as such:

    average = int(sumValues / len(sentenceValue))

    # And lastly, we need to store the sentences into our summary:

    summary = ''

    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary