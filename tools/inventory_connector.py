# tools/inventory_connector.py
class InventoryConnector:
    def __init__(self):
        # Mock inventory database
        self.inventory = {
            "COMP-FLT-7A": {"name": "Filter Cartridge", "stock": 12, "location": "Warehouse A"},
            "Motor-Bearing-22": {"name": "Motor Bearing", "stock": 5, "location": "Warehouse B"},
            "Seal-Kit-45": {"name": "Seal Kit", "stock": 0, "location": "Warehouse A"},
        }

    def check_part(self, part_number: str):
        """Return availability of a specific part."""
        return self.inventory.get(part_number, {"name": "Unknown", "stock": 0, "location": "N/A"})
    def create_purchase_requisition(self, part_id, qty):
        """Simulate raising a purchase requisition."""
        req = {
            "part": part_id,
            "quantity": qty,
            "status": "Pending Approval"
        }
        self.requisitions.append(req)
        return req
