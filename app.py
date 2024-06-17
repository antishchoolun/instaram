from flask import Flask, jsonify, send_file
import subprocess
import base64
import os
import io

app = Flask(__name__)

def download_instagram_image(profile_id):
    try:
        # Full path to instaloader executable (adjust if needed)
        instaloader_path = 'instaloader'  # Assuming instaloader is in the PATH
        
        # Directory where instaloader will download the image
        download_directory = f'-{profile_id}'
        
        # Construct the command to download the image
        command = [instaloader_path, '--', f'-{profile_id}']
        
        # Run the command
        result = subprocess.run(command, capture_output=True)
        
        # Check for errors
        if result.returncode == 0:
            print(f"Image with profile ID '{profile_id}' downloaded successfully.")
            
            # Find the downloaded image file
            image_path = find_downloaded_image(download_directory)
            
            if image_path:
                return image_path
            else:
                print(f"No image file found in directory '{download_directory}'.")
                return None
        else:
            print(f"Failed to download image. Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def find_downloaded_image(directory):
    # Function to find the downloaded image file in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg'):
                return os.path.join(root, file)
    return None

@app.route('/')
def hello():
    profile_id = 'C8Ad5VAJWCQ'  # Replace with your desired profile ID
    downloaded_image_path = download_instagram_image(profile_id)
    if downloaded_image_path:
        # Return the downloaded image file
        return send_file(downloaded_image_path, mimetype='image/jpeg')
    else:
        return "Failed to download image."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
