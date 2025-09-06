import random, datetime
import pandas as pd
from typing import Dict, Any

class IoTConnector:
    def fetch_sensor_data(self) -> Dict[str, Any]:
        """Mock IoT sensor data for 2 generators and 2 compressors"""
        records = []

        for i in range(1, 3):
            records.append({
                "asset_id": f"Generator-{i}",
                "type": "generator",
                "timestamp": datetime.datetime.now().isoformat(),
                "vibration": round(random.uniform(0.2, 2.5), 2),
                "exhaust_temp": round(random.uniform(300, 600), 1),
                "oil_pressure": round(random.uniform(20, 60), 1),
                "load_kw": round(random.uniform(100, 500), 1),
            })

        for i in range(1, 3):
            records.append({
                "asset_id": f"Compressor-{i}",
                "type": "compressor",
                "timestamp": datetime.datetime.now().isoformat(),
                "vibration": round(random.uniform(0.2, 1.5), 2),
                "motor_current": round(random.uniform(10, 40), 1),
                "discharge_temp": round(random.uniform(60, 120), 1),
                "pressure": round(random.uniform(80, 120), 1),
            })

        return {"iot_data": pd.DataFrame(records).to_dict(orient="records")}
