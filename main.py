import os
import base64
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def main():
    # Get environment variables
    service_account_json_base64 = os.getenv("SERVICE_ACCOUNT_JSON")
    playlist_id = os.getenv("PLAYLIST_ID")

    if not service_account_json_base64 or not playlist_id:
        print("SERVICE_ACCOUNT_JSON and PLAYLIST_ID must be set as environment variables.")
        return

    # Decode the base64-encoded service account JSON
    service_account_json = base64.b64decode(service_account_json_base64).decode('utf-8')

    # Save the decoded JSON to a file
    with open("credentials.json", "w") as f:
        f.write(service_account_json)

    # Authenticate using service account
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/youtube"])
    youtube = build("youtube", "v3", credentials=creds)

    # List of channels to monitor
    channel_ids = [
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

    # Fetch live videos and add to playlist
    for channel_id in channel_ids:
        live_videos = youtube.search().list(part="snippet", channelId=channel_id, eventType="live", type="video", maxResults=50).execute()

        for item in live_videos.get("items", []):
            video_id = item["id"]["videoId"]
            youtube.playlistItems().insert(
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
            ).execute()
            print(f"Added video {video_id} from channel {channel_id} to playlist {playlist_id}")

if __name__ == "__main__":
    main()
