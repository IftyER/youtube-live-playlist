import os
import subprocess
import shutil

# Define the YouTube Live URLs
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

# Output M3U file path (this will be saved in the repository directory)
output_file = "playlist.m3u"

def extract_m3u8_links(youtube_urls):
    """Extracts .m3u8 links from YouTube Live URLs."""
    m3u8_links = []
    for url in youtube_urls:
        try:
            print(f"Extracting stream for: {url}")
            command = ["yt-dlp", "--cookies", "cookies.txt", "-g", url]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                m3u8_links.append(result.stdout.strip())
            else:
                print(f"Failed to extract URL: {url}\n{result.stderr}")
        except Exception as e:
            print(f"Error extracting URL {url}: {e}")
    return m3u8_links

def generate_m3u_file(m3u8_links, output_file):
    """Generates the #EXTM3U file."""
    with open(output_file, "w") as f:
        f.write("#EXTM3U\n")
        for i, link in enumerate(m3u8_links, start=1):
            f.write(f'#EXTINF:-1,YouTube Live Stream {i}\n')
            f.write(f"{link}\n")
    print(f"Playlist saved to {output_file}")

def main():
    """Main function to generate the playlist."""
    if not shutil.which("yt-dlp"):
        print("yt-dlp is not installed. Install it using `pip install yt-dlp`.") 
        return

    m3u8_links = extract_m3u8_links(youtube_urls)
    if m3u8_links:
        generate_m3u_file(m3u8_links, output_file)
    else:
        print("No .m3u8 links were extracted. Exiting.")

if __name__ == "__main__":
    main()
