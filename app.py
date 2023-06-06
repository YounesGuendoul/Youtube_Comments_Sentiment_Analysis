from flask import Flask, request, render_template
import csv
from googleapiclient.discovery import build
import googleapiclient.errors
from model import emotion_preponderante

app = Flask(__name__)


# Define the route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for form submission
@app.route('/process', methods=['POST'])
def process():
    # Get form data
    url = request.form['url']
    num_comments = int(request.form['num_comments'])
    api_key = request.form['api_key']

    # Extract video ID from the URL
    video_id = url.split('v=')[1]

    # Initialize the YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        # Retrieve comments for the video
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=num_comments
        ).execute()

        # Save comments to a CSV file
        with open('comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Author', 'Comment'])
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                writer.writerow([author, comment])

        message = 'Comments saved successfully!'
    except googleapiclient.errors.HttpError as e:
        message = f'An error occurred: {e}'
    dominant_emotion = emotion_preponderante("comments.csv")
    
    return render_template('result.html', message=message,dominant_emotion=dominant_emotion)

if __name__ == '__main__':
    app.run(debug=True)
