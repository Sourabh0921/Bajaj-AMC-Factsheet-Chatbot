from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
import time
import os
from langchain_groq import ChatGroq
import streamlit as st
import re

# groq_api_key = os.getenv("GROQ_API_KEY")

def clean_response(response_text):
    text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)    
    text = re.sub(r"\\begin\{.*?\}.*?\\end\{.*?\}", "", text, flags=re.DOTALL)
    text = text.replace("$", "")
    text = re.sub(r"\\[a-zA-Z]+\{(.*?)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = text.replace("[", "").replace("]", "")
    text = re.sub(r"[ ]{2,}", " ", text) 
    text = re.sub(r"(?<!\n)\n(?!\n)", "\n", text)  
    text = re.sub(r"\n{3,}", "\n\n", text) 
    return text.strip()

def handle_query(prompt1):
    llm = ChatGroq( 
        groq_api_key=groq_api_key,
        model_name="openai/gpt-oss-120b"
    )

    prompt_template = ChatPromptTemplate.from_template(
        """
        You are a specialized Bajaj Finserv AMC Fund Factsheet analyst assistant.

        Answer the question comprehensively using the provided context from the Bajaj AMC Fund Factsheet.  
        Provide detailed explanations and insights based on the available data.
        Use all relevant information from the factsheet context to give a complete answer.

        <context>
        {context}
        </context>

        Question: {input}

        Output Formatting Guidelines:
        - Provide comprehensive answers with context and explanations
        - Use bullet points, tables, or structured format for clarity
        - Include relevant background information from the factsheet
        - **For fund performance and financial metrics, follow this enhanced format:**

        **Overview:**  
        - Brief introduction to the fund/metric being discussed
        - Context about the fund's strategy or category

        **Data Source:**  
        - Clearly mention which fund/section from factsheet
        - Include reporting period and data as of date

        **Detailed Analysis:**  
        - Present all relevant data points
        - Include comparative information if available
        - Explain trends or patterns observed
        - Provide sector/theme context where applicable

        **Key Findings:**  
        - Highlight important insights
        - Compare with benchmarks if available
        - Note any significant changes or trends

        **Additional Context:**  
        - Include related information from factsheet
        - Mention fund manager details if relevant
        - Add expense ratios, fund size, or other metrics as applicable

        **Formula (if applicable):**  
        - Write the financial calculation formula
        - Show step-by-step computation if needed

        **Final Summary:**  
        - Comprehensive conclusion with all key points
        - Include units (%, ₹ Crores, basis points, etc.)

        **Enhanced Instructions:**
        - For holdings questions: Include sector allocation, market cap distribution, and portfolio strategy
        - For performance questions: Add benchmark comparison, risk metrics, and historical context
        - For fund comparisons: Create detailed comparison tables with multiple metrics
        - For asset allocation: Explain investment philosophy and allocation rationale
        - Always provide business context and fund strategy insights
        - Include fund manager commentary or investment thesis if available
        - Add peer comparison or category average data when present

        **Example Enhanced Response for Holdings:**

        **Overview:**  
        The Bajaj [Fund Name] follows a diversified investment approach across large and mid-cap stocks.

        **Data Source:**  
        Bajaj [Fund Name] portfolio holdings as of [Date] from monthly factsheet

        **Detailed Analysis:**  
        **Top Holdings:**
        - [Stock Name]: [%] - [Sector] - [Brief about company/rationale]
        - [Continue for top 5-10 holdings]

        **Sector Allocation:**
        - [Sector]: [%]
        - [Additional sectors with context]

        **Portfolio Strategy:**
        - [Investment approach from factsheet]
        - [Risk management aspects]

        **Key Findings:**  
        - Portfolio concentration in [sectors/themes]
        - Focus on [quality/growth/value] stocks
        - Diversification across [market caps/sectors]

        Use all available information from the factsheet context to provide rich, detailed responses.
        Do **not** use LaTeX, <think> tags, or mathematical symbols.
        Always provide comprehensive analysis while staying within factsheet data.
        """
    )

    document_chain = create_stuff_documents_chain(llm, prompt_template)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start_time = time.time()
    response = retrieval_chain.invoke({"input": prompt1})
    end_time = time.time()

    raw_answer = response.get("answer", "No relevant context found.")
    cleaned_answer = clean_response(raw_answer)

    context_docs = response.get("context", [])

    return cleaned_answer, context_docs, end_time - start_time