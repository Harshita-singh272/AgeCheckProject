import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

st.markdown("""
<style>
.panel {
    background-color: #fffbff;
    border: 1.5px solid #9a8c98;
    border-radius: 12px;
    padding: 20px;
    height: calc(100vh - 10rem);
    box-sizing: border-box;
}
            
[data-testid="stFileUploader"] {
    border: 2px dashed #b8c1d1;
    border-radius: 15px;
    padding-top: 15px !important;
    padding-left: 50px !important;
    padding-bottom: 18px;
    background-color: #F0F2F6;      
}
            
[data-testid="stRadio"] > div {
    border: 1px solid #d9dee8;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08),
    0 4px 12px rgba(0,0,0,0.04);
    padding: 10px;
    border-radius: 4px;
    background-color: white;
    min-width: 26vw !important;
}
            
[data-testid="stRadio"] label {
    border: 1px solid #d9dee8;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    width: 100%;
    display: flex;
    align-items: center;
    box-sizing: border-box;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08),
    0 4px 12px rgba(0,0,0,0.04);
}
            
[data-testid="stRadio"] label:has(input:checked) {
    border: 2px solid #4f8dfd;
    background: #f8fbff;
}
            
[data-testid="stRadio"] label:has(input:checked) p {
    font-weight: 700 !important;
    color: #1F4DFF !important;
}
            
[data-testid="stRadio"] label p {
    font-size: 15px;
    margin: 0;
}

[data-testid="stButton"]{
    # display: flex;
    # justify-content: center; 
    # width: 100%;
    font-weight: 700 !important; 
    width: fit-content !important;
    margin: 0 auto !important;      
    margin-bottom: 0 !important;   
}
[data-testid="stButton"] button {
    background: #1E4DFF !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(13, 91, 255, 0.25);
    border-radius: 8px;
    width: 320px !important;
}    
[data-testid="stButton"] button * {
    # font-weight: 700 !important;
    font-size: 15px !important;        
    color: white !important;
    font-family: "Nunito", sans-serif;
    font-weight: 500;
}        
.block-container {
    padding-top: 2rem;
    padding-left: .5rem;
    padding-right: .5rem;
}
            
h3{
    color: #003049 !important;
}
            
h1{
    color: white !important;
    background-color: #031d44;  
    font-size: 35px !important;  
    padding-left: 5px !important;
    padding-top: 10px !important;
    margin-bottom: 0.5rem !important; 
    line-height:1.2;    
} 
            
hr{
    margin-top: 0 !important;
    margin-bottom: 05.rem !important;
}

.upload-title {
    font-size: 20px;
    color: #003049 !important;
}

.threshold-title {
    font-size: 20px;
    color: #003049 !important;
} 

.privacy-box {
    margin-top: -10px !important;
    padding: 12px;
    border-radius: 8px;
    background-color: #f5f7fb;
    border: 1px solid #dbe3f0;
    font-size: 16px;
}         
</style>
""", unsafe_allow_html=True)
st.title("Age Check with Boolean Privacy Demo")
left , centre , right = st.columns([5,6,5])

with left:
    container = st.container(border=True)

    with container:
        st.subheader("⚙ Configuration")
        st.divider()
        st.markdown(
            '<div class="upload-title">1. Upload Image</div>',
            unsafe_allow_html=True
        )
        uploaded_file=st.file_uploader(
            "",
            type=["jpg" , "png" , "jpeg"],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.info("Upload area")
            st.image(uploaded_file)
       
        st.markdown(
            '<div class="threshold-title">2. Select Age Threshold</div>',
            unsafe_allow_html=True
        )
        threshold = st.radio(
            "Choose the minimum age that a user must meet to pass age verification.",
            ["18+ (Default)","21+","25+","60+"]
        )

        st.button("🛡️ VERIFY AGE" , use_container_width=True)
        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("""
            <div class="privacy-box">
                🛡️ <b>This system uses Boolean Privacy.</b>
                Exact age is never shown to normal users.
            </div>
        """, unsafe_allow_html=True)

with centre:
    container = st.container(border=True)
    with container:
        st.subheader("User Panel")

with right:
    st.markdown("""
    <style>
    
    </style>
    """ , unsafe_allow_html = True)
    st.subheader("Admin Access")        