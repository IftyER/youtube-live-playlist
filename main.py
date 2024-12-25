# main.py

from googleapiclient.discovery import build
import os

# Replace with your YouTube Data API key
API_KEY = "AIzaSyCCEdOKSh_Axvs5qF87xtjWVvAmCGysc6U"
# List of channel IDs you want to monitor
CHANNEL_IDS = [
    "UCt8llfhkf9LRzjTEnbG2qnQ",  # Channel 1
    "UCb2O5Uo4a26CdTE7_2QA-jA",  # Channel 2
    "UCHLqIOMPk20w-6cFgkA90jw",  # Channel 3
    "UC0V3IJCnr6ZNjB9t_GLhFFA",  # Channel 4
    "UCWVqdPTigfQ-cSNwG7O9MeA",  # Channel 5
    "UC2P5Fd5g41Gtdqf0Uzh8Qaw",  # Channel 6
    "UCxHoBXkY88Tb8z1Ssj6CWsQ",  # Channel 7
    "UCN6sm8iHiPd0cnoUardDAnw",  # Channel 8
    "UCtqvtAVmad5zywaziN6CbfA",  # Channel 9
    "UCUvXoiDEKI8VZJrr58g4VAw",  # Channel 10
    "UC8NcXMG3A3f2aFQyGTpSNww",  # Channel 11
    "UCmCCTsDl-eCKw91shC7ZmMw",  # Channel 12
    "UCATUkaOHwO9EP_W87zCiPbA",  # Channel 13
]
# Playlist ID where live streams will be added
PLAYLIST_ID = "PLhDI33oYisToytKQ-gNFqG9Mx4XmOCmNA"

def get_live_videos(api_key, channel_id):
    """
    Fetches live videos from a given channel.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="live",
        type="video",
        maxResults=50
    )
    response = request.execute()
    return [item['id']['videoId'] for item in response.get('items', [])]

def add_video_to_playlist(api_key, playlist_id, video_id):
    """
    Adds a video to a specified playlist.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

def main():
    """
    Main function to fetch live videos from channels and add them to a playlist.
    """
    for channel_id in CHANNEL_IDS:
        live_videos = get_live_videos(API_KEY, channel_id)
        for video_id in live_videos:
            try:
                print(f"Adding video {video_id} to playlist {PLAYLIST_ID}")
                response = add_video_to_playlist(API_KEY, PLAYLIST_ID, video_id)
                print("Added successfully:", response)
            except Exception as e:
                print(f"Failed to add video {video_id}: {e}")

if __name__ == "__main__":
    main()

