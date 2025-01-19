from flask import Flask, render_template, request, redirect, url_for
import requests
import cohere
import os

app = Flask(__name__)


cohere_api_key = "LbRuj1xVbMG26WTND3gbG3MwqpRx2hH7v5Uzkjw3"  # Replace with your Cohere API key
co = cohere.ClientV2(cohere_api_key)

# Wikipedia API URL for summary
WIKI_SUMMARY_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

@app.route('/')
def index():
    """Home page with a search form."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Fetch Wikipedia page and generate AI summary."""
    topic = request.form.get('topic')
    if not topic:
        return redirect(url_for('index'))

    
    response = requests.get(WIKI_SUMMARY_API_URL + topic)
    if response.status_code == 200:
        data = response.json()
        page_content = data.get('extract', '')

    
        if not page_content:
            return render_template('flashcard.html', title=topic, summary=["No content found."])

        summary = summarize_with_cohere(page_content)

 
        if isinstance(summary, str):
            summary = summary.split('\n') 

        
        summary = summary[:3]

        return render_template('flashcard.html', title=topic, summary=summary)
    else:
        return render_template('flashcard.html', title="Error", summary=["Topic not found."])

def summarize_with_cohere(text):
    """Summarize text using Cohere API."""
    message = f"Generate a concise summary of this text in 10 sentences divided into 3 paragraphs\n{text}"

    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": message}],
    )

    
    summary = response.message.content[0].text
    return summary

if __name__ == '__main__':
    app.run(debug=True)
