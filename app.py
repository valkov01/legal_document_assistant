import streamlit as st # used for building web app
# from dotenv import load_dotenv # used for loading env variables
from PyPDF2 import PdfReader # used for reading pdf files
from langchain.text_splitter import CharacterTextSplitter # used for splitting text into chunks
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings # used for creating vector store (using OpenAI, online) (using HuggingFace, locally)
from langchain.vectorstores import FAISS # used for creating vector store (using FAISS, locally)
from langchain.chat_models import ChatOpenAI # used for creating the chat model (using OpenAI)
from langchain.llms import HuggingFaceHub # used for creating the chat model (using HuggingFace model)
from langchain.memory import ConversationBufferMemory # used for creating conversation chain memory
from langchain.chains import ConversationalRetrievalChain # allows to chat with the vector store
from htmlTemplates import css, bot_template, user_template # used for creating the chat UI


def get_pdf_text(pdf_docs): # get text from pdf
    text = ""
    for pdf in pdf_docs: # iterate through all pdfs
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: # iterate through all pages
            text += page.extract_text() # extract text from page
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter( # split text into chunks
        separator="\n", # split text by new line
        chunk_size=1000, # split text into chunks of 1000 characters
        chunk_overlap=200, # overlap chunks by 200 characters
        length_function=len # use len function to get length of text
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # locally, but it's not really slow, because it's using CPU
    embeddings = OpenAIEmbeddings() # online
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings) # we use Faiss to store the vectors
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI( # OpenAI chat model, online
    temperature=0.2,
    max_tokens=100,
    model_kwargs={
        'top_p': 0.7,
        'frequency_penalty': 0.2,
        'presence_penalty': 0.2
    }
    )
    llm = HuggingFaceHub(repo_id='google/flan-t5-xxl') # HuggingFace chat model, locally
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0: # if even, it's user
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:       # if odd, it's bot
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    # load_dotenv()
    st.set_page_config(page_title='Legal Problems Assistant', page_icon=':page_facing_up:')
    st.write(css, unsafe_allow_html=True)

    if 'conversation' not in st.session_state: # if there is no conversation, create one
        st.session_state.conversation = None

    if 'chat_history' not in st.session_state: # if there is no chat history, create one
        st.session_state.chat_history = None

    st.header('Legal Problems Assistant :page_facing_up:')
    user_question = st.text_input("Hi, I'm Saul Goodman. Did you know you have rights? The Constitution says you do, and so do I. I believe that until proven guilty, every man, woman and child is innocent. How can I assist you?")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
             "Upload your documents here:", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing your documents..."):
                # get text from pdf
                raw_text = get_pdf_text(pdf_docs)

                # get text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
        main()
