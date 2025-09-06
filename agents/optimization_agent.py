# agents/optimizer_agent.py
import ast
import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from sympy import re
from config import GEMINI_API_KEY, GEMINI_MODEL
from tools.inventory_connector import InventoryConnector
from tools.cmms_connector import CMMSConnector
from tools.scheduling_tool import SchedulingTool
from tools.notification_tool import NotificationTool


class OptimizerAgent:
    def __init__(self):
        # LLM setup
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", GEMINI_MODEL),
            api_key=GEMINI_API_KEY,
            temperature=0.0,
            max_tokens=512
        )

        # Tools
        self.inventory = InventoryConnector()
        self.cmms = CMMSConnector()
        self.scheduler = SchedulingTool()

    def generate_supervisor_report(
        self, decision_output: Dict[str, Any], parts_report: List[Dict[str, Any]],
        techs: List[str], schedule: str
    ) -> str:
        """Ask LLM to generate an intelligent summary for the supervisor."""
        prompt = f"""
            You are a maintenance optimization assistant.

            Decision Agent Recommendation:
            {decision_output.get('decision', '')}

            Manual Context:
            {decision_output.get('manual_context', '')}

            Parts Availability:
            {parts_report}

            Technician Availability:
            {techs}

            Optimal Maintenance Window:
            {schedule}

            Summarize into a clear supervisor report:
            - What the issue is
            - Which parts are available/missing
            - Which technicians are free
            - The recommended schedule
            - Final prioritized action plan
            """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def analyze_and_execute(self, decision_output: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize decision output, enrich with tools, and return structured state for supervisor."""
        print("\n🔎 Optimizer Agent: Analyzing decision agent output...")

        # 1. Use LLM to extract parts list
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant that extracts spare parts names and IDs from maintenance reports."),
            ("human", "Extract all spare parts mentioned in this decision report:\n\n{report}\n\n"
                      "Return only a Python list of part IDs or names, no explanations.")
        ])

        decision_text = decision_output.get("decision", "")
        chain = prompt | self.llm

        import json

        try:
            llm_response = chain.invoke({"report": decision_text})
            raw_output = llm_response.content.strip()

            # remove ```python ... ``` fences if present
            raw_output = re.sub(r"^```(?:python)?", "", raw_output).strip()
            raw_output = re.sub(r"```$", "", raw_output).strip()

            # safely parse Python list
            parts_needed = ast.literal_eval(raw_output)

        except Exception as e:
            print("⚠️ Error parsing LLM parts output:", e)
            print("LLM raw output:", raw_output)
            parts_needed = []

        print("\n🧩 Parts extracted:", parts_needed)

        # 2. Check each part in inventory
        parts_report = []
        for part in parts_needed:
            part_info = self.inventory.check_part(part)
            part_info["id"] = part
            parts_report.append(part_info)

        # 3. Get technician availability
        available_techs = self.cmms.get_available_technicians()

        # 4. Find optimal schedule
        schedule = self.scheduler.find_optimal_time(available_techs, parts_report)

        # 5. Generate supervisor report
        supervisor_report = self.generate_supervisor_report(
            decision_output, parts_report, available_techs, schedule
        )
        print("\n📋 Supervisor Report Draft:\n", supervisor_report)

        # 6. Return structured state (let graph handle supervisor + action)
        return {
            "optimization": supervisor_report,
            "parts_report": parts_report,
            "available_techs": available_techs,
            "schedule": schedule
        }
