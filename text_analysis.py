import streamlit as st
import json
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from entity_detection import entity_detection1


def language_analysis_menu():
    with st.container():
        analysis_type = option_menu(
            menu_title="Text_analysis",
            options=["Sentiment_analysis", "Entity_detection", "Content_safety", "Topic_detection", "Speaker_labels",
                     "Summarization"],
            icons=["bi-emoji-smile", "bi-search", "bi-shield-lock", "bi-key", "bi-journal-text"],
            key="language_analysis"
        )
        return analysis_type


def page_header():
    content = (" In text analysis, various techniques are employed to extract meaningful insights from written content."
               " Sentiment analysis assesses the emotional tone of a text, helping to understand whether the sentiment"
               " expressed is positive, negative, or neutral. Entity detection identifies and categorizes significant elements like names,"
               " organizations, and locations within the text. Content safety analysis ensures that the content"
               " is appropriate and adheres to guidelines, preventing harmful or offensive material from being shared."
               " Lastly, topic detection and summarization identify the main themes and key points within a text,"
               " making it easier to understand the central subjects and obtain concise overviews.")
    st.markdown(f"""
    <div style="background-color:#4CAF50;overflow:auto; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white; font-family: 'Arial', sans-serif;">
            🎤 This is the last section where you can access all text analysis of your audio file. 🎧
        </h1>
        <p style="color: white; font-size: 18px;">
            {content}
        </p>
    </div>
    <br></br>
    """, unsafe_allow_html=True)




def display_no_category_banner(category):
    banner_html = f"""
    <div style="background-color:white;overflow:auto; padding:20px; border-radius:15px; margin-top:30px; font-family:'Courier New', Courier, monospace; text-align:center; width:100%; height:300px;">
        <h2 style="color:black; text-align:center; position:relative; top:70px; ">No {category} detected</h2>
        <p style="color:green; text-align:center; position:relative; top:70px; ">Make sure you have a transcribed file already</p>
        <p style="color:green; text-align:center; position:relative; top:70px; ">If you already have a transcribed file, then your content does not apply for {category} category</p>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


def analysis_type_header(entity_type, color, content):
    banner_html = f"""
    </div>
      <div style="background-color:{color};overflow:auto; padding:10px; border-radius:10px; text-align:center;">
                        <h2 style="color:orange;">Analysis_type: {entity_type}</h2>
                        <p style="color:white; font-size:18px;">{content}</p>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


