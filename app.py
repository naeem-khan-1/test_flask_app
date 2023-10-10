from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

openai.api_key = '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'
def extract_text_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find and extract the main textual content
        main_content = soup.get_text()
        return main_content
    except Exception as e:
        return str(e)

# Function to generate Instagram post content using ChatGPT
def generate_instagram_content(text_content):
    try:
        prompt = f"Create an Instagram post content using the following text: '{text_content}'"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50  # Adjust the max tokens as needed for your content length
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/crawl', methods=['POST'])
def crawl_and_generate_content():
    url = request.form['url']
    extracted_content = extract_text_from_url(url)

    if extracted_content:
        instagram_content = generate_instagram_content(extracted_content)
        return f"Generated Instagram Post Content: {instagram_content}"
    else:
        return "Failed to extract content from the provided URL."

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))