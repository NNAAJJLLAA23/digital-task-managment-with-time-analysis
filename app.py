import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002"

st.title("🗂 Digital Task Management")

if "username" not in st.session_state:
    st.session_state["username"] = None

menu = ["Login", "Register", "My Tasks"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")
    if st.button("Register"):
        res = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
        if res.status_code == 200:
            st.success("Account created!")
        else:
            st.error(res.json().get("detail"))

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        res = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state["username"] = username
            st.success("Logged in successfully!")
        else:
            st.error(res.json().get("detail"))

elif choice == "My Tasks":
    if st.session_state["username"] is None:
        st.warning("You must login first.")
    else:
        st.subheader("Your Tasks")
        res = requests.get(f"{API_URL}/tasks/", params={"username": st.session_state['username']})
        if res.status_code == 200:
            tasks = res.json()
            for t in tasks:
                st.write(f"{t['title']} — {t['start_time']} → {t['end_time']}")
        else:
            st.error("Error fetching tasks")

        title = st.text_input("New task", key="task_title")
        start = st.text_input("Start time (YYYY-MM-DD HH:MM:SS)", key="task_start")
        end = st.text_input("End time (YYYY-MM-DD HH:MM:SS)", key="task_end")
        if st.button("Add Task"):
            data = {
                "username": st.session_state["username"],
                "title": title,
                "start_time": start,
                "end_time": end
            }
            res = requests.post(f"{API_URL}/tasks/", json=data)
            if res.status_code == 200:
                st.success("Task added!")
            else:
                st.error("Error adding task")

