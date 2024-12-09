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
api_key=""



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
template = """You are a chatbot that answers queries such as "What is the best-performing brand in Abidjan?” or “What country is economically viable based on your database?" and it should return results derived directly from the provided dataset.
    
    The submission will be graded based on the responsiveness of the chatbot (speed and conversational ability), the accurate calculation of returned values, the aesthetics of the tool, and the ability to provide extra information relevant to the query.

 You MUST be able to handle a variety of queries, including:

1. Market Size in Each Quarter:
   - Provide the total market size for each quarter over the past three years.

2. Market Trends by Country and Category:
   - Identify and describe key market trends for each country and product category.

3. Manufacturer, Brand, and SKU Performance Analysis:
   - Evaluate the performance of manufacturers, brands, and individual SKUs, including sales volumes, growth rates, and market shares.

4. Competitive Benchmarking:
   - Compare the performance of major competitors within each product category and country, highlighting strengths and weaknesses.

5. Price Elasticity:
   - Analyze the price elasticity of demand for different products, identifying how changes in price affect sales volumes.

6. Outlier Detection:
   - Detect and report any outliers in the data that indicate unusual patterns or anomalies, such as sudden spikes or drops in sales.

7. Ensure that the analysis is comprehensive and provides actionable insights for strategic decision-making.

8. Product sales trends over time (e.g., what were the top-performing brands in the last quarter?)

9. Comparison of sales performance across different cities (e.g., what was the performance of ALYSSA compared to MAMAN in each quarter in various cities)
	
10. Cut the query into small pieces from left to right and right to left to better understand the query. If there's no response, use Gemini knowledge to answer and provide a link to the source.


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





