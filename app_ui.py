import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title="Health & Nutrition Advisor",
    page_icon="🥗",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #f8faf8;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 12px;
    }
    .chat-container {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🥗 יועץ הבריאות והתזונה שלך")
st.write("ברוכים הבאים! כאן תוכלו לקבל עצות לתזונה נכונה ואורח חיים בריא.")

with st.sidebar:
    st.header("ניהול שיחה")
    if st.button("🔄 התחל שיחה חדשה"):
        try:
            url = "http://127.0.0.1:5001/reset"
            payload = {"user_id": st.session_state.user_id}
            
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                st.session_state.chat_history = []
                st.success("השיחה אופסה בהצלחה!")
                st.rerun()
            else:
                st.error(f"שגיאה מהשרת: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("לא ניתן להתחבר לשרת. וודא ש-server.py רץ בפורט 5001.")
        except Exception as e:
            st.error(f"שגיאה לא צפויה: {e}")
    
    st.markdown("---")
    st.markdown("### 🍎 עקרונות התזונה")
    
    st.write("1. **גיוון בצלחת:** שלבו צבעים שונים.")
    st.write("2. **שתייה:** לפחות 8 כוסות מים ביום.")
    st.write("3. **פעילות:** הליכה יומית של 30 דקות.")


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("מה תרצה לדעת היום?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("מכין לך תשובה בריאה..."):
            response = requests.post(
                "http://localhost:5001/chat",
                json={"message": prompt, "user_id": st.session_state.user_id}
            )
            res_data = response.json()
            
            if "response" in res_data:
                full_response = res_data["response"]
                with st.chat_message("assistant"):
                    st.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            else:
                st.error("שגיאה בקבלת תשובה מהשרת.")
    except Exception as e:
        st.error(f"לא ניתן להתחבר לשרת בפורט 5001. וודא ש-server.py רץ! ({e})")
