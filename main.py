import os, dotenv
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

#import matplotlib.pyplot as plt 
#import seaborn as sns




#API keys loading
load_dotenv()
#api_key = os.getenv('GOOGLE_API_KEY')
api_key="AIzaSyA6J3u2hL4jNsFE67yy2q75KV9BSkdLHnI"



#LLM loading. Here we use gemini
llm= ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5,google_api_key=api_key)



#Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", temperature=0.5,google_api_key=api_key)




#BDV loading
data_store=Chroma(persist_directory="indaba_x_bdv", embedding_function=embeddings)





#Then, we will retriever a vectorial database. If you want how to xreate a database, you'll find it in notebook
retriever = data_store.as_retriever(search_type="similarity", search_kwargs={"k": 15})



#PrompTemplate
#Here I create a template to use to query the model
template = """You are a chatbot that answer to a query like "what is the best performing brand in Abidjan" and it should return a result that shows the brand with the highest volume of sales calculated from the provided dataset.
    
    The submission will be graded based on the responsiveness of the chatbot (speed and conversational ability), the accurate calculation of returned values, the aesthetics of the tool, and the ability to provide extra information relevant to the query.

    You must be able to handle a variety of queries, including:

    Product sales trends over time (e.g., what were the top-performing brands in the last quarter?)
    Comparison of sales performance across different cities (e.g., what was the performance of BRAND A compared to BRAND B in each quarter in various cities)
    Market view: What is the market size in each quarter?

   Cut the query in small piece left to right et right to left to undestand well the query.I you have'nt response,use gemini knowledge to answer and provide link to source.



 Here is the question you are supposed to answer: {input}

  context: {context}
  input: {input}
  answer:
 """


prompt = PromptTemplate(
        template=template,
    input_variables=['input']
)



#Chain LLM, prompt and retriever
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)





#Let's write a function to retrieve with llm
def chatbot(question : str):
    response=retrieval_chain.invoke({"input": question})

    if response:
        return response['answer']
    else :
        "Please, ask another question"




print(chatbot("Make me a presnetation of what you can do"))





