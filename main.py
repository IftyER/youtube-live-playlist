# main.py

from googleapiclient.discovery import build
import os

# Replace with your YouTube Data API key
API_KEY = "YOUR_API_KEY"
# List of channel IDs you want to monitor
CHANNEL_IDS = [
    "UC_x5XG1OV2P6uZZ5FSM9Ttw",  # Google Developers Channel
    "UCOhHO2ICt0ti9KAh-QHvttg",  # Another Example Channel
]
# Playlist ID where live streams will be added
PLAYLIST_ID = "YOUR_PLAYLIST_ID"

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
