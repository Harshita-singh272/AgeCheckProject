import streamlit as st
from PIL import Image
import requests

API_URL = "http://127.0.0.1:8000/check_age"

uploaded_file=('data/test_images/profile.png')
threshold= 18
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
    padding-top: 0rem !important;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-bottom: 0rem;
}
div[data-testid="stHeading"]{
    margin-top:0 !important;
    padding-top:0 !important;
}

div[data-testid="stHeading"] h1{
    margin:0 !important;
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
    margin-bottom: .7rem;
    padding: 12px;
    border-radius: 8px;
    background-color: #f5f7fb;
    border: 1px solid #dbe3f0;
    font-size: 18px;
}         

.about {
    font-size: 27px;
    color: #003049 !important;           
    font-weight: 500;
}
    
.about-data {
    font-size: 17px;
    color: #003049 !important;   
    margin-bottom: 1.5rem;      
    font-weight: 400;        
}
            
.left_description {
    font-size: 18px;
    margin-top: -6px;
    margin-bottom:10px;
    color: #343a40 !important;            
}
            
.caption {
    margin-top: -8px;
    color: #adb5bd;
    text-align: center;
    font-size: 15px;
}
            
.uploaded {
    font-weight: 600;   
    font-size: 19px;         
}

.decision-card{
    padding:20px;
    padding-top: 10px !important;
    border-radius:12px;
    text-align:left;
    min-height:90px;
    margin-bottom: .5rem;
}

.pass{
    border:2px solid #22C55E;
    background:#F0FDF4;
    padding-right:10px;
}

.inconclusive{
    border:2px solid #F59E0B;
    background:#FFFBEB;
}

.fail{
    border:2px solid #EF4444;
    background:#FEF2F2;
    padding-right:10px !important;
}

.icon{
    font-size:20px;
}

.title{
    font-size:20px;
    font-weight:500;
    margin-top:5px;
}

.desc{
    font-size:15px;
    margin-top:5px;
    color:#4B5563;
}
            /* ---------- RIGHT PANEL ---------- */

.admin-card{
    background:#ffffff;
    border:1px solid #d9dee8;
    border-radius:12px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 1px 3px rgba(0,0,0,.08);
}

.admin-title{
    font-size:18px;
    font-weight:700;
    color:#4F46E5;
    margin-bottom:10px;
}

.admin-subtitle{
    color:#4B5563;
    font-size:15px;
    margin-bottom:15px;
}

.locked-card{
    background:#FFF8F8;
    border:1px dashed #FCA5A5;
    border-radius:12px;
    padding:18px;
    margin-top:18px;
}

.locked-title{
    color:#7C2D12;
    font-size:18px;
    font-weight:700;
    margin-bottom:10px;
}

.lock-item{
    padding:7px 0;
    font-size:15px;
    color:#374151;
}

.lock-footer{
    margin-top:18px;
    padding:12px;
    border-radius:10px;
    background:#FEF2F2;
    border:1px solid #FECACA;
    text-align:center;
    color:#B91C1C;
    font-size:14px;
    font-weight:600;
}

.user-header{
    font-size:40px !important;
    font-weight:600;
    color:#023e8a;
    margin-right: -.6rem;
     
}   

.user-description{
    padding-top: 5rem !important; 
    font-size:25px !important;
    font-weight:600;
    color:#023e8a;    
    
}   
               
.configuration-header{
    color: #003049 !important;
    font-size: 40px !important;
    font-weight: 600;
}       
            
.divider-user hr{
    border: 2px soild #023e8a ;
    border-radius: 10px;
    height:.4rem !important;
    background: #023e8a ;  
    margin-top: 1rem;
    margin-bottom: .5rem;
}
            
.divider-config hr{
    border: 2px soild #003049 ;
    border-radius: 10px;
    height:.2rem !important;
    background: #003049 ;  
    margin-top: 1rem;
    margin-bottom: .5rem;        
}
            
