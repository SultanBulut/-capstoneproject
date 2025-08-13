# rag/educational_story_rag.py

import os
from dotenv import load_dotenv
import asyncio
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain import LLMChain
from langchain.prompts import PromptTemplate

from langchain_community.document_loaders import TextLoader, PyPDFLoader

from tempfile import NamedTemporaryFile

# Ortam değişkenlerini yükle
load_dotenv()

# API Anahtarını al
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Event loop yoksa oluşturup ayarlayın
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Embedding modeli
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_API_KEY
)

# LLM (Gemini Pro)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

# Prompt şablonu
prompt_template = """
Aşağıdaki bilgileri kullanarak, {topic} hakkında çocuklara yönelik eğlenceli ve öğretici bir hikaye yaz:

{context}

Hikaye çocukların anlayabileceği basit bir dille yazılmalı ve öğretici olmalıdır.
"""

prompt = PromptTemplate(
    input_variables=["topic", "context"],
    template=prompt_template,
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

# Metni yükle ve böl
def load_text_and_chunk(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([text])
    return docs

# Vektör veritabanını oluştur (FAISS)
def create_vectorstore(docs):
    vectordb = FAISS.from_documents(
        documents=docs,
        embedding=embedding
    )
    return vectordb

# Hikaye üret
def generate_story_from_docs(user_question, vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(user_question)
    context = "\n".join([doc.page_content for doc in docs])
    story = llm_chain.run(topic=user_question, context=context)
    return story

# UploadedFile'dan hikaye üretmek için ana fonksiyon
def generate_story_from_uploaded_file(uploaded_file, topic):
    # UploadedFile'i temp dosyaya kaydet
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Dosya tipine göre loader seç
    ext = os.path.splitext(tmp_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(tmp_path)
    elif ext == ".txt":
        loader = TextLoader(tmp_path, encoding="utf-8")
    else:
        os.remove(tmp_path)
        raise ValueError("Desteklenmeyen dosya formatı! Sadece PDF ve TXT dosyaları desteklenmektedir.")

    try:
        # Belgeleri yükle ve böl
        docs = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)

        # Vektör veritabanı oluştur (FAISS)
        vectordb = create_vectorstore(chunks)

        # Hikaye üret
        story = generate_story_from_docs(topic, vectordb)

        return story
        
    except Exception as e:
        raise Exception(f"Hikaye oluşturulurken hata oluştu: {str(e)}")
    finally:
        # Temp dosyayı sil
        if os.path.exists(tmp_path):
            os.remove(tmp_path)