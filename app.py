import instaloader
import subprocess
import os

def download_instagram_image(profile_id):
    try:
        # Dynamically set the base directory where images will be downloaded
        script_directory = os.path.dirname(os.path.abspath(__file__))
        base_directory = os.path.join(script_directory, 'downloaded')
        
        # Ensure the directory exists
        if not os.path.exists(base_directory):
            os.makedirs(base_directory)
        
        # Full path to instaloader executable (adjust if needed)
        instaloader_path = 'instaloader'  # Assuming instaloader is in the PATH

        # Construct the command with the specified base directory
        command = [instaloader_path, '--dirname-pattern', base_directory, '--', f'-{profile_id}']
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True, cwd=base_directory)
        
        # Check for errors
        if result.returncode == 0:
            print(f"Image with profile ID '{profile_id}' downloaded successfully.")
            # Find the downloaded image in the specified base directory
            images = [f for f in os.listdir(base_directory) if f.endswith('.jpg')]
            if images:
                image_path = os.path.join(base_directory, images[0])
                print(f"Downloaded image path: {image_path}")
                return image_path
            else:
                print("No image files found in the folder.")
                return None
        else:
            print(f"Failed to download image. Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    profile_id = 'C8Ad5VAJWCQ'  # Replace with your desired profile ID
    downloaded_image_path = download_instagram_image(profile_id)
