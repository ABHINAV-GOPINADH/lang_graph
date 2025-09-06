# test_action_agent.py

from tools.inventory_connector import InventoryConnector
from tools.cmms_connector import CMMSConnector
from tools.notification_tool import NotificationTool
from agents.action_agent import ActionAutomationAgent

# Mock connectors for testing (optional if your connectors already simulate actions)
class MockInventoryConnector(InventoryConnector):
    def create_purchase_requisition(self, part_id, qty):
        print(f"Purchase requisition raised for part {part_id}, qty={qty}")
        return {"part": part_id, "quantity": qty, "status": "Pending Approval"}

class MockCMMSConnector(CMMSConnector):
    def create_work_order(self, asset, tasks, parts, technicians):
        print(f"Work order created for asset {asset}")
        return {"asset": asset, "tasks": tasks, "parts": parts, "technicians": technicians, "status": "Created"}

class MockNotificationTool(NotificationTool):
    def notify_team(self, message):
        print(f"Notification sent to team: {message}")

# Initialize the ActionAutomationAgent with mock tools
agent = ActionAutomationAgent()
agent.cmms = MockCMMSConnector()
agent.inventory = MockInventoryConnector()
agent.notifier = MockNotificationTool()

# Test data
asset = "Pump-101"
tasks = ["Inspect pump", "Lubricate bearings"]
parts = [
    {"id": "Bearing-001", "available": False},
    {"id": "Seal-002", "available": True}
]
technicians = ["Tech-A", "Tech-B"]
supervisor_report = "Approved maintenance plan for Pump-101"
approved = True

# Execute the agent
result = agent.execute(asset, tasks, parts, technicians, supervisor_report, approved)

print("\n=== Agent Execution Result ===")
print(result)
