import streamlit as st
import pandas as pd

st.set_page_config(page_title="list", layout="wide")

# Top marquee background style aur Container ki border green karne ka CSS
st.markdown("""
<style>
    .block-container {padding-top: 1.9rem !important;}
    .stAppDeployButton {display: none !important;}
    
    /* Container ki line ko green karne ke liye CSS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid green !important;
        border-radius: 8px;
    }
</style>
<div style="position:fixed; top:0; left:0; width:100%; background:green; color:white; font-size:18px; font-weight:bold; z-index:999999;">
    <marquee behavior="scroll" direction="left" scrollamount="3">khandelwal software Aapaka Hardik Swagat Karta h</marquee>
</div>
<br>
""", unsafe_allow_html=True)

st.markdown("Khandelwal APP")

# === SESSION STATE SETUP ===
# Yahan hum record rakh rahe hain ki user ne koi choice ki hai ya nahi
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None

# Jab tak user choice (Agree/Disagree) nahi karta, tab tak ye dono container dikhenge
if st.session_state.user_choice is None:
    
    # 1. MAIN CONTAINER
    with st.container(border=True):
        col1, col2 = st.columns(2)
        agree = col1.checkbox("I Am Agree")
        not_agree = col2.checkbox("I Am Not agree")
        
        # Jese hi 'Agree' par click hoga, status save hoga aur page turant refresh hoga
        if agree:
            st.session_state.user_choice = 'agree'
            st.rerun()
            
        # Jese hi 'Not Agree' par click hoga, status save hoga aur page turant refresh hoga
        if not_agree:
            st.session_state.user_choice = 'not_agree'
            st.rerun()
            
        st.divider()
        
        # 2. NESTED CONTAINER (Terms and Conditions)
        with st.container(height=300):
            st.markdown("**Terms & Conditions**")
            st.markdown("""
            1. This app has been developed solely for the convenience of members and to facilitate information sharing.
            2. The app owner (developer) shall not be responsible or liable for any content or data displayed on this app.
            3. The concerned organization or the member submitting the information is solely responsible for any incorrect or misleading details.
            4. Data in the app may contain errors due to technical glitches or human oversight; please verify independently before making any decisions.
            5. Members are entirely responsible for checking and confirming the authenticity and accuracy of the details provided in the app.
            6. This app is currently provided completely free of charge to all members.
            7. The organization and app management reserve the right to alter or modify app rules, features, or services at any time.
            8. All users using the app must strictly follow the guidelines of the organization.
            9. If any member or organization worker spreads incorrect information or rumors, the app owner reserves the right to completely shut down the app.
            10. If members experience any inconvenience while using the app, the app owner may terminate/shut down the app service.
            11. No legal action can be initiated against the app owner (developer) in case of any error, incorrect data, or dispute arising from the app.
            12. Using this app implies that you fully understand and agree to all the terms and conditions listed above.
            """)

# =========================================================================
# Yahan se aage ka code tabhi chalega jab check box par click ho chuka hoga
# =========================================================================

