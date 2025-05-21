import torch
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os

def initialize_chain():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load multiple PDFs
    pdf_files = ["./leave_policy.pdf", "./company_policy.pdf"]  # Add your PDF files here
    all_documents = []

    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"Loading {pdf_file}...")
            loader = PyPDFLoader(file_path=pdf_file)
            documents = loader.load()
            all_documents.extend(documents)
            print(f"Loaded {len(documents)} pages from {pdf_file}")
        else:
            print(f"Warning: {pdf_file} not found")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    text_chunks = text_splitter.split_documents(all_documents)

    # Initialize Large Language Model for answer generation
    llm_answer_gen = LlamaCpp(
        streaming=True,
        model_path=r"./mistral-7b-openorca.Q4_0.gguf",
        temperature=0.75,
        top_p=1,
        f16_kv=True,
        verbose=False,
        n_ctx=4096
    )

    # Create vector database for answer generation
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": device})

    # Initialize vector store for answer generation
    vector_store = Chroma.from_documents(text_chunks, embeddings)

    # Initialize retrieval chain for answer generation
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"  # Specify which output to store in memory
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm_answer_gen, 
        retriever=vector_store.as_retriever(),
        memory=memory,
        return_source_documents=True  # Enable source tracking
    )

# Only run the terminal interface if this file is run directly
if __name__ == "__main__":
    answer_gen_chain = initialize_chain()
    while True:
        user_input = input("Enter a question: ")
        if user_input.lower() == 'q':
            break

        # Run question generation chain
        result = answer_gen_chain.invoke({"question": user_input})
        print("\nAnswer:", result['answer'])
        print("\nSources:", [doc.metadata.get('source', 'Unknown') for doc in result.get('source_documents', [])])
