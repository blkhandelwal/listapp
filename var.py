import streamlit as st
import pandas as pd

st.set_page_config(page_title="list", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem !important;}
    .stAppDeployButton {display: none !important;}
</style>
<div style="position:fixed; top:0; left:0; width:100%; background:green; color:white; font-size:18px; font-weight:bold; z-index:999999;">
    <marquee behavior="scroll" direction="left" scrollamount="3">khandelwal software Aapaka Hardik Swagat Karta h</marquee>
</div>
""", unsafe_allow_html=True)

st.markdown("Balai Svyam Seva Sasthan       Surpura")

# Container me shartien aur Checkboxes
with st.container(border=True):
    st.subheader("Niyam aur Shartien (Terms & Conditions)")
    st.write("1. Aapko sabhi niyamo ka palan karna hoga.\n2. Di gayi jankari poori tarah sahi honi chahiye.\n3. Kisi bhi galat jankari ke liye aap swayam zimmedar honge.")
    st.divider()
    col1, col2 = st.columns(2)
    agree = col1.checkbox("I am agree")
    not_agree = col2.checkbox("I am not agree")

# "I am agree" tick hone par container hat jayega aur code chalega
if agree:
    st.markdown("<style>[data-testid='stVerticalBlock'] > div:has(div.stCheckbox) {display: none !important;}</style>", unsafe_allow_html=True)
    try:
        raw_df = pd.read_csv("LTM.csv", header=None, nrows=2, encoding='latin-1')
        file_date = raw_df.iloc[1, 0] if len(raw_df) > 1 else ""
        df = pd.read_csv("LTM.csv", header=2, encoding='latin-1').dropna(how='all')
        df.columns = df.columns.str.strip()
        
        if 'phone' in df.columns:
            df['phone'] = df['phone'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        st.success("✅ Aapne shartien sweekar kar li hain.")
        st.markdown(f"<div style='display:flex; justify-content:space-between;'><b>Mobile Number Enter Karein:</b><b style='color:#1f77b4;'>List Date: {file_date}</b></div>", unsafe_allow_html=True)
        
        # Fixed Empty Label Warning
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
                
                # Sabhi columns ko string me convert karke Arrow error fix kiya gaya hai
                final = pd.concat([res, pd.DataFrame([sums])], ignore_index=True).fillna('')
                for col in final.columns:
                    final[col] = final[col].astype(str).str.replace(r'\.0$', '', regex=True)
                
                st.success(f"✅ {len(res)} records mile | 💰 Total Amount: ₹{int(total_amount):,d}")
                
                if 'phone' in final.columns: 
                    final = final.drop(columns=['phone'])
                
                # Updated width='stretch' for new Streamlit standard
                st.dataframe(
                    final.style.apply(lambda r: ['background-color: #ffcccc; color: #cc0000; font-weight: bold']*len(r) if r.get('Name') == 'TOTAL' else ['']*len(r), axis=1),
                    width="stretch", 
                    hide_index=True
                )
            else:
                st.warning(f"❌ Number '{val}' nahi mila!")
    except Exception as e:
        st.error(f"Error: {e}")

elif not_agree:
    st.error("❌ Aapne shartien sweekar nahi ki hain. Data load nahi hoga.")
