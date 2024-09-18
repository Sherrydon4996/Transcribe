import streamlit as st
import json


def entity_header(entity_type, color):
    banner_html = f"""
    <div style="background-color:{color}; padding:10px; border-radius:5px; width:100%; text-align:center; display:flex; align-items:center; justify-content:center;">
        <h2 style="color:white; margin:0;">{entity_type}</h2>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


def display_no_category_banner(category):
    banner_html = f"""
    <div style="background-color:white; padding:20px; border-radius:15px; margin-top:30px; font-family:'Courier New', Courier, monospace; text-align:center; width:100%; height:300px;">
        <h2 style="color:black; text-align:center; position:relative; top:70px; ">No {category} detected</h2>
        <p style="color:green; text-align:center; position:relative; top:70px; ">Make sure you have a transcribed file already</p>
        <p style="color:green; text-align:center; position:relative; top:70px; ">If you already have a transcribed file, then your content does not apply for {category} category</p>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


def entity_detection1(temp_file):
    if temp_file:
        full_list = [
            ["account_number", "banking_information", "blood_type", "credit_card_cvv"], ["credit_card_expiration",
                                                                                         "credit_card_number", "date",
                                                                                         "date_interval"],
            ["date_of_birth", "drivers_license", "drug", "duration"], ["email_address", "event",
                                                                       "filename", "gender_sexuality"],
            ["healthcare_number", "injury", "ip_address", "language"], ["location", "marital_status",
                                                                        "medical_condition", "medical_process"],
            ["money_amount", "nationality", "number_sequence", "occupation"], ["organization", "passport_number",
                                                                               "password", "person_age"],
            ["person_name", "phone_number", "physical_attribute", "political_affiliation"],
            ["religion", "statistics", "time",
             "url"], ["us_social_security_number", "username",
                      "vehicle_id", "zodiac_sign"]
        ]
        col1, col2 = st.columns(2)
        our_data = []
        # with open(temp_file, "r", encoding="utf-8") as file2:
        #     entities = json.load(file2)
        entities = temp_file
        entity_infor = entities["entities"]
        if entity_infor is not None:
            for data in entities['entities']:
                our_data.append(data["entity_type"])

            colors = ["#007bff", "#28a745", "#ff5733", "gold"]

            cols = st.columns(4)
            with col1:
                if st.button("Display all data"):
                    for lists in full_list:
                        for index, (name, color) in enumerate(zip(lists, colors)):
                            col = cols[index]
                            with col:
                                if name in our_data:
                                    entity_header(name, "blue")

                                    for id, data in enumerate(entities['entities']):
                                        if data["entity_type"] == name:
                                            our_int = data["text"]
                                            time_start = data["start"]
                                            time_end = data["start"]
                                            div_content = f"""
                                                                         <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:20px;
                                                                          font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                                                           <h4 style="color:green; text-align:left;">{id + 1}. {our_int.title()}</h4>
                                                                           <p style="color:red; text-align:left; font-size:14px;">
                                                                                Time detected: {time_start / 1000} seconds or {time_start / 60000:.3f} minutes<br>
                                                                                Time ended: {time_end / 1000} seconds or {time_end / 60000:.3f} minutes<br>
        
                                                                           </p>
                                                                                                             """
                                            st.markdown(div_content, unsafe_allow_html=True)

                                else:

                                    entity_header(name, "red")
                                    div_content = f"""
                                                                          <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:20px;
                                                                           font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                                                            <h4 style="color:green; text-align:left;">No Available Data</h4>
                                                                          """
                                    st.markdown(div_content, unsafe_allow_html=True)
            with col2:
                if st.button("Display available data only"):
                    for lists in full_list:
                        for index, (name, color) in enumerate(zip(lists, colors)):
                            col = cols[index]
                            with col:
                                if name in our_data:
                                    entity_header(name, "blue")

                                    for id, data in enumerate(entities['entities']):
                                        if data["entity_type"] == name:
                                            our_int = data["text"]
                                            time_start = data["start"]
                                            time_end = data["start"]
                                            div_content = f"""
                                                                         <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:20px;
                                                                          font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                                                           <h4 style="color:green; text-align:left;">{id + 1}. {our_int.title()}</h4>
                                                                           <p style="color:red; text-align:left; font-size:14px;">
                                                                                Time detected: {time_start / 1000} seconds or {time_start / 60000:.3f} minutes<br>
                                                                                Time ended: {time_end / 1000} seconds or {time_end / 60000:.3f} minutes<br>
        
                                                                           </p>
                                                                                                             """
                                            st.markdown(div_content, unsafe_allow_html=True)
        else:
            display_no_category_banner("entity_detection=>(no entity in file)")
    else:
        display_no_category_banner("entity_detection_no_temp=>(no file)")


