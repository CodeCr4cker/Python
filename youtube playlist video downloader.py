import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please install it using: pip install yt-dlp")
    sys.exit(1)


def download_playlist(playlist_url, download_path="downloads", video_quality="best"):
    """
    Download a YouTube playlist
    
    Args:
        playlist_url: URL of the YouTube playlist
        download_path: Directory where videos will be saved
        video_quality: Quality of video ('best', 'worst', or specific format)
    """
    
    # Create download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        print(f"Created directory: {download_path}")
    
    # Configure download options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Best quality video and audio
        'outtmpl': os.path.join(download_path, '%(playlist_index)s - %(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,  # Continue on download errors
        'progress_hooks': [progress_hook],
    }
    
    # If user wants audio only
    if video_quality == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nFetching playlist information...")
            info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in info:
                print(f"\nPlaylist: {info.get('title', 'Unknown')}")
                print(f"Total videos: {len(info['entries'])}")
                print(f"Download location: {os.path.abspath(download_path)}\n")
                
                # Confirm download
                confirm = input("Start downloading? (y/n): ").lower()
                if confirm != 'y':
                    print("Download cancelled.")
                    return
                
                print("\nStarting download...\n")
                ydl.download([playlist_url])
                print("\n✓ Playlist download completed!")
            else:
                print("Error: Could not fetch playlist information.")
                
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("Please check the playlist URL and try again.")


def progress_hook(d):
    """Display download progress"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print(f"\n✓ Downloaded: {d['filename']}")


def main():
    print("=" * 60)
    print("YouTube Playlist Downloader")
    print("=" * 60)
    
    # Get playlist URL from user
    playlist_url = input("\nEnter YouTube playlist URL: ").strip()
    
    if not playlist_url:
        print("Error: No URL provided.")
        return
    
    # Get download location
    download_path = input("Enter download folder (press Enter for 'downloads'): ").strip()
    if not download_path:
        download_path = "downloads"
    
    # Get quality preference
    print("\nQuality options:")
    print("1. Best quality (video + audio)")
    print("2. Audio only (MP3)")
    
    choice = input("Select option (1 or 2): ").strip()
    
    video_quality = "best" if choice == "1" else "audio"
    
    # Start download
    download_playlist(playlist_url, download_path, video_quality)


if __name__ == "__main__":
    main()