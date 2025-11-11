import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # tvoj FastAPI backend

st.title("🗂 Digital Task Management")

menu = ["Login", "Register", "My Tasks"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        data = {"username": username, "password": password}
        res = requests.post(f"{API_URL}/register", json=data)
        st.success("Account created!") if res.status_code == 200 else st.error("Error during registration.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        data = {"username": username, "password": password}
        res = requests.post(f"{API_URL}/login", json=data)
        if res.status_code == 200:
            st.session_state["user"] = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")

elif choice == "My Tasks":
    if "user" not in st.session_state:
        st.warning("You need to login first.")
    else:
        st.subheader("My Tasks")
        res = requests.get(f"{API_URL}/tasks?user={st.session_state['user']}")
        if res.status_code == 200:
            tasks = res.json()
            for task in tasks:
                st.write(f"- {task['title']} ({task['status']})")
        new_task = st.text_input("Add new task")
        if st.button("Add Task"):
            data = {"title": new_task, "user": st.session_state["user"]}
            res = requests.post(f"{API_URL}/tasks", json=data)
            if res.status_code == 200:
                st.success("Task added!")
