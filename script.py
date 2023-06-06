import googleapiclient.discovery
import csv
import re


api_key = str(input())
url = str(input())
max_comments =int(input())
output_file = "comments.csv"

match = re.search(r"watch\?v=(\w+)", url)
if match:
    video_id = match.group(1)
else:
    print("Aucun code vidéo trouvé.")


def extract_comments(api_key, video_id, max_comments):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments - len(comments), 100),
            textFormat="plainText",
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        next_page_token = response.get("nextPageToken", None)
        if next_page_token is None:
            break

    return comments

def save_comments_to_csv(comments, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Comment'])
        for comment in comments:
            csvwriter.writerow([comment])


comments = extract_comments(api_key, video_id, max_comments)
save_comments_to_csv(comments, output_file)
print(f"Comments saved to {output_file}")

