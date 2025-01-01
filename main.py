from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os

# Define the scopes needed by the app
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

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

def get_live_videos(youtube, channel_id):
    """
    Fetches live videos from a given channel.
    """
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            eventType="live",
            type="video",
            maxResults=50
        )
        response = request.execute()
        return [item['id']['videoId'] for item in response.get('items', [])]
    except Exception as e:
        print(f"Error fetching live videos for channel {channel_id}: {e}")
        return []

def add_video_to_playlist(youtube, playlist_id, video_id):
    """
    Adds a video to a specified playlist.
    """
    try:
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
        print(f"Successfully added video {video_id} to playlist.")
        return response
    except Exception as e:
        print(f"Error adding video {video_id} to playlist: {e}")
        return None

def main():
    """
    Main function to fetch live videos from channels and add them to a playlist.
    """
    # Set credentials from the JSON key file
    creds = None
    if os.path.exists('credentials.json'):
        creds = Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)

    # Use the credentials to build the API client
    youtube = build('youtube', 'v3', credentials=creds)

    # Iterate through each channel and add live videos to the playlist
    for channel_id in CHANNEL_IDS:
        print(f"Checking live videos for channel: {channel_id}")
        live_videos = get_live_videos(youtube, channel_id)
        for video_id in live_videos:
            add_video_to_playlist(youtube, PLAYLIST_ID, video_id)

if __name__ == "__main__":
    main()
