# Text_Summarizer: A text_Summarizer built with LLM pre-trained models and Gemini AI
🔬Text Summarization for  **Large documents**! 💫
It is powered with pre-trained LLM models with high accuracy of data and also the efficiency of AI using Gemini AI 

# Text Summarizer : Features 🤖🗓️

 1. Summarizing the text
 2. Related links for reference 💬🤖
 3. Minimal data loss
 4. Large documents Summarization

# Workflow 📊📚

  -  The user can provide data in the form of text or either as a pdf.If pdf the text is extracted using [PyPDF2](https://pypi.org/project/PyPDF2/).
  -  The extracted text is then split into chunks each of size 500 words.
  -  The set of chunks are passed to summarizer function which in turn loads the pre trained model [facebook's bart large cnn](https://huggingface.co/facebook/bart-large-cnn) from Huggingface.
  -  The chunks are passed to the model by using a strategy of refine method which uses the previous contexts to maintain the integrity and minimize the information loss.
  -  Next with [Gemini's model](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/overview#text-use-cases) helps us to prettify the given summary to display the result in an attractive way.
  -  Finally based on the summary we suggest some reference links using Google's search engine api [Custom Search API](https://developers.google.com/custom-search/v1/introduction) which helps user to gain deeper knowledge about it.

# Demonstration of the project

https://github.com/KarthikeyanM3011/Text_Summarizer/assets/133127501/afa01117-618c-4f8b-86f8-16983665b552

# Built With 🛠️

  1.  **Frontend - Streamlit:** The frontend user interface was developed using Streamlit, a powerful Python library for creating web applications with simple Python scripts. Streamlit's intuitive interface allowed us to design interactive and responsive user interfaces effortlessly, streamlining the development process and enhancing user experience. 💻🌐

  2.  **Flask** : This also has a Code for Flask API.Sijnce Flask is a powerful python framework for API calls you can experiance it with this model.Flask provides safe and secure connection and also it retrives faster when compared to others

  3.  **LLM Models** - Facebook's Bart: ** The backend for text summarization is done by the pre-trained model [facebook's bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn).It is a transformer encoder-encoder (seq2seq) model with a bidirectional (BERT-like) encoder and an autoregressive (GPT-like) decoder which is trained upon **406M** parameters with a good ROUGE score**📊📚

  4.  **API's** - We have used Gemini's **[gemini-1.0-pro](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/overview#text-use-cases)** for prettifying the summary and **[Custom Search API](https://developers.google.com/custom-search/v1/introduction)** to get related reference links for more automated and efficient for learning path

  5.  **Other Technologies:** - In addition to streamlit , LLM models and API's we have also used **Langchain** for efficient usage of the pre-trained models and also Python a powerful language with concise and expressive syantax.it also has many built-in packages to make our work easy.🐍🚀📦
