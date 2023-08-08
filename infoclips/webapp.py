from django.shortcuts import render
import re 

def button(request):

    return render(request,'home.html')

def output(request):
    
    output_data = "Genius Voice eliminates friction. For years people have had to learn to interact with computers, we turn this around. We teach computers how to interact with humans through voice. This creates a seamless experience without losing the human touch."
    website_link = "Visit our website: " + "https://www.geniusvoice.nl/"
    
    return render(request,"home.html",{"output_data":output_data, "website_link":website_link})

def get_id(request):
    url = "https://www.youtube.com/watch?v=9QiE-M1LrZk&ab_channel=BetterThanYesterday"

    # regex to get id
    match = re.search(r'(?<=v=)[\w-]+', url)
    # outputs <re.Match object; span=(32, 43), match='9QiE-M1LrZk'>

    if match:
        video_id = match.group()
        # print(video_id)
        return render(request,"home.html",{"output_data":video_id})