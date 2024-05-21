import streamlit as st
from transformers import pipeline
import re
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import requests

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
    genai.configure(api_key='YOUR_API')
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
    api_key = "YOUR_API"
    search_engine_id = "YOUR_ID"
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
    genai.configure(api_key='YOUR_API')
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

def main():
    st.title("PDF Summarizer")
    st.write("Upload a PDF file or type the text to summarize")

    upload_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if upload_file is not None:
        pdf_text = ""
        for page in PdfReader(upload_file).pages:
            pdf_text += page.extract_text()

        # Expander for extracted text
        with st.expander("Extracted Text"):
            st.write(pdf_text)

        # Summarize the text
        summarized_text = summarize_chunks(split_text_by_words(pdf_text))

        # Expander for summarized text
        with st.expander("Summarized Text"):
            st.write(summarized_text)

        # Get related links
        urls = links(summarized_text)

        # Expander for related links
        with st.expander("Related Links"):
            for url in urls:
                st.write(f"- {url}")

    else:
        input_text = st.text_area("Type text here")
        if st.button("Summarize"):
            summarized_text = summarize_chunks(split_text_by_words(input_text))

            # Expander for summarized text
            with st.expander("Summarized Text"):
                st.write(summarized_text)

            # Get related links
            urls = links(summarized_text)

            # Expander for related links
            with st.expander("Related Links"):
                for url in urls:
                    st.write(f"- {url}")

if __name__ == "__main__":
    main()