def sentiment_analysis(analysis_type, temp_file):
    if analysis_type == "Sentiment_analysis":
        content = (
            "In this section, you'll explore the emotional tone of the content through sentiment analysis,"
            " which identifies whether the text is positive, negative, or neutral. It not only"
            " provides the sentiment score but also visualizes this information with bar and pie charts"
            " to help you quickly grasp the overall mood. The sentiment score displayed below offers a detailed"
            " numerical insight into the emotions conveyed by the content, making it easier to understand the"
            " underlying feelings or attitudes expressed.")
        banner_html = f"""
        </div>
          <div style="background-color:green; padding:10px; border-radius:10px;overflow:auto; text-align:center;">
                            <h2 style="color:orange;">Analysis_type: Sentiment_analysis</h2>
                            <p style="color:white; font-size:18px;">{content}</p>
        </div>
        """
        st.markdown(banner_html, unsafe_allow_html=True)
        if temp_file:
            try:
                # with open(temp_file, "r", encoding="utf-8") as file2:
                #     sentiments = temp_file
                sentiments = temp_file
                if sentiments:
                    # Sentiment Analysis Overview
                    col1, col2, col57 = st.columns([1, 1, 1])

                    with col1:
                        st.subheader("Sentiment Analysis Overview")
                        df = pd.DataFrame(sentiments["sentiment_analysis_results"])
                        overview_df = pd.DataFrame(df[["sentiment", "text"]])
                        st.dataframe(overview_df)
                    with col2:
                        st.subheader("Summary of text_sentiments..")
                        data = sentiments["sentiment_analysis_results"]
                        POSITIVE = 0
                        NEUTRAL = 0
                        NEGATIVE = 0
                        for index, dat in enumerate(data):
                            if dat["sentiment"] == "POSITIVE":
                                POSITIVE += 1
                            elif dat["sentiment"] == "NEUTRAL":
                                NEUTRAL += 1
                            elif dat["sentiment"] == "NEGATIVE":
                                NEGATIVE += 1

                        div_content = f"""
                                        <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px;
                                         font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                            <h4 style="color:#343a40; text-align:left;">Total number of sentiments: {df.shape[0]}</h4>
                                            <h5 style="color:#343a40; text-align:left;">Positive sentiments: {POSITIVE}</h5>
                                            <h5 style="color:#343a40; text-align:left;">Neutral sentiments: {NEUTRAL}</h5>
                                            <h5 style="color:#343a40; text-align:left;">negative sentiments: {NEGATIVE}</h5>

                                        </div>
                                        """
                        st.markdown(div_content, unsafe_allow_html=True)

                    with col57:
                        text_content = ' '.join([word['text'] for word in sentiments["words"]])
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.text_area("Text content", text_content, height=400)

                    # Sentiment Distribution and Summary
                    col3, col4, col5 = st.columns([1, 1, 1])

                    with col3:
                        st.subheader("Sentiment Distribution")
                        grouped = pd.DataFrame(df["sentiment"].value_counts()).reset_index()
                        grouped.columns = ["sentiment", "count"]
                        color_mapping = {"NEGATIVE": "red", "POSITIVE": "green", "NEUTRAL": "purple"}
                        fig = px.bar(grouped, x="sentiment", y="count", color="sentiment",
                                     color_discrete_map=color_mapping)
                        fig.update_layout(
                            showlegend=False,
                            autosize=False,
                            width=400,
                            height=400,
                            margin=dict(l=50, r=50, b=50, t=50, pad=4)
                        )
                        st.plotly_chart(fig)

                    with col4:
                        st.subheader("Sentiment Percentages")
                        sentiment_counts = df["sentiment"].value_counts(normalize=True) * 100
                        sentiment_counts = sentiment_counts.reset_index()
                        sentiment_counts.columns = ["sentiment", "percentage"]
                        fig = px.pie(sentiment_counts, names="sentiment", values="percentage", color="sentiment",
                                     color_discrete_map=color_mapping)
                        fig.update_layout(
                            autosize=False,
                            width=400,
                            height=400,
                            margin=dict(l=50, r=50, b=50, t=50, pad=4)
                        )
                        st.plotly_chart(fig)

                    # Sentiment Score
                    with col5:
                        st.subheader("Sentiment Score Calculation")
                        positive_percentage = \
                            sentiment_counts[sentiment_counts['sentiment'] == "POSITIVE"]['percentage'].iloc[0] if not \
                                sentiment_counts[sentiment_counts['sentiment'] == "POSITIVE"].empty else 0
                        negative_percentage = \
                            sentiment_counts[sentiment_counts['sentiment'] == "NEGATIVE"]['percentage'].iloc[0] if not \
                                sentiment_counts[sentiment_counts['sentiment'] == "NEGATIVE"].empty else 0
                        neutral_percentage = \
                            sentiment_counts[sentiment_counts['sentiment'] == "NEUTRAL"]['percentage'].iloc[0] if not \
                                sentiment_counts[sentiment_counts['sentiment'] == "NEUTRAL"].empty else 0

                        sentiment_score = neutral_percentage + positive_percentage - negative_percentage

                        fig = go.Figure()
                        fig.add_trace(go.Indicator(
                            mode="delta",
                            value=sentiment_score,
                            title={"text": "Sentiment Score"},
                            delta={"reference": 50},
                            domain={"row": 1, "column": 1}
                        ))
                        fig.update_layout(
                            autosize=False,
                            width=400,
                            height=400,
                            margin=dict(l=50, r=50, b=50, t=50, pad=4)
                        )
                        st.plotly_chart(fig)

            except json.JSONDecodeError as e:
                st.error(f"Error loading JSON: {e}")
        else:
            display_no_category_banner(analysis_type)


