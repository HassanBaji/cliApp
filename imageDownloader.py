import argparse
import requests
import os

UNSPLASH_API_BASE_URL = 'https://api.unsplash.com/'
ACCESS_KEY = 'OrFM6VKyDAgMYdiLRM2Gc2pfVshoHFe-1GIZVW1rGdA'

def fetch_image(topic, orientation):
    url = f'{UNSPLASH_API_BASE_URL}photos/random'
    headers = {
        'Accept-Version': 'v1',
        'Authorization': f'Client-ID {ACCESS_KEY}'
    }
    params = {
        'query': topic,
        'orientation': orientation
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['raw']
        image_id = data['id']
        
        response = requests.get(image_url, stream=True)
        
        if response.status_code == 200:
            file_path = f'{image_id}.jpg'
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                    
            print(f'Image downloaded and saved as {file_path}')
        else:
            print('Error downloading image')
    else:
        print('Error fetching image from Unsplash')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch and store images from Unsplash API')
    parser.add_argument('topics', nargs='+', help='topics to search for')
    parser.add_argument('--orientation', default='landscape', choices=['landscape', 'portrait', 'squarish'],
                        help='image orientation (default: landscape)')
    
    args = parser.parse_args()
    
    for topic in args.topics:
        fetch_image(topic, args.orientation)
