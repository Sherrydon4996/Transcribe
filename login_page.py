import streamlit as st
import MySQLdb
from streamlit_cookies_manager import EncryptedCookieManager
import os
from PIL import Image
import json
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("PASSWORD")

st.set_page_config(
    page_title="@HarryProTranscribe",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)
try:
    from validate_credentials import validate_email, hashing_password, empty_fields_alert, validate_password
    from home_page import recall_functions
except:
    st.info("Unexpected error has occurred, try refreshing the page")

connection = MySQLdb.connect(
    host="localhost",
    user="root",
    password=password,
    database="media_files"
)
my_cursor = connection.cursor()

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


def save_credentials_to_database(username, email, first_name, new_password):
    my_cursor.execute("insert into user_details(username, email, full_names, password) VALUES(%s,%s,%s,%s)",
                      (username, email, first_name, new_password))
    my_cursor.execute("update user_details set balance=%s where username=%s", (10, username))
    connection.commit()


def get_logins(username):
    my_cursor.execute("SELECT password from user_details where username=%s", (username,))
    results = my_cursor.fetchone()
    if results:
        return results[0]
    return


def update_password(password, username):
    my_cursor.execute("select * from user_details where username=%s", (username,))
    results = my_cursor.fetchall()
    if results:
        if username in results[0]:
            my_cursor.execute("update user_details set password=%s where username=%s", (password, username))
            connection.commit()
            return True
    else:
        return False


def check_duplicate_registrations(username, email):
    my_cursor.execute("select full_names, email from user_details where username=%s", (username,))
    results = my_cursor.fetchall()
    if results:
        if username in results[0]:
            return False
        elif email in results[0]:
            return False
    else:
        return True


def save_login_data(username):
    my_cursor.execute("select full_names from user_details where username=%s", (username, ))
    results = my_cursor.fetchone()
    if results:
        full_names = results[0]
        my_cursor.execute("insert into login_info(username, full_names) VALUES(%s, %s)", (username, full_names))
        connection.commit()


def show_registration_form():
    st.subheader(":blue[Proceed to login if you already have an account]")
    col4, col5 = st.columns(2)
    with col4:
        size = (800, 450)
        img = Image.open("images/register.jpg")
        resized_image = img.resize(size, Image.LANCZOS)
        st.image(resized_image)
    with col5:
        with st.form("Enter your details"):

            st.subheader(":red[SIGN_UP]")
            username = st.text_input(":red[*]:green[Enter your username]", key="username")
            email = st.text_input(":red[*]:green[Enter your email]")
            full_name = st.text_input(":red[*]:green[Enter full names]")
            user_password = st.text_input(":red[*]:green[Enter your password]", type="password")
            new_password = hashing_password(user_password)
            if st.form_submit_button("Submit"):
                field_names = [username, email, username, full_name, user_password
                               ]
                if empty_fields_alert(field_names) and \
                        validate_password(user_password) and \
                        validate_email(email):
                    if check_duplicate_registrations(username, email):
                        save_credentials_to_database(username, email, full_name, new_password)
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
        img = Image.open("images/register2.jpg")
        resized_image = img.resize(size, Image.LANCZOS)
        st.image(resized_image)

    with col7:
        login_username = st.text_input(":green[Enter Username]")
        password = st.text_input(":green[Enter Password]", type="password")
        login_password = hashing_password(password)
        if st.button("Submit your details"):
            database_password = get_logins(login_username)
            if login_username and password:
                if database_password == login_password:
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
        img = Image.open("images/image.png")
        new_image = img.resize(size, Image.LANCZOS)
        st.image(new_image)
    with col9:
        with st.form("reset"):
            st.write(":green[reset your password here]")
            user_name = st.text_input(":green[Enter your username to reset password]")
            password = st.text_input(":green[Enter a new password]", type="password")
            new_password = hashing_password(password)
            if st.form_submit_button("reset_password"):
                if user_name and password:
                    if update_password(new_password, user_name):
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
            my_cursor.execute("select full_names, email from user_details where username=%s", (new_username,))
            results = my_cursor.fetchall()
            if results:
                list_details = results[0]
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
                                <strong>Full Names:</strong> {list_details[0]} &emsp;&emsp;
                                <strong>Email:</strong> {list_details[1]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                col1, col2, col3, col4 = st.columns([2, 0.5, 1, 2])
                main_balance = f"ksh. {350}"
                my_cursor.execute("select balance from user_details where username=%s",(new_username, ))
                results = my_cursor.fetchone()
                if results is not None:
                    kenyan_currency = results[0]
                    USD = round(kenyan_currency / 127, 2)
                    
                else:
                    main_balance = "ksh. 0.00"
                with col1:
                    st.subheader(f":green[Welcome {new_username.title()}]")
                with col2:
                    currency = st.selectbox("Select currency", ["KSH", "USD"])
                with col4:
                    if currency == "KSH":
                         st.subheader(f":green[you balance: ksh. {kenyan_currency}]")
                    else:
                        st.subheader(f":green[you balance: ${USD}]")
                        

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
                comment = st.text_area("", placeholder="Write your comment, press control enter and then press add comment button that will appear below.")
                st.subheader("User comments and recomendations are available here.")
                with open("user_comments.json", "r") as file:
                    data = json.load(file)
                
                if comment:
                    my_cursor.execute("select full_names from user_details where username=%s", (new_username, ))
                    results = my_cursor.fetchone()[0]
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
            st.experimental_rerun()


if __name__ == "__main__":
    logged_in()
