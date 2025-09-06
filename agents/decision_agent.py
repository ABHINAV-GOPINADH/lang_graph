import os
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY, GEMINI_MODEL
from tools.rag_retriever import get_retriever

class DecisionAgent:
    def __init__(self):
        api_key = GEMINI_API_KEY
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash") 

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            api_key=api_key,
            temperature=0.0,
            max_tokens=512
        )

        # Retriever + QA chain
        retriever = get_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            chain_type="stuff"
        )

        # Decision prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a predictive maintenance decision agent. "
                       "Use predictions and manuals to recommend actions."
                       "Use a summarize format (symptoms,possible causes,required parts,actions)"
                       ),
            ("human", "Predictions:\n{predictions}\n\n"
                      "Give specific maintenance actions, required parts, and urgency. "
                      "Use the format as symtoms,possible causes,required parts,actions"
                      "Use the manual if relevant.")
        ])


    def decide(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        # Get manual context
        manual_context = self.qa_chain.invoke({
            "query": "maintenance procedure for " + str(predictions)
        })['result']

        # Generate decision using prompt + LLM
        chain = self.prompt | self.llm
        response_text = chain.invoke({"predictions": predictions})

        return {
            "decision": response_text,
            "manual_context": manual_context
        }

