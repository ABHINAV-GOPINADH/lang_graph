from typing import List, Dict, Any
from tools.inventory_connector import InventoryConnector
from tools.cmms_connector import CMMSConnector
from tools.notification_tool import NotificationTool

class ActionAutomationAgent:
    def __init__(self):
        self.inventory = InventoryConnector()
        self.cmms = CMMSConnector()
        self.notifier = NotificationTool()

    def execute(self, asset: str, tasks: list, parts: list, technicians: list, supervisor_report: str, approved: bool):
        if not approved:
            return {"status": "rejected", "message": "Supervisor did not approve the plan."}

        results = {}

        # 1. Raise purchase requisitions for missing parts
        results["requisitions"] = []
        for part in parts:
            if not part.get("available", True):  # if inventory says not available
                req = self.inventory.create_purchase_requisition(part["id"], qty=1)
                results["requisitions"].append(req)

        # 2. Create CMMS Work Order
        wo = self.cmms.create_work_order(asset, tasks, parts, technicians)
        results["work_order"] = wo

        # 3. Notify team with supervisor report
        self.notifier.notify_team(supervisor_report)
        results["notification"] = "Sent to team"

        return {
            "status": "success",
            "executed_plan": supervisor_report,
            "systems_updated": results
        }
