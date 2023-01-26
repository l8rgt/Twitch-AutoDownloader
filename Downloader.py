import requests
import json
import streamlink
from moviepy.editor import VideoFileClip
from datetime import timedelta, datetime
from pathlib import Path
import shutil
import os

from index import TwitchID
from index import TwitchSecret
from index import ChannelName
from index import Automatic

src_path = os.path.dirname(__file__)
trg_path = src_path+'\VODs'

def downloader():
    response = requests.post('https://id.twitch.tv/oauth2/token', data={
        'client_id': TwitchID,
        'client_secret': TwitchSecret,
        'grant_type': 'client_credentials'
    })

    response_json = response.json()
    access_token = response_json['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': TwitchID
    }

    getuser = requests.get('https://api.twitch.tv/helix/users', params={
            'login': ChannelName
        }, headers=headers)

    getUser_json = getuser.json()
    user = getUser_json['data'][0]
    channelID = user['id']

    VODList = requests.get('https://api.twitch.tv/helix/videos', params={
                'user_id': channelID,
                'type': 'archive'
            }, headers=headers)

    VODList_json=VODList.json()
    TotalNum=0
    VODNum=0
    VODList_Data=VODList_json['data']
    #print(VODList_Data)
    for VOD in VODList_Data:
        TotalNum+=1
    #print(TotalNum)
    IDList=json.load(open('Downloaded.json','r'))
    Incompat=['\\','/',':','*','?','"','<','>','|']
    New=False
    while VODNum<TotalNum:
        Download=True
        test=False
        VOD_Data=VODList_json['data'][VODNum]
        VOD_title=VOD_Data['title']
        VOD_URL=VOD_Data['url']
        VOD_ID=VOD_Data['id']
        for ID in IDList:
            if VOD_ID==ID:
                Download=False
                break
        if Download:
            New=True
            for symbol in Incompat:
                    cleansedTitle=VOD_title.replace(symbol," ")
            if test:
                print(VOD_title)
                print(cleansedTitle)
                print(VOD_URL)
            else:
                stream_url = streamlink.streams(VOD_URL)['best'].url
                clip = VideoFileClip(stream_url)
                clip.write_videofile(cleansedTitle+"_"+VOD_ID+".mp4")
                clip.close()
                for src_file in Path(src_path).glob('*.mp4'):
                    shutil.move(src_file, trg_path)
            IDList.append(VOD_ID) 
        VODNum+=1
    with open('Downloaded.json','w') as i:
        json.dump(IDList,i)
    if New:
        print("All new VODs have been downloaded!")
    else:
        if Automatic:
            print("No new VODs found. Checking again in 24 hours")
        else:
            print("No new VODs found.")

downloader()
CurrTime=datetime.now()
while Automatic:
    StartTime = datetime.now()
    OneDay = timedelta(hours=24)
    print(str(StartTime+OneDay)[:-6])

    while str(CurrTime)[:-6]!=str(StartTime+OneDay)[:-6]:
        CurrTime = datetime.now()
    print("24 hours have passed since last check! Checking for new VODs...")
    downloader()
