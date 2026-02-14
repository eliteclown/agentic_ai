from dotenv import load_dotenv

# Use the langchain package imports (adjust if your environment differs)
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from index import vectore_store

load_dotenv()

client = OpenAI()

embedding_model = OpenAIEmbeddings()



# Correct variable name and use Retriever API
retriever = vectore_store.as_retriever(search_kwargs={"k": 5})
user_query = input("Enter your query: ")

# Use the retriever's document retrieval method
docs = retriever.invoke(user_query)

results = [doc.page_content for doc in docs]

SYSTEM_PROMPT = """
You are a helpful assistant for question-answering tasks. Use the following retrieved documents to answer the user's query. If you don't know the answer, say you don't know.

User Query: {user_query}
Retrieved Documents: {results}
// Thought Process: Analyze the retrieved documents to find relevant information that can help answer the user's query. Consider the context and details provided in the documents to formulate a comprehensive response.
    output the thought process in a clear and structured manner, explaining how you are interpreting the retrieved information and how it relates to the user's query. This will help in understanding your reasoning and the steps you are taking to arrive at the final answer.
Final Answer: Based on the retrieved documents and your analysis, provide a concise and accurate answer to
the user's query. Ensure that your answer directly addresses the question and is supported by the information found in the retrieved documents.
"""


