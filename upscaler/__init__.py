
import requests
import time
import os

url = ""

from . import url

# Replace this URL with the public URL from ngrok
def set_url(url_):
    url = url_

def upload_video(video_path):
    # Upload the video
    with open(video_path, 'rb') as video_file:
        files = {'video': video_file}
        response = requests.post(f"{url}/upload", files=files)
        print("Upload response:", response.json())

def receive_video(output_dir):
    while True:
        response = requests.get(f"{url}/progress")
        
        # Determine if the response is JSON or a file
        content_type = response.headers.get('Content-Type')
        
        if "application/json" in content_type:
            status = response.json()
            print("Status:", status.get("status"))
            
            if status.get("status") == "Upscaling complete. Ready to download.":
                # Download the upscaled video
                video_response = requests.get(f"{url}/progress", stream=True)
                with open(output_dir, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print("Video downloaded as upscaled_video.mp4")
                break
        else:
            # If not JSON, assume it's the video file
            with open(output_dir, 'wb') as f:
                f.write(response.content)
            print("Video downloaded as upscaled_video.mp4")
            break
        
        time.sleep(10)  # Check every 10 seconds