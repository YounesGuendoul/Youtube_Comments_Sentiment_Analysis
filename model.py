from transformers import pipeline
import pandas as pd
import re
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

def remove_combining_chars(text):
    # Remove combining characters using the 'Mn' (Mark, Nonspacing) category
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

# Define a function to clean the text
def clean_text(text):
    # Remove combining characters
    cleaned_text = remove_combining_chars(text)
    # Remove all non-alphanumeric characters
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_text)
    return cleaned_text

def get_emotion_label(text):
      return(emotion(text)[0]['label'])   

# Assuming your dataset has a column named 'text_column' containing the text entries
# Replace 'text_column' with the name of the column you want to clean

stop_words = set(stopwords.words('english'))

def cleanyoutube(youtubeText):
    youtubeText =re.sub(pattern='http\S+\s*', repl=' ', string=youtubeText) # URLs
    youtubeText = re.sub(pattern='RT|cc', repl=' ', string=youtubeText)  # remove RT and cc
    youtubeText = re.sub(pattern='@\S+', repl=' ', string=youtubeText) # hashtags
    youtubeText = re.sub('@S+', '  ', youtubeText)  # mentions
    youtubeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), repl=' ', string=youtubeText) # punctuations
    youtubeText = re.sub(r'[^\x00-\x7f]',r' ', youtubeText) # numbers
    youtubeText = re.sub('\s+', ' ', youtubeText) # extra whitespace
    youtubeText = youtubeText.lower()
    words = word_tokenize(youtubeText)
    filtered_sentence = [w for w in words if not w in stop_words]
    youtubeText = ' '.join(filtered_sentence)
    return youtubeText

file = "comments.csv"
def emotion_preponderante(file):
    df = pd.read_csv("comments.csv")
    df['Comment']=df['Comment'].astype(str)
    df['cleaned_text'] = df['Comment'].apply(clean_text)
    df['cleanedyoutube'] = df['Comment'].apply(lambda tweet:cleanyoutube(tweet))  
    df['emotion']=df['cleanedyoutube'].apply(get_emotion_label)
    freq = df['emotion'].value_counts(ascending=False).rename_axis('unique_values').reset_index(name='counts')
    freq = pd.DataFrame(freq)
    return freq['unique_values'][1]    