# Agar user ne 'Agree' click kiya hai:
if st.session_state.user_choice == 'agree':
    st.markdown("Balai Svyam Seva Sasthan Surpura")
    try:
        raw_df = pd.read_csv(r"e:\python\LTM.csv", header=None, nrows=2, encoding='latin-1')
        file_date = raw_df.iloc[1, 0] if len(raw_df) > 1 else ""
        df = pd.read_csv(r"e:\python\LTM.csv", header=2, encoding='latin-1').dropna(how='all')
        df.columns = df.columns.str.strip()
        
        if 'phone' in df.columns:
            df['phone'] = df['phone'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        st.markdown(f"<div style='display:flex; justify-content:space-between;'><b>Mobile Number Enter Karein:</b><b style='color:#1f77b4;'>List Date: {file_date}</b></div>", unsafe_allow_html=True)
        
        val = st.text_input("Mobile Number Enter Karein", label_visibility="collapsed")
        
        if val:
            res = df[df['phone'].astype(str).str.contains(str(val), na=False, regex=False)].copy()
            if not res.empty:
                num_cols = [c for c in ['Nest Lo.', 'Discount', 'Kist', 'K.P.', 'Loan', 'L.P.', 'Inter', 'Other', 'Total', 'L.Balance'] if c in res.columns]
                for c in num_cols:
                    res[c] = pd.to_numeric(res[c].astype(str).str.replace(',', '').str.strip(), errors='coerce')
                
                sums = {c: res[c].sum() if c in num_cols else "" for c in res.columns}
                sums['Name'] = "TOTAL"
                total_amount = sums.get('Total', 0)
                
                final = pd.concat([res, pd.DataFrame([sums])], ignore_index=True).fillna('')
                for col in final.columns:
                    final[col] = final[col].astype(str).str.replace(r'\.0$', '', regex=True)
                
                st.success(f"✅ {len(res)} records mile | 💰 Total Amount: ₹{int(total_amount):,d}")
                
                if 'phone' in final.columns: 
                    final = final.drop(columns=['phone'])
                
                st.dataframe(
                    final.style.apply(lambda r: ['background-color: #ffcccc; color: #cc0000; font-weight: bold']*len(r) if r.get('Name') == 'TOTAL' else ['']*len(r), axis=1),
                    width="stretch", 
                    hide_index=True
                )
            else:
                st.warning(f"❌ Number '{val}' nahi mila!")

        st.divider()

        st.info("**संस्था का मुख्य उद्देश्य:** समाज के हर परिवार को आर्थिक रूप से आज़ाद करना और ब्याज-खोरों के जाल से बचाना है।")

        st.divider()

        st.markdown("खंडेलवाल ऐप समाज के लिए पूरी तरह से निःशुल्क (फ्री) है।")
        st.markdown("""
        * यह संस्था आपकी अपनी है।
        * हम सबको मिलकर इसका सहयोग करना चाहिए।
        * यह हमारी और आपके परिवार की जरूरतों को पूरा करती है।
        * यह हमारी और आपके परिवार की जरूरतों को पूरा करती है।
        * हमारे समाज में बहुत से लोग भारी ब्याज (Interest) चुकाते-चुकाते कभी कर्ज़ के जाल से बाहर नहीं आ पाते।
        * अगर हम सब एक-दूसरे का साथ देंगे, तो कोई भी भाई कभी आर्थिक मजबूरी में नहीं फँसेगा।
        * कर्ज़ मुक्त जीवन ही हमारे बच्चों को एक बेहतर कल दे सकता है।
        * छोटी बचत, बड़ा सहारा समय पर अपनी किस्त और सहयोग राशि जमा करके आप किसी जरूरतमंद भाई की बड़ी मदद कर रहे हैं।
        * आपका विश्वास और ईमानदारी ही इस संस्था की सबसे बड़ी पूँजी (Capital) है।
        * **याद रखें:** यह संस्था किसी एक की नहीं, बल्कि हम सबकी अपनी है।
        * जब हम सब मिलकर नियमों का पालन करते हैं, तभी हमारा समाज और परिवार कर्ज के जाल से बाहर निकलकर मजबूत बनता है।
        *आइए, एक बार फिर सोचें और मिलकर समाज को आगे बढ़ाएं!*
        """)
        st.success(" आइए, हम सब मिलकर इस संस्था को मजबूत बनाएं और अपने समाज को आगे बढ़ाएं!")
    except Exception as e:
        st.error(f"Error: {e}")

# Agar user ne 'Not Agree' click kiya hai:
elif st.session_state.user_choice == 'not_agree':
    st.markdown("""खंडेलवाल ऐप में आने पर आपका हार्दिक स्वागत है!
    * **ऐप की भूमिका:** **खंडेलवाल सॉफ्टवेयर** द्वारा यह ऐप केवल सदस्यों को आसानी से जानकारी (जैसे लिस्ट और हिसाब) उपलब्ध कराने के लिए तैयार किया गया है। 
    * ऐप का उद्देश्य केवल डिजिटल सुविधा देना है। यदि आप नियमों से असहमत हैं, तो सुरक्षा कारणों से डेटा प्रदर्शित नहीं किया जाएगा। 
    
    *जब भी आप चाहें, पेज को रीफ्रेश करके शर्तें स्वीकार कर सकते हैं। आपका पुनः स्वागत है!*
    """)
