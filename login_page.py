import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import os
from PIL import Image
import json
from dotenv import load_dotenv
from pymongo import MongoClient
import bcrypt
from datetime import datetime

import ssl

string_word ="mongodb+srv://edwinnjogu4996:ghvfCPPaVYVaMWgd@transcription.sezw1.mongodb.net/?retryWrites=true&w=majority&appName=Transcription"
# Create SSL context to enforce TLS 1.2
ssl_context = ssl.create_default_context()
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2  # Enforce TLS 1.2 or later

client = MongoClient(
    string_word,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,  # Ensure certificates are validated
    tls=True,
    ssl_context=ssl_context
)


st.set_page_config(
    page_title="@HarryProTranscribe",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from validate_credentials import validate_email, hashing_password, empty_fields_alert, validate_password
from home_page import recall_functions





def database_table_structure():
    """
    database_structure
    {
    full_names: "",
    username: "",
    email: "",
    amount: 0,
    audio_filename:"",
    srt_file:"",
    json_file:"",
    password: "",
    current_time:"",
    }

    """


cookies = EncryptedCookieManager(
    prefix="My_weApp",
    password="12345"
)
if not cookies.ready():
    st.stop()

if "is_logged_in" in cookies and cookies["is_logged_in"] == "True":
    st.session_state.is_logged_in = True
else:
    st.session_state.is_logged_in = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "reset_password" not in st.session_state:
    st.session_state.reset_password = False


def header():
    features = [
        "High quality English Transcription",
        "Swahili Transcription",
        "High Quality Video Subtitles Generation (with translations to your choice language)",
        "Text to speech services",
        "Language Translation",
        "Language Detection",
    ]

    # Create the list in pairs for four columns
    columns = [features[i:i + 2] for i in range(0, len(features), 2)]

    # Create the HTML for the columns
    header_content = "<div style='display: flex; justify-content: center; flex-wrap: wrap;'>"
    for column in columns:
        header_content += "<div style='flex: 1; min-width: 150px; margin: 10px;'><ul>"
        for feature in column:
            header_content += f"<li>{feature}</li>"
        header_content += "</ul></div>"
    header_content += "</div>"

    st.markdown(f"""
        <div style="
            background: #34495E;
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
            color: #ECF0F1;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <h2 style="margin-bottom: 10px; color:#E67E22;">Welcome to @Harry's Transcription Service Provider</h2>
            <p style="font-size: 16px; font-weight: bold;">The following services are available:</p>
            <div style="
                background: #F7F9F9; 
                border-radius: 5px; 
                padding: 10px; 
                margin: 10px auto; 
                color: green;
                text-align: left;
                font-size: 14px;">
                {header_content}
            </div>
            <p style="font-size: 12px; font-style: italic;">Thank you for visiting our site, and we hope you enjoy our services.</p>
        </div>
        <br></br>
    """, unsafe_allow_html=True)


header()


def button_appearance():
    login_button_css = """
        <style>
        div.stButton > button {
            background-color: #4CAF50; /* Green background */
            color: white; /* White text */
            padding: 10px 24px; /* Padding */
            font-size: 16px; /* Increase font size */
            border: none; /* Remove borders */
            border-radius: 8px; /* Rounded corners */
            cursor: pointer; /* Pointer/hand icon on hover */
            transition: background-color 0.3s ease; /* Smooth transition for hover effect */
        }

        div.stButton > button:hover {
            background-color: #45a049; /* Darker green on hover */
        }

        div.stButton > button:active {
            background-color: #3e8e41; /* Even darker green when clicked */
        }
        </style>
    """

    st.markdown(login_button_css, unsafe_allow_html=True)


def save_credentials_to_database(username, email, full_names, new_password):
    # Hash the password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    db = client["Transcription"]
    user_collection = db["user_registration"]

    # Insert new user into the collection
    user_document = {
        "username": username,
        "email": email,
        "full_names": full_names,
        "password": hashed_password,
        "amount": 10,  # Set initial balance to 10
        "audio_filename": "",
        "srt_file": "",
        "json_file": "",
        "current_time": datetime.now()  # Store current timestamp
    }

    # Insert the document into MongoDB
    user_collection.insert_one(user_document)


def get_logins(username):
    # Connect to MongoDB
    db = client["Transcription"]
    user_collection = db["user_registration"]

    # Find the user by username
    result = user_collection.find_one({"username": username}, {"password": 1, "_id": 0})

    if result:
        return result["password"]
    return None


def update_password(new_password, username):
    # Connect to MongoDB
    db = client["Transcription"]
    user_collection = db["user_registration"]

    # Check if the user exists
    result = user_collection.find_one({"username": username})
    if result:
        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Update the password
        user_collection.update_one({"username": username}, {"$set": {"password": hashed_password}})
        return True
    return False


def check_duplicate_registrations(username, email):
    # Connect to MongoDB
    db = client["Transcription"]
    user_collection = db["user_registration"]

    # Check for username or email duplication
    result = user_collection.find_one({"$or": [{"username": username}, {"email": email}]})

    if result:
        return False  # Duplicate found
    return True  # No duplicates found


def save_login_data(username):
    # Connect to MongoDB
    db = client["Transcription"]

    # Collections
    user_collection = db["user_registration"]
    login_collection = db["login_info"]

    # Find the user's full name
    result = user_collection.find_one({"username": username}, {"full_names": 1, "_id": 0})
    if result:
        full_names = result["full_names"]

        # Insert login info into a separate collection
        login_data = {
            "username": username,
            "full_names": full_names,
            "login_time": datetime.now()  # Record login time
        }
        login_collection.insert_one(login_data)


def show_registration_form():
    st.subheader(":blue[Proceed to login if you already have an account]")
    col4, col5 = st.columns(2)
    with col4:
        size = (800, 450)
        img = Image.open("static/register.jpg")
        resized_image = img.resize(size, Image.LANCZOS)
        st.image(resized_image)
    with col5:
        with st.form("Enter your details"):

            st.subheader(":red[SIGN_UP]")
            username = st.text_input(":red[*]:green[Enter your username]", key="username")
            email = st.text_input(":red[*]:green[Enter your email]")
            full_name = st.text_input(":red[*]:green[Enter full names]")
            user_password = st.text_input(":red[*]:green[Enter your password]", type="password")
            # new_password = hashing_password(user_password)
            if st.form_submit_button("Submit"):
                field_names = [username, email, username, full_name, user_password
                               ]
                if empty_fields_alert(field_names) and \
                        validate_password(user_password) and \
                        validate_email(email):
                    if check_duplicate_registrations(username, email):
                        save_credentials_to_database(username, email, full_name, user_password)
                        st.success(":green[successfully registered]")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(":red[username or email has already been used to register another account]")

                else:
                    st.error(
                        ":red[Make sure there are no empty fields, password = 6 or more characters and email is valid]")


def login():
    button_appearance()
    col6, col7 = st.columns(2)
    with col6:
        size = (750, 350)
        img = Image.open("static/register2.jpg")
        resized_image = img.resize(size, Image.LANCZOS)
        st.image(resized_image)

    with col7:
        login_username = st.text_input(":green[Enter Username]")
        password = st.text_input(":green[Enter Password]", type="password")
        # login_password = hashing_password(password)
        if st.button("Submit your details"):
            database_password = get_logins(login_username)
            if login_username and password:
                if database_password and bcrypt.checkpw(password.encode("utf-8"), database_password):
                    save_login_data(login_username)
                    get_user_name(login_username)
                    st.success("Login success")
                    st.session_state.is_logged_in = True
                    cookies["is_logged_in"] = "True"
                    cookies.save()
                    st.rerun()
                else:
                    st.warning(":red[Invalid email or password]")
            else:
                st.error(":red[Please enter username and password!]")

        st.write(":blue[forgotten your password?]")
        if st.button("reset_here"):
            st.session_state.reset_password = True
            st.rerun()


def get_user_name(username):
    cookies["user_name"] = username


def reset_password():
    button_appearance()
    col8, col9 = st.columns(2)
    with col8:
        size = (800, 300)
        img = Image.open("static/image.png")
        new_image = img.resize(size, Image.LANCZOS)
        st.image(new_image)
    with col9:
        with st.form("reset"):
            st.write(":green[reset your password here]")
            user_name = st.text_input(":green[Enter your username to reset password]")
            password = st.text_input(":green[Enter a new password]", type="password")
            # new_password = hashing_password(password)
            if st.form_submit_button("reset_password"):
                if user_name and password:
                    if update_password(password, user_name):
                        if validate_password(password):
                            st.success("Password reset was successful")
                            st.session_state.reset_password = False
                            st.rerun()

                        else:
                            st.error(":red[password must be 6 characters or more]")
                    else:
                        st.error(":red[User not registered]")
                else:
                    st.error(":red[Please enter your username and new password!]")


def page_appearance():
    st.markdown("""
    <style>
     .stApp{
      background-color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)


page_appearance()

if "user_currency" not in st.session_state:
    st.session_state.user_currency = 0
if "USD" not in st.session_state:
    st.session_state.USD = 0


def logged_in():
    button_appearance()
    if not st.session_state.is_logged_in:
        register_message = "Not registered yet? Join us today and start transcribing with ease enjoying cheap and affordable transcription service <b style='color:black;'> @ ksh10/per audio minute </b> with all the other services being free!</b>"
        register_css = f"""
            <div style="width:100%; height:auto; background-color:#1F618D; padding:20px; border-radius:8px; 
                        text-align:center; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); display: flex; justify-content: space-between; align-items: center;">
                <p style="color:gold; font-size:16px; font-weight:500; margin: 0; text-align: left;">Create an account</p>
                <p style="color:#F7F9F9; font-size:16px; font-weight:500; margin: 0;">{register_message}</p>
                <p style="color:gold; font-size:16px; font-weight:500; margin: 0; text-align: right;">Login</p>
            </div>
        """
        st.markdown(register_css, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            if st.button("Register"):
                st.session_state.show_register = True
                st.session_state.reset_password = False
                st.rerun()
        with col6:

            if st.button("Login"):
                st.session_state.show_register = False
                st.session_state.reset_password = False
                st.rerun()
        if st.session_state.show_register:
            show_registration_form()
        elif st.session_state.reset_password:
            reset_password()
        else:
            login()

    else:
        new_username = cookies["user_name"]
        if new_username:
            db = client["Transcription"]
            user_collection = db["user_registration"]

            # Find the user by username
            results = user_collection.find_one({"username": new_username}, {"full_names": 1, "email": 1, "_id": 0})

            if results:
                # Create list_details from the result
                list_details = {
                    "full_names": results["full_names"],
                    "email": results["email"]
                }

                # USER PROFILE DETAILS
                with st.expander("See your profile details"):
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #f8f9fa;
                            padding: 15px;
                            border-radius: 10px;
                            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                            font-family: Arial, sans-serif;
                            color: #333;">
                            <h3 style="text-align: center; color: #007BFF;">Profile Details</h3>
                            <p style="text-align: left;">
                                <strong>Username:</strong> {new_username} &emsp;&emsp;
                                <strong>Full Names:</strong> {list_details["full_names"]} &emsp;&emsp;
                                <strong>Email:</strong> {list_details["email"]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                col1, col2, col3, col4 = st.columns([2, 0.5, 1, 2])
                main_balance = f"ksh. {350}"
                db = client["Transcription"]
                db_collection = db["user_registration"]

                results = db_collection.find_one({"username": new_username}, {"amount": 1, "_id": 0})
                if results:
                    st.session_state.user_currency = results['amount']
                    st.session_state.USD = round(st.session_state.user_currency / 127, 2)

                else:
                    main_balance = "ksh. 0.00"
                with col1:
                    st.subheader(f":green[Welcome {new_username.title()}]")
                with col2:
                    currency = st.selectbox("Select currency", ["KSH", "USD"])
                with col4:
                    if currency == "KSH":
                        st.subheader(f":green[you balance: ksh. {st.session_state.user_currency}]")
                    else:
                        st.subheader(f":green[you balance: ${st.session_state.USD}]")

                st.markdown(
                    f"""
                    <div style="background-color: #34495E; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: #ECF0F1; text-align: center;">Hello and Welcome {new_username}</h3>
                        <p style="color: #BDC3C7; font-size: 16px; text-align: center;">
                            Please note that the method of payment has yet to be configured. The app is still in the testing phase.
                            For top-up and access to services, contact the admin @ <strong>+254711140899</strong> for both calls and WhatsApp.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("### leave your comment or recomendation here:")
                # USER COMMENTS
                comment = st.text_area("",
                                       placeholder="Write your comment, press control enter and then press add comment button that will appear below.")
                st.subheader("User comments and recomendations are available here.")
                with open("user_comments.json", "r") as file:
                    data = json.load(file)

                if comment:
                    db = client["Transcription"]
                    db_collection = db["user_registration"]
                    results_mg = db_collection.find_one({"username": new_username}, {"full_names": 1, "_id": 0})
                    results = results_mg["full_names"]
                    if st.button("add_comment"):
                        names = [name['full_name'] for name in data["user_views"]]
                        if results in names:
                            st.error("you can only comment once!")
                        else:
                            data["user_views"].append({"full_name": results, "comment": comment})
                            with open("user_comments.json", "w") as file2:
                                json.dump(data, file2, indent=4)
                        comment = ""
                with st.expander("View comments"):
                    for index, data in enumerate(data["user_views"]):
                        st.markdown(f"""
                                    <div style="background-color:black; width:100%; height:200px; position:realtive">
                                        <h4 style="color:red; position:absolute; left:2%; top:30%; font-family:sans-serif; text-transform:capitalize; text-decoration:underline;">{index + 1}. {data['full_name']}</h4>
                                        <p style="font-family: courier; position:absolute; left:2%; top:50%; color:green;">{data['comment']}<p>
                                    </div>
                                    
                                    """, unsafe_allow_html=True)



        else:
            st.error("no username", new_username)
        this_username = cookies["user_name"]
        if this_username:
            recall_functions(this_username)
        if st.button("Logout"):
            st.session_state.is_logged_in = False
            st.session_state.show_register = False
            st.session_state.reset_password = False
            cookies["is_logged_in"] = "False"
            cookies["user_name"] = ""
            cookies.save()
            st.rerun()



if __name__ == "__main__":
    logged_in()
