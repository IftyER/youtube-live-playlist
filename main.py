import os
from googleapiclient.discovery import build

# Fetch sensitive information from environment variables
API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")

# Validate environment variables
if not API_KEY or not PLAYLIST_ID:
    raise ValueError("YOUTUBE_API_KEY and PLAYLIST_ID must be set as environment variables.")

# Example channel IDs
CHANNEL_IDS = ["UCt8llfhkf9LRzjTEnbG2qnQ", "UCb2O5Uo4a26CdTE7_2QA-jA"]

def get_live_videos(youtube, channel_id):
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
    youtube = build("youtube", "v3", developerKey=API_KEY)

    for channel_id in CHANNEL_IDS:
        print(f"Checking live videos for channel: {channel_id}")
        live_videos = get_live_videos(youtube, channel_id)
        for video_id in live_videos:
            add_video_to_playlist(youtube, PLAYLIST_ID, video_id)

if __name__ == "__main__":
    main()
