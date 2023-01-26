import os
src_path = os.path.dirname(__file__)

SaveLocation = src_path+'\VODs'                          #VOD storage location
TwitchID = ''                                            #Twitch Client ID
TwitchSecret = ''                                        #Twitch Client Secret
ChannelName=''                                           #Twitch Channel Name
Automatic = True           #While set to true, the program will attempt to download new vods every 24 hours
