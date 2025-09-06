# tools/cmms_connector.py
class CMMSConnector:
    def __init__(self):
        self.work_orders = []
        self.technicians = [
            {"name": "John Doe", "skill": "Motor Specialist", "available": True},
            {"name": "Jane Smith", "skill": "Compressor Alignment", "available": False},
            {"name": "Raj Patel", "skill": "Filter Replacement", "available": True},
        ]

    def get_available_technicians(self):
        """Return list of available technicians."""
        return [tech for tech in self.technicians if tech["available"]]
    def create_work_order(self, asset, tasks, parts, technicians):
        """Simulate work order creation in CMMS (IBM Maximo)."""
        wo = {
            "asset": asset,
            "tasks": tasks,
            "parts": parts,
            "technicians": technicians,
            "status": "Created"
        }
        self.work_orders.append(wo)
        return wo
