from flask import Flask, jsonify
import instaloader
import subprocess
import base64
import io
import os

app = Flask(__name__)

def download_instagram_image(profile_id):
    try:
        # Full path to instaloader executable (adjust if needed)
        instaloader_path = 'instaloader'  # Assuming instaloader is in the PATH
        
        # Use an in-memory buffer to store image data
        image_buffer = io.BytesIO()
        
        # Construct the command to download the image
        command = [instaloader_path, '-{profile_id}']
        
        # Run the command
        result = subprocess.run(command, capture_output=True)
        
        # Check for errors
        if result.returncode == 0:
            print(f"Image with profile ID '{profile_id}' downloaded successfully.")
            
            # Load the image into the buffer
            image_buffer.write(result.stdout)
            
            # Read image content from buffer
            image_buffer.seek(0)
            image_content = image_buffer.read()
            
            # Encode image content as base64
            base64_image = base64.b64encode(image_content).decode('utf-8')
            
            return base64_image
        else:
            print(f"Failed to download image. Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

@app.route('/')
def hello():
    profile_id = 'C8Ad5VAJWCQ'  # Replace with your desired profile ID
    base64_image_data = download_instagram_image(profile_id)
    if base64_image_data:
        # Return base64 image data as JSON response
        return jsonify({"image_data": base64_image_data})
    else:
        return "Failed to download image."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

