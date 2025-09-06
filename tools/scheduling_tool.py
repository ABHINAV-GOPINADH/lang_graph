from typing import List, Dict, Any
import random
import datetime

class SchedulingTool:
    """Tool to find an optimal maintenance schedule."""

    def find_optimal_time(self, technicians: List[str], parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not technicians:
            return {"scheduled_time": None, "team": None, "note": "No technicians available"}

        # Pick first available technician (or random)
        assigned_tech = random.choice(technicians)

        # Schedule 1 day later at 10:00 AM
        scheduled_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d 10:00")

        return {
            "scheduled_time": scheduled_time,
            "team": assigned_tech,
            "parts_status": [p.get("id", "unknown") + " - " + p.get("status", "unknown") for p in parts]
        }
