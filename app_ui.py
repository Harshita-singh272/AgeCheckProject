import streamlit as st
from PIL import Image
import requests
import json
import plotly.express as px
from datetime import datetime
from app.storage import get_bargraph_dataframe , get_statistics,load_verification_logs

API_URL_USER = "http://127.0.0.1:8000/check_age"
API_URL_ADMIN = "http://127.0.0.1:8000/admin/check_age"

st.set_page_config(layout="wide")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "admin_result" not in st.session_state:
    st.session_state.admin_result = None

if "admin_message" not in st.session_state:
    st.session_state.admin_message = ""

if "admin_passkey" not in st.session_state:
    st.session_state.admin_passkey = ""

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "threshold" not in st.session_state:
    st.session_state.threshold = 18

if "verification" not in st.session_state:
    st.session_state.verification = False

if "verification_result" not in st.session_state:
    st.session_state.verification_result = None


def verify_admin():
    files = {
        "image": (
            st.session_state.uploaded_file.name,
            st.session_state.uploaded_file,
            st.session_state.uploaded_file.type
        )
    }

    data = {
        "passkey": st.session_state.admin_passkey,
        "threshold": str(st.session_state.threshold)
    }

    try:
        response = requests.post(API_URL_ADMIN, files=files, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend: {e}")
        return
    except ValueError:
        st.error("Backend returned an invalid JSON response.")
        return

    st.session_state.admin_result = result

def verify_user():
    files = {
        "image": (
            st.session_state.uploaded_file.name,
            st.session_state.uploaded_file,
            st.session_state.uploaded_file.type
        )
    }

    data = {
        "threshold": str(st.session_state.threshold)
    }

    try:
        response = requests.post(API_URL_USER, files=files, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend: {e}")
        return
    except ValueError:
        st.error("Backend returned an invalid JSON response.")
        return

    st.session_state.verification_result = result

def show_left_panel():
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
        st.session_state.uploaded_file = st.file_uploader(
            "",
            type=["jpg","png","jpeg"],
            label_visibility="collapsed"
        )   
        
        if st.session_state.uploaded_file is not None:
            st.info("Upload area")
            st.image(st.session_state.uploaded_file , width=90)
       
        st.markdown(
            '<div class="threshold-title">2. Select Age Threshold</div>',
            unsafe_allow_html=True
        )
        st.session_state.threshold = st.radio(
            "💡 Choose the minimum age that a user must meet to pass age verification.",
            [18,21,25,50,60],
            index=[18,21,25,50,60].index(st.session_state.threshold)
        )

        if st.button("🛡️ VERIFY AGE" , use_container_width=True):

            if st.session_state.uploaded_file is None:
                st.warning("Please upload an image first.")

            else:

                if st.session_state.admin_logged_in:
                    verify_admin()

                else:
                    verify_user()
                    
                st.session_state.verification = True

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

def show_admin_panel():
    if st.session_state.admin_result is None:

        age = "--"
        threshold = "--"
        decision = "--"
        difference = "--"
        confidence = 0
        latency = "--"
        model = "--"
        image_name = "--"
        status = "Waiting..."

    else:

        result = st.session_state.admin_result

        age = result["estimated_age"]
        threshold = result["threshold"]
        decision = result["decision"]
        difference = result["difference"]
        confidence = result["confidence"]
        latency = result["latency_ms"]
        model = result["model_name"]
        image_name = st.session_state.uploaded_file.name
        status = "Completed"

    container = st.container(border=True)

    with container:

        st.markdown(
        """
            <div style="
                display:flex;
                align-items:center;
                gap:14px;
                margin-bottom:6px;
            ">
                <span style="font-size:34px;">
                    🔓
                </span>
                <span style="
                    font-size:42px;
                    font-weight:700;
                    color:#15803D;
                    line-height:1;
                ">
                    ADMIN PANEL
                </span>
                <span style="
                    font-size:22px;
                    color:#15803D;
                    font-weight:500;
                    margin-top:8px;
                ">
                    (UNLOCKED)
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                color:#64748B;
                font-size:15px;
                margin-left:2px;
                margin-bottom:18px;
            ">
                Diagnostics & Internal View (For learning purposes only)
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        with col1:

            st.markdown(f"""
                <div style="
                    background:white;
                    border:1px solid #E5E7EB;
                    border-radius:12px;
                    padding-top:16px;
                    padding-right:16px;
                    padding-left:16px;
                    padding-bottom:14px;
                    margin-bottom:1rem;
                    height:170px;">
                    <div style="
                        color:#343a40;
                        font-size:15px;
                        font-weight:500;
                    ">
                        Estimated Age (Raw Model Output)
                    </div>
                    <div style="
                        color:#264653;
                        font-size:38px;
                        font-weight:700;
                        margin-top:5px;
                    ">
                        {age}
                    </div>
                    <div style="color:#64748B;font-size:14px;">
                        Years
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:

            st.markdown(f"""
            <div style="
                background:white;
                border:1px solid #E5E7EB;
                border-radius:12px;
                padding-top:16px;
                padding-right:16px;
                padding-left:16px;
                padding-bottom:16px;
                height:170px;
            ">
                <div style="
                    color:#343a40;
                    font-size:15px;
                    font-weight:500;
                ">
                    Threshold
                </div>
                <div style="
                    color:#111827;
                    font-size:38px;
                    font-weight:700;
                    margin-top:24px;
                ">
                    {threshold}
                </div>
                <div style="color:#64748B;font-size:14px;">
                    Years
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if decision == "PASS":
            decision_color = "#15803D"

        elif decision == "FAIL":
            decision_color = "#DC2626"

        elif decision == "INCONCLUSIVE":
            decision_color = "#F59E0B"

        else:
            decision_color = "#9CA3AF"

        with col3:

            st.markdown(f"""
            <div style="
                background:white;
                border:1px solid #E5E7EB;
                border-radius:12px;
                padding-top:16px;
                padding-right:16px;
                padding-left:16px;
                padding-bottom:20px;
                height:170px;
            ">
                <div style="
                    color:#343a40;
                    font-size:15px;
                    font-weight:500;
                ">
                    Decision (Boolean)
                </div>
                <div style="
                    color:{decision_color};
                    font-size:34px;
                    font-weight:700;
                    margin-top:26px;
                ">
                    {decision}
                </div>
                <div style="
                    color:#64748B;
                    font-size:14px;
                    padding-top:5px;
                ">
                    {status}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col4:

            st.markdown(f"""
            <div style="
                background:white;
                border:1px solid #E5E7EB;
                border-radius:12px;
                padding-top:16px;
                padding-right:16px;
                padding-left:16px;
                padding-bottom:12px;
                height:170px;
            ">
                <div style="
                    color:#343a40;
                    font-size:15px;
                    font-weight:500;
                ">
                    Difference From Threshold
                </div>
                <div style="
                    color:#00296b;
                    font-size:38px;
                    font-weight:700;
                    margin-top:7px;
                ">
                    {difference}
                </div>
                <div style="
                        color:#64748B;
                        font-size:14px;
                    ">
                        Years
                </div>
            </div>
            """, unsafe_allow_html=True)

        confidence_container = st.container(border=True)

        with confidence_container:
            if not st.session_state.verification:
                st.markdown(
                """<div class="uploaded">Confidence Level</div>""",
                unsafe_allow_html=True
                )
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
            else: 
                st.markdown(
                """<div class="uploaded">Verification Result</div>""",
                unsafe_allow_html=True
                )


                if decision=="PASS":
                    st.markdown(f"""
                        <div class="decision-card pass">
                            <div style="color:#16A34A;font-size:38px; font-weight:600;">✅  PASS</div>
                            <div style="font-size:20px; margin-left:2rem;margin-top:.5rem;">
                                &nbsp;&nbsp;&nbsp;&nbsp; User is above Threshold ({st.session_state.threshold})+ <br>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                elif decision=="FAIL":
                    st.markdown(f"""
                        <div class="decision-card fail">
                            <div style="color:#DC2626;font-size:38px; font-weight:600;">❌  FAIL</div>
                            <div style="font-size:20px; margin-left:2rem;margin-top:.5rem;">
                                &nbsp;&nbsp;&nbsp;&nbsp; User is below Threshold ({st.session_state.threshold})+ <br>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)    
                                            
                elif decision == "INCONCLUSIVE":
                    st.markdown(f"""
                        <div class="decision-card inconclusive">
                            <div style="color:#F59E0B;font-size:38px; font-weight:600;">⚠️ INCONCLUSIVE</div>
                            <div style="font-size:20px; margin-left:2rem;margin-top:.5rem;">
                                &nbsp;&nbsp;&nbsp;&nbsp; Prediction is close to threshold ({st.session_state.threshold})+ or confidence is low <br>
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
                        {confidence}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    if 0 <= confidence <= 59:

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
                    elif 60 <=confidence <= 79:
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
                confidence = float(confidence)

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
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1.5,2])     
    with col1:

        card = st.container(border=True)

        with card:
            st.markdown(
                """
            <div style= 'font-size:25px;font-weight:600;'>Confidence Calculation</div>
            """,unsafe_allow_html=True)
           

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns([1,0.2,1])

            with c1:
                st.markdown(
                        f"""<div style='text-align:center;color:#475569;border: 1px solid #E5E7EB;border-radius: 12px;box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);height:120px;padding: 10px'>
                        <div style='font-size:18px;font-weight:600;'>Predicted Age</div>
                        <div style= "font-size:17px;margin:.5rem"> {age}
                        </div>
                        </div>""",
                        unsafe_allow_html=True
                    )

            with c2:
                st.markdown(
                    "<h2 style='text-align:center;margin-top:15px;'>−</h2>",
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                        f"""<div style='text-align:center;color:#475569;;border: 1px solid #E5E7EB;border-radius: 12px;box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);height:120px;padding:10px '>
                        <div style='font-size:18px;font-weight:600;'>Threshold</div>
                        <div style= "font-size:17px;margin:2rem"> {threshold}
                        </div>
                        </div>""",
                        unsafe_allow_html=True
                    )  

            difference_display = "--"

            if difference != "--":
                difference_display = difference
            
            st.markdown(
                        f"""<div style='text-align:center;color:#475569;border-radius: 12px;box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);height:90px;padding: 10px;margin-right:3rem;margin-left:3rem;margin-bottom:1rem;margin-top:.5rem;'>
                        <div style='font-size:18px;font-weight:600;'>Difference</div>
                        <div style= "font-size:17px;margin:.5rem"> {difference_display}
                        </div>
                        </div>""",
                        unsafe_allow_html=True
                    ) 
            
        with col2:

            card = st.container(border=True)

            with card:

                st.markdown("#### Model & Inference Info")      
                info = {
                    "Model": model,
                    "Latency": f"{latency} ms",
                    "Output": decision,
                    "Threshold": threshold,
                    "Privacy": "Boolean",
                }
                for key, value in info.items():

                    c1, c2 = st.columns([1.2,1])

                    c1.write(key)

                    c2.write(value)
        with col3:

            card = st.container(border=True)

            with card:

                st.markdown("#### Request Information")
                request = {

                    "Endpoint": "/admin/check_age",

                    "Method": "POST",

                    "Threshold": threshold,

                    "Timestamp": datetime.now().strftime("%d %b %Y %I:%M %p")
                }
                for key, value in request.items():

                    c1, c2 = st.columns([.8,1])

                    c1.write(key)

                    c2.write(value)
    st.info("ⓘ &nbsp;Confidence is based on how far the predicted age is from the selected threshold.")
    st.markdown(
                """
            <div style= 'font-size:20px;font-weight:400;'>Formula Used</div>
            """,unsafe_allow_html=True)
    st.code(
        "confidence = min(50 + difference × 5 , 100)",
        language="text"
    )         
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.admin_result is None:
        st.markdown( """
        <div style = 'max-width: 100;height:300px;border: 1px solid #E5E7EB;border-radius: 12px;box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);'>
        <div style= 'font-size: 30px;'>
        📄 Full JSON Payload
        </div>
            <div style= 'padding:20px; font-size: 20px'>
                "The JSON response will appear after the first successful verification."
            </div>        
         </div>"""
        ,unsafe_allow_html=True
                )             
    else:
        payload = json.dumps(
            st.session_state.admin_result,
            indent=4
        )
        st.markdown(
            f"""
            <div style="
                background:#111827;
                border:1px solid #1F2937;
                border-radius:12px;
                padding:22px;
                margin-top:12px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);
            ">
            <div style="
                color:white;
                font-size:24px;
                font-weight:700;
                margin-bottom:16px;
            ">
            📄 Full JSON Payload
            </div>
            <p style="
                color:#E5E7EB;
                font-size:18px;
                font-family:Consolas,'Courier New',monospace;
                line-height:1.6;
                margin:0;
                white-space:pre-wrap;
                overflow-x:auto;
            ">{payload}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
            

def show_user_panel():
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
        if not st.session_state.verification:
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
                    if st.session_state.uploaded_file is None:
                        st.image("data/test_images/profile.png", width=250)
                        st.caption("No Image Uploaded")

                    else:
                        st.image(st.session_state.uploaded_file, width=300)

            st.markdown(
            """<div class="uploaded">Verification Result</div>""",
            unsafe_allow_html=True
            )

            result = st.session_state.verification_result

            if result["decision"]=="PASS":
                st.markdown(f"""
                    <div class="decision-card pass">
                        <div style="color:#16A34A;font-size:38px; font-weight:600;">✅  PASS</div>
                        <div style="font-size:20px; margin-bottom: .3rem; margin-left:2rem;margin-topm:.7rem;">
                            &nbsp;&nbsp;&nbsp;&nbsp; User is above Threshold ({st.session_state.threshold})+ <br>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            elif result["decision"]=="FAIL":
                st.markdown(f"""
                    <div class="decision-card fail">
                        <div style="color:#DC2626;font-size:38px; font-weight:600;">❌  FAIL</div>
                        <div style="font-size:20px; margin-bottom: .3rem; margin-left:2rem;margin-topm:.7rem;">
                            &nbsp;&nbsp;&nbsp;&nbsp; User is below Threshold ({st.session_state.threshold})+ <br>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)    
                                          
            else:
                st.markdown(f"""
                    <div class="decision-card inconclusive">
                        <div style="color:#F59E0B;font-size:38px; font-weight:600;">⚠️ INCONCLUSIVE</div>
                        <div style="font-size:20px; margin-bottom: .3rem; margin-left:2rem;margin-topm:.7rem;">
                            &nbsp;&nbsp;&nbsp;&nbsp; Prediction is close to threshold ({st.session_state.threshold})+ or confidence is low <br>
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

def  show_admin_dashboard():
    admin_card = st.container(border=True)

    with admin_card:

        bar_df = get_bargraph_dataframe()
        if not bar_df.empty:

            fig = px.bar(
                bar_df,
                x="Threshold",
                y="Count",
                text="Count",
                color="Threshold",
                color_discrete_sequence = [
                    "#FABC3C",
                    "#FFB238",
                    "#F19143",
                    "#FF773D",
                    "#F55536"
                ]
            )

            fig.update_traces(
                textposition = "outside",
                marker_line_width = 0,
                hovertemplate = 
                "<b>%{x}+</b><br>" +
                "Verifications: %{y}<extra></extra>"
            )

            fig.update_layout(

                title = { 
                "text":"Verification Count by Threshold",
                "x":0.02,
                "font":dict(size=34)
                },

                plot_bgcolor = "white",
                paper_bgcolor = "white",

                showlegend= False,
                height=380,
                bargap = 0.25,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                ),
                
                xaxis=dict(
                title=dict(
                    text="Threshold Used",
                    font=dict(
                            size=20,
                            color="#812020"
                            ),
                    ),
                    showline=False,
                    type="category"
                ),

                yaxis=dict(
                    title=dict(
                        text="Number of Verifications",
                        font=dict(
                            size=20,
                            color="#812020"
                            ),
                        
                    ),
                    showgrid=True,
                    gridcolor="#a9a9a9",
                    zeroline=False
                )
            )
            
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar":False}
            )

        else:
            st.info("No verification data available.")

        st.markdown("---")

        st.markdown("### 📊 Activity Overview")

        stats = get_statistics()

        total = stats["total_verifications"]
        passed = stats["pass_count"]
        failed = stats["fail_count"]
        inconclusive = stats["inconclusive_count"]

        col1, col2, col3, col4 = st.columns(4, gap="small")

        cards = [
            ("Total", total, "#F8FAFC", "#334155", "#CBD5E1"),
            ( "Pass", passed, "#F0FDF4", "#15803D", "#BBF7D0"),
            ( "Fail", failed, "#FEF2F2", "#DC2626", "#FECACA"),
            ( "Inconclusive", inconclusive, "#FFFBEB", "#B45309", "#FDE68A"),
        ]

        for col, ( title, value, bg, text, border) in zip(
            [col1, col2, col3, col4], cards
        ):

            with col:

                st.markdown(f"""
                <div style="
                    background:{bg};
                    border:1px solid {border};
                    border-radius:12px;
                    padding:14px 10px;
                    text-align:center;
                    min-height:120px;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    box-shadow:0 2px 6px rgba(0,0,0,0.08);
                ">
                    <div style="
                        font-size:20px;
                        font-weight:600;
                        color:{text};
                        white-space:nowrap;">
                        {title}
                    </div>
                    <div style="
                        font-size:32px;
                        font-weight:700;
                        color:{text};
                        margin-top:8px;">
                        {value}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("---")
        logs = load_verification_logs()

        st.markdown("### 📝 Recent Activity")
        with st.container(border=True):

            h1, h2, h3, h4, h5 = st.columns([2.2, 1.5, 1.4, 1.2, 1.2])

            with h1:
                st.markdown(
                    "<div style='font-weight:700;color:#475569;padding-bottom:10px;font-size:17px;'>Timestamp</div>",
                    unsafe_allow_html=True
                )

            with h2:
                st.markdown(
                    "<div style='font-weight:700;text-align:center;color:#432818;padding-bottom:10px;font-size:17px;'>Threshold</div>",
                    unsafe_allow_html=True
                )

            with h3:
                st.markdown(
                    "<div style='font-weight:700;text-align:center;color:#475569;padding-bottom:10px;font-size:17px;'>Decision</div>",
                    unsafe_allow_html=True
                )

            with h4:
                st.markdown(
                    "<div style='font-weight:700;text-align:center;color:#432818;padding-bottom:10px;font-size:17px;'>Age</div>",
                    unsafe_allow_html=True
                )

            with h5:
                st.markdown(
                    "<div style='font-weight:700;text-align:center;color:#475569;padding-bottom:10px;font-size:17px;'>Latency</div>",
                    unsafe_allow_html=True
                )
        if not logs:
            st.info("No activity recorded yet.")

        else:

            for log in reversed(logs[-5:]):

                with st.container(border=True):

                    st.write("")

                    col1, col2, col3, col4, col5 = st.columns([2.8, 1, 1.4, 1.2, 1])

                    with col1:
                        st.write(log["timestamp"][:19])

                    with col2:
                        st.markdown(
                            f"<div style='font-weight:700;text-align:center;'>{log['threshold']}+</div>",
                            unsafe_allow_html=True
                        )

                    with col3:

                        decision = log["decision"]

                        if decision == "PASS":
                            st.markdown("""
                            <div style="
                                background:#DCFCE7;
                                color:#15803D;
                                padding:10px 16px;
                                border-radius:10px;
                                text-align:center;
                                font-weight:700;">
                                PASS
                            </div>
                            """, unsafe_allow_html=True)

                        elif decision == "FAIL":
                            st.markdown("""
                            <div style="
                                background:#FEE2E2;
                                color:#DC2626;
                                padding:10px 16px;
                                border-radius:10px;
                                text-align:center;
                                font-weight:700;">
                                FAIL
                            </div>
                            """, unsafe_allow_html=True)

                        elif decision == "INCONCLUSIVE":
                            st.markdown("""
                            <div style="
                                background:#FEF3C7;
                                color:#B45309;
                                padding:10px 16px;
                                border-radius:10px;
                                text-align:center;
                                font-weight:700;">
                                INCONCLUSIVE
                            </div>
                            """, unsafe_allow_html=True)

                    with col4:
                        st.markdown(
                            f"<div style='text-align:center;font-weight:600;'>{round(log['predicted_age'])} yrs</div>",
                            unsafe_allow_html=True
                        )

                    with col5:
                        st.markdown(
                            f"<div style='text-align:center;color:#6B7280;'>{round(log['latency_ms'])} ms</div>",
                            unsafe_allow_html=True
                        )

                    
def show_admin_login():

    admin_card = st.container(border=True)

    with admin_card:    

        st.markdown(
            '<div class="admin-title">🔒 Admin Access</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="divider-access"><hr></div>'
        ,unsafe_allow_html=True)
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

        if unlock:

            response = requests.post(
                "http://127.0.0.1:8000/admin/login",
                json={
                    "passkey": passkey
                }
            )

            result = response.json()

            if result["authenticated"]:

                st.session_state.admin_logged_in = True
                st.session_state.admin_passkey = passkey
                st.success("Admin Login Successful")

                st.rerun()

            else:

                st.error("Invalid Passkey")

        st.markdown("""
            <div class="custom-caption">
            🔒 Admin access is for demo and learning purposes only.
            </div>
            """, unsafe_allow_html=True)

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
            
h1{
    color: white !important;
    background-color: #031d44;  
    font-size: 35px !important;  
    padding-left: 5px !important;
    padding-top: 20px !important;
    margin-bottom: 0.2rem !important; 
    line-height:1.2;    
} 
            
hr{
    margin-top: 0 !important;
    margin-bottom: 05.rem !important;
}

.upload-title {
    font-size: 25px;
    color: #003049 !important;
}

.threshold-title {
    font-size: 25px;
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
    font-size: 27px;         
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

.admin-card{
    background:#ffffff;
    border:1px solid #d9dee8;
    border-radius:12px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 1px 3px rgba(0,0,0,.08);
}

.admin-title{
    font-weight:700;
    color:#4F46E5;
    margin-bottom:10px;
    font-size:38px;
}

.admin-subtitle{
    color:#4B5563;
    font-size:22px;
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
    font-size:30px;
    font-weight:700;
    margin-bottom:10px;
}

.lock-item{
    padding:7px 0;
    font-size:23px;
    color:#374151;
    font-style:italic;
}

.lock-footer{
    margin-top:18px;
    margin-bottom:18px;
    padding:12px;
    border-radius:10px;
    background:#FEF2F2;
    border:1px solid #FECACA;
    text-align:center;
    color:#B91C1C;
    font-size:20px;
    font-weight:600;
}
            
[data-testid = "stTextInput"] input {
    letter-spacing:2px;
    font-size: 20px !important;
}
    
[data-testid = "stTextInput"]{ 
    border: 2px solid #D6DCE8 !important;
    border-radius: 10px !important;
    background-color: #F8FAFC !important;
    padding: 10px 13px !important;
    margin-bottom: .9rem;
    color: #003049 !important;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
            
[data-testid="stTextInput"] input::placeholder{
    color:#003049 !important;
    opacity:1 !important;
}
 
.divider-access hr {
    border: .5px soild #4F46E5 ;
    border-radius: 5px;
    height:.2rem !important;
    background: #4F46E5 ;  
    margin-top: 1rem;
    margin-bottom: 1rem; 
}
            
.custom-caption {
    color:#64748B;
    font-size:20px;
    font-style:italic;
    margin-bottom: .8rem;    
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
st.title("🔔 Age Check with Boolean Privacy Demo")

if st.session_state.admin_logged_in:
    left , centre , right = st.columns([5,7,5])

else:
    left , centre , right = st.columns([5,7,4])    

with left:
    show_left_panel()

with centre:
    
    if st.session_state.admin_logged_in:
        show_admin_panel()

    else:
        show_user_panel()
with right:

    if st.session_state.admin_logged_in:
        show_admin_dashboard()

    else:
        show_admin_login()
