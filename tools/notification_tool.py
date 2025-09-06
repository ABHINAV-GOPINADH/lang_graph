# tools/notification_tool.py
class NotificationTool:
    def __init__(self):
        # Mock supervisor inbox
        self.supervisor_response = None

    def send_to_supervisor(self, report: str):
        """Send report to supervisor (console simulation)."""
        print("\n📩 Sending report to supervisor...")
        print(report)
        print("-------------------------------------------------")
        print("Supervisor, please approve (yes/no):")

        # Simulate manual supervisor response (you can integrate email/Slack)
        self.supervisor_response = input().strip().lower()
        return self.supervisor_response
    
    def notify_team(self, message: str):
        """Send notification to maintenance team (simulate Teams/Slack)."""
        print("\n📱 Sending notification to maintenance team...")
        print(message)
