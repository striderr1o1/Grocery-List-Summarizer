from applogic.mongoDB_conn import MongoDBConnector
from applogic.auth import authentication
import streamlit as st
from applogic.auth import authentication

def require_auth(db_connector):
    if st.session_state.get("authenticated"):
        return  # user already logged in
    st.title("Authentication")

    db_connector.connectToAuthDatabase()
    authobj = authentication(db_connector)

    option = st.selectbox("Login or Sign-up", ["Login", "Sign-up"])
    if option == "Login":
        login(authobj)
    else:
        signup(authobj)
    st.stop()  # IMPORTANT: stop rest of app until auth passes

def login(authobj):
    st.subheader("Login")

    username = st.text_input("username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        #check if exists
        # user = users_collection.find_one({"username": email})
        # cursor = dbconnector.get_user(username)
        # user = cursor[0]
        # if not user:
        #     st.error("User not found")

        # elif not verify_password(password, user["password"]):
        #     st.error("Invalid credentials")
        condition = authobj.authenticate_user(username, password)
        if condition is not True:
            st.error("failed, make sure your username/password is correct")
        else:
            st.session_state.authenticated = True
            st.session_state.user = {
                "username": username,
                "auth": True
            }
            st.success("Logged in successfully")
            st.rerun()

def signup(authobj):
    st.subheader("Sign-up")

    username = st.text_input("Username")
    # email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not username  or not password:
            st.error("All fields are required")

        elif password != confirm:
            st.error("Passwords do not match")

        elif authobj.check_user_exists(username):
            st.error("username already exists")

        else:
            authobj.create_user(username, password)
            st.success("Account created. Please login.")
            