</style>
""", unsafe_allow_html=True)
st.markdown("""
<h1 style="
background:#031D44;
color:white;
padding:18px 20px;
margin:0;
border-radius:0;
font-size:38px;
font-weight:700;">
🔔 Age Check with Boolean Privacy Demo
</h1>
""", unsafe_allow_html=True)
left , centre , right = st.columns([5,7,4])

with left:
    container = st.container(border=True)

    with container:
        st.markdown(
            '<div class="configuration-header">⚙ Configuration</div>'
        ,unsafe_allow_html=True)
        st.markdown(
            '<div class="left_description">[Configure age verification settings]</div>',unsafe_allow_html=True
        )
        st.markdown(
            '<div class="divider-config"><hr></div>'
        ,unsafe_allow_html=True)
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
            st.image(uploaded_file , width=90)
       
        st.markdown(
            '<div class="threshold-title">2. Select Age Threshold</div>',
            unsafe_allow_html=True
        )
        threshold = st.radio(
            "💡 Choose the minimum age that a user must meet to pass age verification.",
            [18,21,25,50,60]
        )

        verification = st.button("🛡️ VERIFY AGE" , use_container_width=True)
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

    container = st.container(border=True)

    with container:
        st.markdown(
            '<div class="about">📋 About this System</div>',
            unsafe_allow_html=True)
        
        st.divider()

        st.markdown(
            '<div class=about-data>This demo verifies whether a user is above a selected age threshold without revealing the exact age. It follows the principle of data minimization and privacy by design.</div>',
        unsafe_allow_html=True)

with centre:
    container = st.container(border=True)
    with container:
        st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:32px;color:#023e8a;">
                    🪪
                </span>
                <span style="font-size:40px;font-weight:700;color:#023e8a;white-space:nowrap;">
                    User Panel
                </span>
                <span style="font-size:20px;color:#023e8a;margin-top:12px;white-space:nowrap;">
                    (Normal View)
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
            '<div class="divider-user"><hr></div>'
        ,unsafe_allow_html=True)
        if verification == False:
            st.markdown(
            '<div class="uploaded">Uploaded Image</div>',
            unsafe_allow_html=True
            ) 
            col1, col2, col3 = st.columns([2,2, 2])

            with col2:
                container = st.container(border=True)

                with container:
                        st.image('data/test_images/profile.png' , width = 250)
                        st.markdown(
                            '<div class=caption>No Image Uploaded</div>',unsafe_allow_html=True
                        )            
            st.markdown(
            """<div class="uploaded">Verification Result</div>""",
            unsafe_allow_html=True
            )
            placeholder = st.container(border=True)

            with placeholder:

                left_icon, right_text = st.columns([1, 8])

                with left_icon:
                    st.markdown(
                        '<div style="color:#014f86;font-size:40px;text-align:center;margin-top: -.7rem;">ⓘ</div>',
                        unsafe_allow_html=True
                    )

                with right_text:
                    st.markdown(
                        """
                        <div style="color:#014f86; font-size:32px; font-weight:600; margin-bottom:0; margin-top: -0.5rem;">
                            Awaiting Verification
                        </div>
                        """,
                    unsafe_allow_html=True
                    )

                    st.markdown(
                         """
                        <div style="
                            color:#335c67; margin-bottom: .5rem;
                          ">
                        "Upload an image and click **VERIFY AGE** to see the result."
                        </div>
                        """,
                    unsafe_allow_html=True
                    )
            st.markdown(
            """<div class="uploaded">Confidence Level</div>""",
            unsafe_allow_html=True
            )
            # Top row
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown("""
                <div style="
                    font-size:40px;
                    font-weight:700;
                    color:#0f172a;
                ">
                    0%
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="
                    text-align:right;
                    margin-top:15px;
                    color:#64748b;
                    font-size:15px;
                ">
                    No data yet
                </div>
                """, unsafe_allow_html=True)

            # Progress Bar
            st.markdown("""
            <div style="
                width:100%;
                height:12px;
                background:#e5e7eb;
                border-radius:10px;
                margin-top:5px;
                margin-bottom:10px;
            "></div>
            """, unsafe_allow_html=True)

            # Scale
            scale1, scale2, scale3, scale4, scale5 = st.columns(5)

            with scale1:
                st.markdown("<div style='text-align:left;'>0%</div>", unsafe_allow_html=True)

            with scale2:
                st.markdown("<div style='text-align:center;'>25%</div>", unsafe_allow_html=True)

            with scale3:
                st.markdown("<div style='text-align:center;'>50%</div>", unsafe_allow_html=True)

            with scale4:
                st.markdown("<div style='text-align:center;'>75%</div>", unsafe_allow_html=True)

            with scale5:
                st.markdown("<div style='text-align:right;'>100%</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Legend
            legend1, legend2, legend3 = st.columns(3)

            with legend1:
                st.markdown(
                    "<div style='text-align:center;color:#475569;margin-bottom:8px'>🔴 0–59% &nbsp; Low</div>",
                    unsafe_allow_html=True
                )

            with legend2:
                st.markdown(
                    "<div style='text-align:center;color:#475569;'>🟡 60–79% &nbsp; Medium</div>",
                    unsafe_allow_html=True
                )

            with legend3:
                st.markdown(
                    "<div style='text-align:center;color:#475569;'>🟢 80–100% &nbsp; High</div>",
                    unsafe_allow_html=True
                )     
            st.info("ⓘ &nbsp; Only a boolean result is shown in this view to protect user privacy.")  
        else: 
            st.markdown(
            '<div class="uploaded">Uploaded Image</div>',
            unsafe_allow_html=True
            ) 
            col1, col2, col3 = st.columns([2,2, 2])
            with col2:
                container = st.container(border=True)
                with container:
                    st.image(uploaded_file , width=300)

            st.markdown(
            """<div class="uploaded">Verification Result</div>""",
            unsafe_allow_html=True
            )
            files = {
                "image": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }

            data = {
                "threshold": str(threshold)
            }

            response = requests.post(
                API_URL,
                files=files,
                data=data
            )
            result = response.json()

            if result["decision"]=="PASS":
                st.markdown(f"""
                    <div class="decision-card pass">
                        <div style="color:#16A34A;font-size:38px; font-weight:600;">✅  PASS</div>
                        <div style="font-size:20px; margin-bottom: .3rem; margin-left:2rem;margin-topm:.7rem;">
                            &nbsp;&nbsp;&nbsp;&nbsp; User is above Threshold ({threshold})+ <br>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            elif result["decision"]=="FAIL":
                st.markdown(f"""
                    <div class="decision-card fail">
                        <div style="color:#DC2626;font-size:38px; font-weight:600;">❌  FAIL</div>
                        <div style="font-size:20px; margin-bottom: .3rem; margin-left:2rem;margin-topm:.7rem;">
                            &nbsp;&nbsp;&nbsp;&nbsp; User is below Threshold ({threshold})+ <br>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)    
                                          
            else:
                st.markdown(f"""
                    <div class="decision-card inconclusive">
                        <div style="color:#F59E0B;font-size:38px; font-weight:600;">⚠️ INCONCLUSIVE</div>
                        <div style="font-size:20px; margin-bottom: .3rem; margin-left:2rem;margin-topm:.7rem;">
                            &nbsp;&nbsp;&nbsp;&nbsp; Prediction is close to threshold ({threshold})+ or confidence is low <br>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)    
            st.markdown(
            """<div class="uploaded">Confidence Level</div>""",
            unsafe_allow_html=True
            )    
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"""
                <div style="
                    font-size:40px;
                    font-weight:700;
                    color:#0f172a;
                ">
                    {result["confidence"]}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if 0 <= result["confidence"] <= 59:

                    st.markdown("""
                    <div style="
                        text-align:right;
                        margin-top:15px;
                        color:#64748b;
                        font-size:15px;
                    ">
                        Low Confidence
                    </div>
                    """, unsafe_allow_html=True)
                elif 60 <= result["confidence"] <= 79:
                    st.markdown("""
                    <div style="
                        text-align:right;
                        margin-top:15px;
                        color:#64748b;
                        font-size:15px;
                    ">
                        Medium Confidence
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="
                        text-align:right;
                        margin-top:15px;
                        color:#64748b;
                        font-size:15px;
                    ">
                        High Confidence
                    </div>
                    """, unsafe_allow_html=True)        
            confidence = float(result["confidence"])

            if confidence <= 59:
                bar_color = "#EF4444"    
            elif confidence <= 79:
                bar_color = "#EBD122" 
            else:
                bar_color = "#16A34A" 

            st.markdown(f"""
            <div style="
                width:100%;
                height:14px;
                background:#E5E7EB;
                border-radius:10px;
                overflow:hidden;
                margin-top:8px;
            ">
                <div style="
                    width:{confidence}%;
                    height:100%;
                    background:{bar_color};
                    border-radius:10px;
                    transition:width .5s ease;
                ">
                </div>
            </div>
            """, unsafe_allow_html=True)      

            scale1, scale2, scale3, scale4, scale5 = st.columns(5)
            with scale1:
                st.markdown("<div style='text-align:left;'>0%</div>", unsafe_allow_html=True)

            with scale2:
                st.markdown("<div style='text-align:center;'>25%</div>", unsafe_allow_html=True)

            with scale3:
                st.markdown("<div style='text-align:center;'>50%</div>", unsafe_allow_html=True)

            with scale4:
                st.markdown("<div style='text-align:center;'>75%</div>", unsafe_allow_html=True)

            with scale5:
                st.markdown("<div style='text-align:right;'>100%</div>", unsafe_allow_html=True)

            legend1, legend2, legend3 = st.columns(3)

            with legend1:
                st.markdown(
                    "<div style='text-align:center;color:#475569;margin-bottom:1rem; margin-top:.5rem;'>🔴 0–59% &nbsp; Low</div>",
                    unsafe_allow_html=True
                )

            with legend2:
                st.markdown(
                    "<div style='text-align:center;color:#475569;margin-bottom:1rem; margin-top:.5rem;'>🟡 60–79% &nbsp; Medium</div>",
                    unsafe_allow_html=True
                )

            with legend3:
                st.markdown(
                    "<div style='text-align:center;color:#475569;margin-bottom:1rem; margin-top:.5rem;'>🟢 80–100% &nbsp; High</div>",
                    unsafe_allow_html=True
                )     
            st.info("ⓘ &nbsp; Only a boolean result is shown in this view to protect user privacy.")     

    Decision = st.container(border=  True)

    with Decision:
        st.markdown(
        '<div class="about">Decision Type</div>',
        unsafe_allow_html=True)
        st.divider()
        col1 , col2 ,col3 = st.columns([1,1.7,1])

        with col1:
            st.markdown("""
            <div class="decision-card pass">
                <div class="title" style="color:#16A34A;">✅  PASS</div>
                <div class="desc">
                    Age is above<br>
                    threshold
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="decision-card inconclusive">
                <div class="title" style="color:#F59E0B;">⚠️ INCONCLUSIVE</div>
                <div class="desc">
                    Prediction is close to threshold
                    or confidence is low
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="decision-card fail">
                <div class="title" style="color:#DC2626;">❌  FAIL</div>
                <div class="desc">
                    Age is below<br>
                    threshold
                </div>
            </div>
            """, unsafe_allow_html=True)
with right:

    # ---------------- Admin Access ---------------- #

    admin_card = st.container(border=True)

    with admin_card:

        st.markdown(
            '<div class="admin-title">🔒 Admin Access</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="admin-subtitle">Enter passkey to unlock admin diagnostics.</div>',
            unsafe_allow_html=True
        )

        passkey = st.text_input(
            "Admin Passkey",
            type="password",
            placeholder="Enter passkey",
            label_visibility="collapsed"
        )

        unlock = st.button(
            "🔓 Unlock Admin",
            use_container_width=True
        )

        st.caption("🔒 Admin access is for demo and learning purposes only.")

    # ---------------- Locked Panel ---------------- #

    locked = st.container(border=True)

    with locked:

        st.markdown(
            """
            <div class="locked-title">
            🔒 Admin Panel (Locked)
            </div>

            <div class="lock-item">📊 Estimated Age (Raw Prediction)</div>

            <div class="lock-item">📈 Confidence Calculation</div>

            <div class="lock-item">🖥️ Model Diagnostics</div>

            <div class="lock-item">📜 Activity Logs</div>

            <div class="lock-item">⚙️ API & Model Information</div>

            <div class="lock-footer">
                Unlock to access sensitive administrator information
            </div>
            """,
            unsafe_allow_html=True
        )


