from pytube import Playlist, YouTube

def convert_views(views):
    # Convert views count into a more readable format (k for thousands, m for millions, b for billions)
    views = int(views)
    if views >= 1_000_000_000:
        return f"{views / 1_000_000_000:.2f}b"
    elif views >= 1_000_000:
        return f"{views / 1_000_000:.2f}m"
    elif views >= 1_000:
        return f"{views / 1_000:.2f}k"
    else:
        return f"{views}"

def format_duration(duration_seconds):
    # Convert duration from seconds to a more readable format (e.g., 3.38m for minutes, 2h 15m for hours and minutes)
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes:02}m"
    else:
        return f"{minutes}.{seconds:02}m"

def get_video_info(yt):
    # Get various information about the video
    title = yt.title
    duration_seconds = yt.length  # Duration in seconds
    views = convert_views(yt.views)
    author = yt.author
    publish_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else "Unknown"
    
    return {
        "Title": title,
        "Duration": format_duration(duration_seconds),
        "Views": views,
        "Author": author,
        "Publish Date": publish_date
    }

def get_video_size(yt, resolution):
    # Try to find the specified resolution stream
    stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
    
    if stream:
        return stream.filesize / (1024 * 1024)  # Convert bytes to megabytes
    else:
        # If specified resolution is not found, get the highest resolution available
        highest_res_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if highest_res_stream:
            return highest_res_stream.filesize / (1024 * 1024)
        else:
            return 0  # Return 0 if no mp4 streams are found

def get_playlist_video_info(playlist_url, resolution='720p'):
    playlist = Playlist(playlist_url)
    video_info_list = []
    total_size_bytes_specific = 0
    total_size_bytes_all = 0
    
    for video_url in playlist.video_urls:
        yt = YouTube(video_url)
        
        # Get detailed information about the video
        video_info = get_video_info(yt)
        
        # Calculate size for specific resolution
        size_mb_specific = get_video_size(yt, resolution)
        if size_mb_specific > 0:
            total_size_bytes_specific += size_mb_specific * (1024 * 1024)  # Convert MB back to bytes for total calculation
        
        # Calculate size for all streams (highest available resolution)
        highest_res_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if highest_res_stream:
            total_size_bytes_all += highest_res_stream.filesize
        
        # Add video info to list
        video_info["File Size (MB)"] = size_mb_specific if size_mb_specific > 0 else "Not Available"
        video_info_list.append(video_info)
    
    total_size_mb_specific = total_size_bytes_specific / (1024 * 1024)  # Total size for specific resolution in megabytes
    total_size_mb_all = total_size_bytes_all / (1024 * 1024)  # Total size for all videos in megabytes
    
    # Print table header
    print("\nVideo Information:")
    print("{:<50} {:<15} {:<10} {:<20} {:<15} {:<15}".format("Title", "Duration", "Views", "Author", "Publish Date", "File Size (MB)"))
    print("-" * 125)
    
    # Print each video's information in a structured format
    for video_info in video_info_list:
        print("{:<50} {:<15} {:<10} {:<20} {:<15} {:<15}".format(
            video_info["Title"][:50], video_info["Duration"], video_info["Views"], video_info["Author"][:20],
            video_info["Publish Date"], video_info["File Size (MB)"]))
    
    print("-" * 125)
    print(f"Total Size of {resolution} streams in Playlist: {total_size_mb_specific:.2f} MB")
    print(f"Total Size of all streams (highest available resolution) in Playlist: {total_size_mb_all:.2f} MB")

# Example usage:
if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    resolution = input("Enter the resolution (e.g., 720p, 1080p): ")
    get_playlist_video_info(playlist_url, resolution)
