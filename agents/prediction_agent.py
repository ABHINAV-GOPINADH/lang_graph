from typing import Dict, Any

class PredictionAgent:
    def __init__(self):
        pass

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze IoT data and generate predictions (mock version)."""
        iot_data = data["iot_data"]
        results = []

        for row in iot_data:
            prediction = {"asset_id": row["asset_id"], "alerts": []}

            # Simple threshold checks
            if row.get("vibration") and row["vibration"] > 2.0:
                prediction["alerts"].append("High vibration - possible bearing issue")

            if row.get("exhaust_temp") and row["exhaust_temp"] > 550:
                prediction["alerts"].append("High exhaust temp - possible injector/turbo issue")

            if row.get("motor_current") and row["motor_current"] > 30:
                prediction["alerts"].append("High motor current - possible overload")

            # Mock Remaining Useful Life (RUL)
            prediction["rul_hours"] = 1000 if not prediction["alerts"] else 100

            results.append(prediction)

        return {"predictions": results}
