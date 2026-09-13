import streamlit as st
import pandas as pd

st.set_page_config(page_title="list", layout="wide")

# Top marquee background style
st.markdown("""
<style>
    .block-container {padding-top: 1.9rem !important;}
    .stAppDeployButton {display: none !important;}
</style>
<div style="position:fixed; top:0; left:0; width:100%; background:green; color:white; font-size:18px; font-weight:bold; z-index:999999;">
    <marquee behavior="scroll" direction="left" scrollamount="3">khandelwal software Aapaka Hardik Swagat Karta h</marquee>
</div>
<br>
""", unsafe_allow_html=True)

# Ye heading hamesha screen par sabse upar dikhegi
st.markdown("Balai Svyam Seva Sasthan Surpura")

# Container with English Terms & Conditions
with st.container(border=True):
    st.markdown("Terms & Conditions")
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
    st.divider()
    col1, col2 = st.columns(2)
    agree = col1.checkbox("I Agree")
    not_agree = col2.checkbox("I Disagree")

# Checkbox click hone par keval Terms & Conditions wala container hide hoga
if agree or not_agree:
    st.markdown("<style>[data-testid='stVerticalBlock'] > div:has(div.stCheckbox) {display: none !important;}</style>", unsafe_allow_html=True)

# "I Agree" tick hone par data load hoga
if agree:
    try:
        raw_df = pd.read_csv("LTM.csv", header=None, nrows=2, encoding='latin-1')
        file_date = raw_df.iloc[1, 0] if len(raw_df) > 1 else ""
        df = pd.read_csv("LTM.csv", header=2, encoding='latin-1').dropna(how='all')
        df.columns = df.columns.str.strip()
        
        if 'phone' in df.columns:
            df['phone'] = df['phone'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        #st.success("✅ Aapne shartien sweekar kar li hain.")
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
    except Exception as e:
        st.error(f"Error: {e}")

# "I Disagree" tick hone par container hide ho jayega aur ye msg aayega
elif not_agree:
    st.error("❌ Aapne shartien sweekar nahi ki hain. Data load nahi hoga.")
