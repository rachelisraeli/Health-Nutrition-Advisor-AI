import requests
import uuid

class HealthAdvisorClient:
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.user_id = str(uuid.uuid4())  # ID ייחודי למשתמש
        
    def send_message(self, message):
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
                "user_id": self.user_id
            }
        )
        return response.json()
    
    def reset_conversation(self):
        requests.post(
            f"{self.base_url}/reset",
            json={"user_id": self.user_id}
        )
        print("🔄 השיחה אופסה")

def main():
    client = HealthAdvisorClient()
    print("🏥 יועץ הבריאות והתזונה שלך")
    print("--------------------------------")
    print("כתוב 'יציאה' לסיום או 'איפוס' לשיחה חדשה\n")
    
    while True:
        user_input = input("אתה: ").strip()
        
        if user_input.lower() in ['יציאה', 'exit', 'quit']:
            print("להתראות! 👋")
            break
            
        if user_input.lower() in ['איפוס', 'reset']:
            client.reset_conversation()
            continue
            
        if not user_input:
            continue
        
        try:
            response = client.send_message(user_input)
            
            if 'error' in response:
                print(f"❌ שגיאה: {response['message']}")
            else:
                print(f"\n🤖 יועץ: {response['response']}\n")
                print(f"[הודעות בשיחה: {response['conversation_length']}]\n")
        except Exception as e:
            print(f"❌ שגיאה: {e}")

if __name__ == "__main__":
    main()
