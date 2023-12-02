# Legal Document Assistant

This repository was used for the Streamlit Deployment. Here is the link to the **[Legal Document Assistant](https://legaldocumentassistant-4swnagomyzzgbkj6sdmrsq.streamlit.app/)**.

If you want to test the program, but don't have a legal file to use, feel free to download *constitution.pdf* file from the repository. After uploading and processing the file, you can ask the chatbot questions about it.

## Design Challenge

**Design a chatbot solution to enable users in need of legal assistance to interact with their legal documents and receive guidance through a conversational interface.**

## Project Overview

### Problem Statement

Many individuals and businesses encounter challenges when dealing with legal documents. Understanding complex legal language, extracting critical information, and knowing how to interpret and act upon it can be daunting tasks. To address this problem, I developed a Legal Document Assistant chatbot (Saul Goodman).

### Project Description

**Solution Overview**

The Legal Document Assistant is a user-friendly chatbot that helps individuals and businesses to interact with their legal documents easily. It provides a streamlined process for uploading legal documents, asking questions related to the content, and receiving informative responses. The chatbot uses state-of-the-art natural language processing and machine learning technologies to offer valuable insights and guidance.

**Components and Workflow**

1. **Streamlit Interface**
   - I have created a web-based user interface using Streamlit, which allows users to upload their legal documents and interact with the chatbot.

2. **Document Processing**
   - Upon uploading a legal document (in PDF, DOCX, or TXT format), the Python code extracts the text content from the document using the PyPDF2 library for PDF files.

3. **Text Chunking**
   - The extracted text is divided into manageable chunks using the CharacterTextSplitter. This step ensures that the chatbot can effectively process and respond to user queries.

4. **Vector Store**
   - I employed OpenAIEmbeddings to convert the text chunks into vector representations. These vectors are stored and indexed using FAISS, a high-performance similarity search library.

5. **Conversational Chatbot**
   - The heart of the system is the ConversationalRetrievalChain, which utilizes a chat model provided by OpenAI. This chat model responds to user questions based on the content of the uploaded document. To ensure a seamless and context-aware conversation, the Legal Document Assistant retains the chat history between the user and the chatbot. This feature allows the system to remember and reference previous user queries and responses. By maintaining the chat history, the chatbot can provide more coherent and relevant answers based on the ongoing conversation context.

6. **User Interaction**
   - Users can interact with the chatbot by asking questions related to their legal documents. The chatbot provides responses in a conversational manner.

7. **Response Visualization**
   - User and chatbot interactions are displayed in a visually appealing format using HTML templates. User inputs and chatbot responses are clearly distinguished.

**Custom Hyperparameters**

To optimize the chatbot's performance for assisting users with legal documents, I have configured custom hyperparameters for the chat model:

- **temperature**: 0.2 (to provide focused and deterministic responses)
- **max_tokens**: 100 (to keep responses concise)
- **top_p**: 0.7 (to allow some response flexibility)
- **frequency_penalty**: 0.2 (to encourage diverse legal terminology)
- **presence_penalty**: 0.2 (to reduce repetition of input content)

### How It Works

1. Users upload their legal documents through the Streamlit interface.
2. The chatbot processes the document, extracts text, and creates vector representations.
3. Users interact with the chatbot by asking questions about their documents.
4. The chatbot analyzes the questions, retrieves relevant information from the vector store, and provides informative responses.
5. User and chatbot interactions are displayed in a user-friendly manner in the interface.

### Conclusion

The Legal Document Assistant chatbot aims to bridge the gap between legal complexity and accessibility. By combining the power of natural language processing, machine learning, and an intuitive user interface, I aspire to provide users with valuable assistance in navigating the legal sector.
