from flask import Flask
from flask import render_template
from random import randint
import googleapiclient.discovery

app = Flask(__name__)

@app.route('/')

def random_vid_from_playlist():
###google api requirements
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyC6xrU74ONYT7SiOOFf7z5mNLZVAGFpsL0"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
###

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
### TODO: implement multiple page search so that more than 50 results
    ### can be returned.
    response = request.execute()
    for item in response['items']:
        video_ids.append(item['snippet']['resourceId']['videoId'])
    
    random_vid_id = video_ids[randint(0, len(video_ids))]
 ###

  # num_values = len(video_ids)
  # video_id = video_ids[randint(0, num_values)]

  #render_template('index.html', video_id = video_id)
    return render_template('index.html', video_id = random_vid_id)

if __name__ == '__main__':
    app.run(debug=False)
