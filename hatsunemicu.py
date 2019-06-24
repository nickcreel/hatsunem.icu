from flask import Flask
from flask import render_template
from random import randint
import googleapiclient.discovery
from os import listdir

app = Flask(__name__)
    
@app.route('/')

def random_vid_from_playlist():
###google api requirements
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = #<insert developer key here>
    youtube = googleapiclient.discovery.build(api_service_name, api_version,
              developerKey = DEVELOPER_KEY)


### playlist and video ids from playlist -> fetching using google dev api    
    playlist_id = "PL4b75VzKmiVO3Kt-0pbZ_kvpxKRKdmNZD"
    video_ids = []
### playlistItems.list returns a googleapiclient.http.HttpRequest object
### see spec at https://github.com/googleapis/google-api-python-client
### /blob/master/docs/epy/googleapiclient.http.HttpRequest-class.html
### basics: an http request must be executed using the .execute() method. 
### it makes more sense to assign the request to a variable, then execute.

    request = youtube.playlistItems().list(part = "snippet", playlistId =
        playlist_id, maxResults = 50)
    response = request.execute()
    nextPageToken = response.get('nextPageToken')
    nextpage = None

### see https://stackoverflow.com/questions/18804904/retrieve-all-
### videos-from-youtube-playlist-using-youtube-v3-api for details on
### how to retrieve all results from playlist using nextPageToken.
### thank you stanzheng!

    while 'nextPageToken' in response:
        nextpage  = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 50, 
        pageToken = nextPageToken)
        nextres = nextpage.execute()
        
        response['items'] = response['items'] + nextres['items']

        if 'nextPageToken' not in nextres:
            response.pop('nextPageToken', None)
        else:
            nextPageToken = nextres['nextPageToken']
   
    for item in response['items']:
        video_ids.append(item['snippet']['resourceId']['videoId'])
    random_vid_id = video_ids[randint(0, len(video_ids))]

    return render_template('index.html', video_id = random_vid_id)

if __name__ == '__main__':
    app.run(debug=False)
