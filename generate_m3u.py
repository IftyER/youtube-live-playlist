import subprocess

def extract_m3u8_url(youtube_url, cookies_file="cookies.json"):
    """Extract the M3U8 URL for a given YouTube live stream using yt-dlp."""
    try:
        # Use yt-dlp to get the best m3u8 URL
        result = subprocess.run(
            [
                "yt-dlp",
                "--cookies", cookies_file,
                "-g", 
                "-f", "bestaudio/best",
                youtube_url
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract URL: {youtube_url}")
        print(e.stderr)
        return None

def generate_m3u_playlist(youtube_urls, cookies_file="cookies.json"):
    """Generate an M3U playlist from a list of YouTube live URLs."""
    m3u_playlist = "#EXTM3U\n"
    
    for index, url in enumerate(youtube_urls, 1):
        print(f"Extracting stream for: {url}")
        m3u8_url = extract_m3u8_url(url, cookies_file)
        if m3u8_url:
            m3u_playlist += f"#EXTINF:-1,Stream {index} - {url}\n{m3u8_url}\n"
        else:
            print(f"Error: Could not extract M3U8 URL from {url}")
    
    return m3u_playlist

def save_m3u_playlist(playlist_content, filename="playlist.m3u"):
    """Save the generated M3U playlist to a file."""
    with open(filename, "w") as file:
        file.write(playlist_content)

def main():
    # Replace this list with your actual YouTube live URLs
    youtube_urls = [
        "https://www.youtube.com/@somoynews360/live",
        "https://www.youtube.com/@JamunaTVbd/live",
        "https://www.youtube.com/@channel24digital/live",
        "https://www.youtube.com/@dbcnewstv/live",
        "https://www.youtube.com/@ATNNews24/live",
        "https://www.youtube.com/@ChanneliNews/live",
        "https://www.youtube.com/@IndependentTelevision/live",
        "https://www.youtube.com/@EkattorTelevision/live",
        "https://www.youtube.com/@RtvNews/live",
        "https://www.youtube.com/@ekhontv/live",
        "https://www.youtube.com/@news24television90/live",
        "https://www.youtube.com/@NTVDigitalLive/live",
        "https://www.youtube.com/@livedeshtv/live"
    ]
    
    # Generate M3U playlist
    playlist_content = generate_m3u_playlist(youtube_urls)
    
    # Save playlist to a file
    save_m3u_playlist(playlist_content)

if __name__ == "__main__":
    main()
