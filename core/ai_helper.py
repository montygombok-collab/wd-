import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# مسارات الداتا والفهرس
DB_PATH = "data/index_db"
TXT_PATH = "data/txt_files"

def build_data_index():
    """قراءة المراجع النصية وبناء الفهرس في قاعدة البيانات"""
    if not os.path.exists(TXT_PATH):
        os.makedirs(TXT_PATH, exist_ok=True)
        return "لم يتم العثور على مجلد النصوص، تم إنشاؤه. يرجى إضافة ملفات .txt"
    
    loader = DirectoryLoader(TXT_PATH, glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    docs = loader.load()
    
    if not docs:
        return "مجلد النصوص فارغ! يرجى إضافة ملفات .txt داخل مجلد data/txt_files"

    # تقطيع النصوص لفقرات مناسبة للبحث الأثري
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)

    # تحويل النصوص إلى متجهات وتخزينها
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=DB_PATH)
    return f"تمت فهرسة {len(docs)} ملف نصوص بنجاح في قاعدة البيانات! ✅"

def ask_assistant(query):
    """استقبال سؤال الباحث والإجابة عليه عبر Gemini والداتا المتاحة"""
    if not os.path.exists(DB_PATH):
        return "عذراً، لم يتم بناء الفهرس بعد. يرجى الضغط على 'تحديث الفهرس والداتا' من الشريط الجانبي."

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

    system_prompt = (
        "أنت 'ود الحاج AI'، المساعد الأكاديمي والبحثي المتخصص لكلية الآثار. "
        "مهمتك الإجابة على أسئلة الطلاب والباحثين بأعلى دقة علمية اعتماداً فقط على المراجع والنصوص المرفقة أدناه. "
        "إذا لم تجد الإجابة في النصوص المرفقة، أجب بوضوح: 'عذراً، هذه المعلومة غير متوفرة في المراجع المتاحة حالياً.'\n\n"
        "المراجع المتاحة:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": query})
    return response["answer"]
