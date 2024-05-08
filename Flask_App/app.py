from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import re
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import requests

app = Flask(__name__)

def count_words(text):
    words = re.findall(r'\w+', text)
    return len(words)

def split_text_by_words(text, chunk_size=500):
    words = re.findall(r'\w+', text)
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = ' '.join(words[start:end])
        chunks.append(chunk_text)
        start = end
    return chunks

def summarize_chunks(chunks):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    hist=''
    summary_chunks = []
    for c in chunks:
        if sum(len(chunk.split(" ")) for chunk in summary_chunks)>=800:
            summary_chunks=[]
            summary_chunks.append(clean('.'.join(summary_chunks)))
        content=hist+' '+c
        summary = summarizer(content, max_length=300, min_length=100, do_sample=False)
        summary_text = ''.join(summary[0]['summary_text'])
        hist=summary_text
        summary_chunks.append(summary_text)
    cont= '. '.join(summary_chunks)
    return clean(cont)

def clean(content):
    genai.configure(api_key='AIzaSyCmPlSpjYkUXH95-1oMRNs7QzSRFRe-A4E')
    model = genai.GenerativeModel('gemini-1.0-pro')
    def get_ans(query):    
        prompt = PromptTemplate(input_variables=["content"],template = ''' content : {content} . Remove repeating lines and give a correct and prettified content alone as a single paragraph''')
        input_prompt = prompt.format(content = query)
        output = model.generate_content(input_prompt)
        return output
    res=get_ans(content)
    return res.text

def summarize_pdf(pdf_path):
    pages = PdfReader(pdf_path)
    text = ""
    for page in pages.pages:
        text += page.extract_text()
    text = text.replace('\t', ' ')
    chunks = split_text_by_words(text)
    return summarize_chunks(chunks)

def geturl(q):
    api_key = "AIzaSyBdlN72Py11hJLSiflzzcp9MAZRv0e03pI"
    search_engine_id = "06e713d09dbd14dbc"
    query=f'Give me related links about {q} in india'
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        print("Error:", response.status_code)
        return None

def links(content):
    genai.configure(api_key='AIzaSyCmPlSpjYkUXH95-1oMRNs7QzSRFRe-A4E')
    model = genai.GenerativeModel('gemini-1.0-pro')
    prompt = PromptTemplate(input_variables=["content"],template = ''' content : {content} . Give the topic about what the content is speaking in less than 5 words.''')
    input_prompt = prompt.format(content = content)
    output = model.generate_content(input_prompt)
    q=output.text
    results=geturl(q)
    if results:
        results=[result['link'] for result in results]
        return results
    else:
        return ['Sorry buddy ! No reference available related to given content.']

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    if request.method == "POST":
        if 'file' in request.files:
            file = request.files['file']
            pdf_text = ""
            input=''
            for page in PdfReader(file).pages:
                pdf_text += page.extract_text()
                input=pdf_text
            summarized_text = summarize_chunks(split_text_by_words(pdf_text))
            urls = links(summarized_text)
            return jsonify(summarized_text=summarized_text, urls=urls,input=input)
        else:
            data = request.get_json()
            input_text=data['data']
            summarized_text = summarize_chunks(split_text_by_words(input_text))
            urls = links(summarized_text)
            return jsonify(summarized_text=summarized_text, urls=urls,input=input_text)


if __name__ == "__main__":
    app.run(debug=True)