def entity_header(entity_type, color):
    banner_html = f"""
    <div style="background-color:{color};overflow:auto; padding:10px; border-radius:5px; width:100%; text-align:center; display:flex; align-items:center; justify-content:center;">
        <h4 style="color:white; margin:0;">Entity type: {entity_type}</h4>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


def entity_detection(analysis_type, temp_file):
    if analysis_type == "Entity_detection":
        explanation = (
            "Entity Detection (also known as Named Entity Recognition, or NER) is a process used in natural"
            " language processing (NLP) to identify and classify key elements, or 'entities,' within a text."
            " These entities are typically proper nouns such as names of people, organizations, locations, dates,"
            "and other specific terms. Press the buttons below to show available data or display all data")
        analysis_type_header("Entity_detection", "green", explanation)
        entity_detection1(temp_file)
        # if temp_file:
        #
        #     try:
        #         entity_detection1(temp_file)
        #     except Exception as e:
        #         st.error(f"Error:{e}")
        #
        # else:
        #     display_no_category_banner("Entity_detection")


# Example usage
def content_safety(analysis_type, temp_file):
    if analysis_type == "Content_safety":
        content = (
            "This section displays the content safety analysis, highlighting specific phrases or words that may be sensitive or harmful,"
            " such as hate speech or violence. Each flagged item is accompanied by a confidence score indicating the likelihood of the"
            " content being inappropriate. This tool helps ensure the content shared on your platform is safe and adheres to community guidelines.")
        analysis_type_header("content_safety", "green", content)
        if temp_file:
            summary = temp_file
            safety_content = summary["content_safety_labels"]["results"]
            if not safety_content:
                display_no_category_banner("Content_safety=>(no safety cont in file)")
            else:
                assembly_labels = [
                    "accidents", "alcohol", "financials", "crime_violence",
                    "drugs", "gambling", "hate_speech", "health_issues",
                    "manga", "marijuana", "disasters", "negative_news", "nsfw",
                    "pornography", "profanity", "sensitive_social_issues", "terrorism",
                    "tobacco", "weapons"
                ]
                summary_results = summary["content_safety_labels"]["results"]
                col1, col2, col3 = st.columns([3, 0.5, 3])
                with col1:

                    for index, data in enumerate(summary_results):
                        time = data["timestamp"]
                        labels = data["labels"]
                        div_content = f"""
                                        <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px;
                                         font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                          <h2 style="color:green; text-align:left;">{index + 1}. Sensitive phrase or word</h2>
                                            <h6 style="color:#343a40; text-align:left;">{data["text"]}</h6>
                                        """
                        st.markdown(div_content, unsafe_allow_html=True)
                        for index, lab in enumerate(labels):
                            div_content = f"""
                                      <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px;
                                       font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                          <h4 style="color:#343a40; text-align:left;">{index + 1}. Category and judgment</h4>
                                          <p style="color:#495057; text-align:left; font-size:16px;">
                                              category: {lab["label"]}
                                          </p>
                                          <p style="color:#6c757d; text-align:left; font-size:14px;">
                                              judgment: {lab["confidence"] * 100:.2f}%
                                          </p>
                                      </div>
                                      """
                            st.markdown(div_content, unsafe_allow_html=True)
                        div_content = f"""
                                          <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px;
                                           font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                              <h4 style="color:#343a40; text-align:left;"> Exact time on the content</h4>
                                              <p style="color:red; text-align:left; font-size:14px;">
                                                  Start time: {time['start'] / 1000} seconds or {time['start'] / 60000:.3f} minutes<br>
                                                  End time: {time['end'] / 1000} seconds or {time['end'] / 60000:.3f} minutes
                                              </p>
                                          </div>
                                          """
                        st.markdown(div_content, unsafe_allow_html=True)
                        st.write("##")
                summary_data = summary["content_safety_labels"]["summary"]
                with col3:
                    for index, data2 in enumerate(summary_data):
                        div_content = f"""
                                       <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px;
                                        font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                         <h2 style="color:green; text-align:left;">{index + 1}. Sensitive content Category</h2>
                                           <h4 style="color:#343a40; text-align:left;">Category: {data2}</h4>
                                       """
                        st.markdown(div_content, unsafe_allow_html=True)

                        if data2 in assembly_labels:
                            div_content = f"""
                                              <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px;
                                               font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                                  <h4 style="color:#343a40; text-align:left;"> Number of times it appears and its judgment</h4>
                                                  <p style="color:#495057; text-align:left; font-size:16px;">
                                                      counted_words or phrases: {summary_data[data2]['count']}<br>
                                                      judgment: {summary_data[data2]['severity']}
                                                  </p>

                                              </div>
                                              """
                            st.markdown(div_content, unsafe_allow_html=True)
                        st.write("##")
        else:
            display_no_category_banner("Content_safety=> no file")


def Topic_detection(analysis_type, temp_file):
    if analysis_type == "Topic_detection":
        content = (
            "This section provides an overview of the main topics detected within your content using topic detection AI feature."
            " Each identified topic helps categorize the content into relevant themes or subjects,"
            " making it easier to understand the key areas of discussion. This is particularly useful for organizing"
            " large volumes of content or gaining insights into dominant themes")
        analysis_type_header("Topic_analysis", "green", content)
        if temp_file:
            # with open(temp_file, "r", encoding="utf-8") as file2:
            #     summary = json.load(file2)
            summary = temp_file
            summary_data = summary["iab_categories_result"]["results"]
            if not summary_data:
                display_no_category_banner("Topic detection=> no topics in file")
            else:
                for data in summary_data:
                    labels_html = ""
                    for index, lab in enumerate(data["labels"]):
                        labels_html += f"<p style='color:#495057; text-align:left; font-size:16px;'>{index + 1}. {lab['label']}</p>"

                    div_content = f"""
                    <div style="background-color:#e9ecef;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px; font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                        <h4 style="color:#343a40; text-align:left;">Detected Topics</h4>
                        {labels_html}
                    </div>
                    """
                    st.markdown(div_content, unsafe_allow_html=True)
        else:
            display_no_category_banner("Topic_detection=>(no file)")


def speaker_labels(analysis_type, temp_file):
    if analysis_type == "Speaker_labels":
        content = ("In this section, you'll see the different speakers identified in your audio content using"
                   " AI's speaker labeling feature. Each segment of the content is associated with a specific speaker,"
                   " making it easier to follow who said what. This feature is particularly useful for transcribing conversations,"
                   " interviews, or meetings where multiple participants are involved, allowing for a clear and organized representation of the dialogue.")
        analysis_type_header("Speaker labels", "green", content)
        if temp_file:
            # with open(temp_file, "r", encoding="utf-8") as file2:
            #     summary = json.load(file2)
            summary = temp_file
            if summary:
                summary_data = summary["utterances"]
                if not summary_data:
                    display_no_category_banner("speaker labels=>(no labels in file)")
                else:
                    for data in summary_data:
                        div_content = f"""
                        <div style="background-color:#f8f9fa;overflow:auto; padding:15px; border-radius:10px; margin-bottom:20px; font-family:'Arial', sans-serif; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                            <h4 style="color:#343a40; text-align:left;">Speaker: {data['speaker']}</h4>
                            <p style="color:#495057; text-align:left; font-size:16px;">
                                {data['text']}
                            </p>
                            <p style="color:red; text-align:left; font-size:14px;">
                                Start time: {data['start'] / 1000} seconds or {data['start'] / 60000:.3f} minutes<br>
                                End time: {data['end'] / 1000} seconds or {data['end'] / 60000:.3f} minutes
                            </p>
                        </div>
                        """
                        st.markdown(div_content, unsafe_allow_html=True)
                        st.write("##")
        else:
            display_no_category_banner("SPeaker_labels=>(no file)")


def text_summary(analysis_type, temp_file):
    if analysis_type == "Summarization":
        content = (
            "Here, you will find a concise summary that captures the most important points from your content."
            " The summary distills lengthy or complex information into a brief, easy-to-read format,"
            " allowing users to quickly grasp the essential details without reading through the entire content."
            " This feature is ideal for quick overviews and efficient content consumption.")
        analysis_type_header("Summary", "green", content)
        if temp_file:
            # with open(temp_file, "r", encoding="utf-8") as file2:
            #     summary = json.load(file2)
            summary = temp_file
            summary_data = summary["summary"]
            if not summary_data:
                display_no_category_banner("text_summary=>(no summary in file)")
            else:
                div_content = f"""
                              <div style="background-color:#e9ecef;overflow:auto; padding:15px; border-radius:10px;
                               margin-bottom:20px; font-family:'Arial', sans-serif;
                                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                  {summary_data}
                              </div>
                              """
                st.markdown(div_content, unsafe_allow_html=True)

        else:
            display_no_category_banner("Summarized text=>(no file)")


def call_functions(unfiltered_data):
    page_header()
    
    try:
        if unfiltered_data is not None:
            analysis = language_analysis_menu()
            sentiment_analysis(analysis, unfiltered_data)
            entity_detection(analysis, unfiltered_data)
            speaker_labels(analysis, unfiltered_data)
            content_safety(analysis, unfiltered_data)
            Topic_detection(analysis, unfiltered_data)
            text_summary(analysis, unfiltered_data)
            st.write("___")
            st.write("##")
            st.write("##")
            st.write("##")
        else:
            st.info("Transcribe a file to view its content analysis")
    except:
        return


if __name__ == "__main__":
    pass
    # call_functions()
