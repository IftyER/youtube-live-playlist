import yt_dlp

def extract_m3u8_url(url):
    """Extract M3U8 URL for a YouTube live stream using cookies."""
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'noplaylist': True,
            'cookies': 'cookies.txt',  # Path to the exported cookies file
            'extractor_args': {
                'youtube': {
                    'live': True
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            m3u8_url = info_dict.get('url', None)
            return m3u8_url
    except Exception as e:
        print(f"Failed to extract URL: {url}\nError: {e}")
        return None

def main():
    youtube_urls = [
        "https://www.youtube.com/@somoynews360/live",
        # Add other URLs here
    ]

    m3u_playlist = "#EXTM3U\n"
    for index, url in enumerate(youtube_urls, 1):
        print(f"Extracting stream for: {url}")
        m3u8_url = extract_m3u8_url(url)
        if m3u8_url:
            m3u_playlist += f"#EXTINF:-1,Stream {index}\n{m3u8_url}\n"
        else:
            print(f"Failed to extract URL: {url}")

    if m3u_playlist.strip() != "#EXTM3U":
        with open("output.m3u", "w") as file:
            file.write(m3u_playlist)
    else:
        print("No .m3u8 links were extracted. Exiting.")

if __name__ == "__main__":
    main()
