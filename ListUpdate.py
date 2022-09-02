import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import os

f = open("List.json","w")
list = []
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def sort(videolist):
    length = len(videolist)
    sorted = []

    for i in range(length):
        item = videolist[i]
        title = item['snippet']['title']
        id = item['contentDetails']['videoId']
        sorted.append(i)
        l  = []
        l.append(title)
        l.append(id)
        sorted.append(l)

    return sorted


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def getlist():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.apps.googleusercontent.com.json"
    print(client_secrets_file)

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()

    uploadsid = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    print("Playlist ID : " + uploadsid)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=200,
        playlistId=uploadsid
    )
    response2 = request.execute()

    videos = response2['items']
    print(videos)
    return videos

d = getlist()
d = sort(d)
d = Convert(d)
j = json.dumps(d, indent=4)
print(j)

f.write(j)


