from flask import Flask, request, jsonify
import instaloader
import base64
import requests

app = Flask(__name__)

def download_instagram_image(profile_id):
    try:
        # Initialize instaloader
        loader = instaloader.Instaloader()

        # Fetch the post
        post = instaloader.Post.from_shortcode(loader.context, profile_id)

        # Download the image into memory
        image_url = post.url
        response = requests.get(image_url)
        response.raise_for_status()  # Check for request errors
        image_content = response.content

        # Encode the image content as base64
        base64_image = base64.b64encode(image_content).decode('utf-8')
        
        return base64_image
    except Exception as e:
        return str(e)

@app.route('/download_image', methods=['GET'])
def download_image():
    profile_id = request.args.get('profile_id')
    if not profile_id:
        return jsonify({"error": "profile_id is required"}), 400

    base64_image_data = download_instagram_image(profile_id)
    if base64_image_data.startswith('An error occurred'):
        return jsonify({"error": base64_image_data}), 500

    return jsonify({"base64_image_data": base64_image_data})

if __name__ == "__main__":
    app.run(debug=True)
