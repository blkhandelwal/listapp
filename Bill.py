import os
import streamlit as st
import pandas as pd

# Page Configuration Setup
st.set_page_config(
    page_title="Khandelwal App",
    layout="wide"
)

# Custom CSS Styling and Top Marquee Banner
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.9rem !important;
        }
        .stAppDeployButton {
            display: none !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 2px solid green !important;
            border-radius: 8px;
        }
        div[data-testid="stTextInput"] input {
            background-color: #1e88e5 !important;
            color: white !important;
            font-weight: bold;
        }
        div[data-testid="stTextInput"] label {
            color: #0d47a1;
            font-weight: bold;
        }
    </style>
    <div style="position:fixed; top:0; left:0; width:100%; background:red; color:white; font-size:18px; font-weight:bold; z-index:999999;">
        <marquee behavior="scroll" direction="left" scrollamount="3">
            khandelwal software Aapaka Hardik Swagat Karta h
        </marquee>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Main App Title Header
st.markdown("Khandelwal APP")

# Session State Initialization for Terms & Conditions Check
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None

# Terms & Conditions Agreement Screen
if st.session_state.user_choice is None:
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        agree = col1.checkbox("I Am Agree")
        not_agree = col2.checkbox("I Am Not agree")
        
        if agree:
            st.session_state.user_choice = 'agree'
            st.rerun()
            
        if not_agree:
            st.session_state.user_choice = 'not_agree'
            st.rerun()
            
        st.divider()
        
        with st.container(height=200):
            st.markdown("**Terms & Conditions**")
            st.markdown(
                """
                1. Developed for members convenience.
                2. App owner is not responsible for data errors.
                3. Verify details independently.
                4. Free of cost service.
                5. Follow organization guidelines.
                6. This app is currently provided completely free of charge to all members.
                7. The organization and app management reserve the right to alter or modify app rules, features, or services at any time.
                8. All users using the app must strictly follow the guidelines of the organization.
                9. If any member or organization worker spreads incorrect information or rumors, the app owner reserves the right to completely shut down the app.
                10. If members experience any inconvenience while using the app, the app owner may terminate/shut down the app service.
                11. No legal action can be initiated against the app owner (developer) in case of any error, incorrect data, or dispute arising from the app.
                12. Using this app implies that you fully understand and agree to all the terms and conditions listed above.
                """)

# Main Application Logic (Executed after Agree)
elif st.session_state.user_choice == 'agree':
    
    st.markdown("Balai Svyam Seva Sasthan Surpura")
    
    # Automatically locate files relative to script directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE1_PATH = os.path.join(BASE_DIR, "LTM.csv")
    FILE2_PATH = os.path.join(BASE_DIR, "Rd.csv")

    def load_ltm_data(path, header_row=0):
        if os.path.exists(path):
            return pd.read_csv(path, dtype=str, header=header_row)
        return None

    def load_rd_data(path, header_row=0):
        if os.path.exists(path):
            return pd.read_csv(path, dtype=str, header=header_row)
        return None

    df1 = load_ltm_data(FILE1_PATH, header_row=2)

    if df1 is None:
        st.error(f"LTM फाइल नहीं मिली! कृपया पाथ जांचें: {FILE1_PATH}")
    else:
        df1.columns = df1.columns.astype(str).str.strip().str.lower()
        
        if 'phone' in df1.columns:
            df1['phone'] = df1['phone'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

        search_val = st.text_input("मोबाइल नंबर दर्ज करें:").strip()

        if search_val:
            if "phone" in df1.columns and "a/c no." in df1.columns:
                
                matched_df = df1[
                    df1["phone"].str.contains(search_val, na=False, regex=False) | 
                    df1["a/c no."].astype(str).str.contains(search_val, na=False, regex=False)
                ]
                
                ltm_count = len(matched_df)

                if ltm_count > 0:
                    acc_set = set(
                        matched_df["a/c no."]
                        .astype(str)
                        .str.strip()
                        .dropna()
                        .tolist()
                    )
                    
                    with st.spinner("डेटा खोजा जा रहा है..."):
                        df2 = load_rd_data(FILE2_PATH, header_row=3)

                        if df2 is not None:
                            df2.columns = df2.columns.astype(str).str.strip().str.lower()
                            
                            if "a/c no." in df2.columns:
                                final_records = df2[df2["a/c no."].astype(str).str.strip().isin(acc_set)].copy()
                                rd_count = len(final_records)

                                total_sum = 0.0
                                loan_sum = 0.0
                                display_df = pd.DataFrame()

                                if not final_records.empty:
                                    
                                    for col in ['name', 'naam']:
                                        if col in final_records.columns:
                                            final_records = final_records.drop(columns=[col])
                                    
                                    if 'name' in df1.columns:
                                        ltm_names = df1[['a/c no.', 'name']].drop_duplicates(subset=['a/c no.'])
                                        ltm_names['a/c no.'] = ltm_names['a/c no.'].astype(str).str.strip()
                                        final_records['a/c no.'] = final_records['a/c no.'].astype(str).str.strip()
                                        
                                        final_records = pd.merge(final_records, ltm_names, on='a/c no.', how='left')
                                        
                                        cols = list(final_records.columns)
                                        cols.remove('name')
                                        cols.insert(cols.index('a/c no.') + 1, 'name')
                                        final_records = final_records[cols]

                                    if "discount" in final_records.columns:
                                        final_records = final_records.drop(columns=["discount"])

                                    for c in final_records.columns:
                                        if 'date' in c or 'दिनांक' in c:
                                            final_records[c] = pd.to_datetime(
                                                final_records[c], 
                                                errors='coerce'
                                            ).dt.strftime('%d-%m-%y').fillna(final_records[c])

                                    col_map = {c.lower(): c for c in final_records.columns}
                                    
                                    t_col = next((col_map[k] for k in col_map if 'total' in k or 'tot' in k), None)
                                    
                                    l_col = None
                                    for key in col_map:
                                        if 'total re' in key or 'total_re' in key or 'total-re' in key or 'loan re' in key or key == 'loan_re':
                                            l_col = col_map[key]
                                            break
                                    if not l_col:
                                        for key in col_map:
                                            if 're' in key or 'loan' in key:
                                                l_col = col_map[key]
                                                break

                                    if t_col:
                                        final_records[t_col] = pd.to_numeric(
                                            final_records[t_col].astype(str).str.replace(',', ''), 
                                            errors='coerce'
                                        ).fillna(0)
                                        total_sum = final_records[t_col].sum()

                                    if l_col:
                                        final_records[l_col] = pd.to_numeric(
                                            final_records[l_col].astype(str).str.replace(',', ''), 
                                            errors='coerce'
                                        ).fillna(0)
                                        loan_sum = final_records[l_col].sum()

                                    total_row = {}
                                    for col in final_records.columns:
                                        num_series = pd.to_numeric(
                                            final_records[col].astype(str).str.replace(',', ''), 
                                            errors='coerce'
                                        )
                                        if num_series.notna().sum() > 0:
                                            total_row[col] = num_series.sum()
                                        else:
                                            total_row[col] = ""
                                            
                                    total_row[final_records.columns[0]] = "Total"
                                    display_df = pd.concat([final_records, pd.DataFrame([total_row])], ignore_index=True)

                                diff = total_sum - loan_sum
                                
                                c1, c2, c3, c4, c5 = st.columns(5)
                                
                                c1.markdown(f"**A/c**<br><span style='font-size: 20px;'>{ltm_count}</span>", unsafe_allow_html=True)
                                c2.markdown(f"**Bill**<br><span style='font-size: 20px;'>{rd_count}</span>", unsafe_allow_html=True)
                                c3.markdown(f"**Total**<br><span style='font-size: 20px;'>{int(round(total_sum)):,}</span>", unsafe_allow_html=True)
                                c4.markdown(f"**Loan**<br><span style='font-size: 20px;'>{int(round(loan_sum)):,}</span>", unsafe_allow_html=True)
                                
                                color_style = "color: #c62828;" if diff < 0 else ""
                                c5.markdown(f"**Cash**<br><span style='{color_style} font-size: 20px;'>{int(round(diff)):,}</span>", unsafe_allow_html=True)

                                st.write("")
                                
                                if not final_records.empty:
                                    def highlight_total(row):
                                        if (row.astype(str) == "Total").any():
                                            return ['color: red; font-weight: bold;' for _ in row]
                                        return ['' for _ in row]

                                    styled_df = display_df.style.apply(highlight_total, axis=1)
                                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                                else:
                                    st.warning("इस महीने में आपने बिल नहीं कटवाया है।")
                            else:
                                st.error("RD फाइल में 'a/c no.' कॉलम नहीं मिला।")
                        else:
                            st.error(f"RD फाइल नहीं मिल सकी! कृपया जाँचें: {FILE2_PATH}")
                else:
                    st.warning("मोबाइल नंबर गलत है।")
            else:
                st.error("LTM फाइल में आवश्यक कॉलम नहीं मिले।")

    # Footer Information Section
    with st.container(height=200):
        st.info("**संस्था का मुख्य उद्देश्य:** समाज के हर परिवार को आर्थिक रूप से आज़ाद करना और ब्याज-खोरों के जाल से बचाना है।")
        st.markdown(
            """
            * यह संस्था आपकी अपनी है।
            * हम सबको मिलकर इसका सहयोग करना चाहिए।
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
        
    st.success("आइए, हम सब मिलकर इस संस्था को मजबूत बनाएं!")

# Not Agree Screen Option
elif st.session_state.user_choice == 'not_agree':
    st.markdown(
        "खंडेलवाल ऐप में आपका स्वागत है! "
        "यदि आप नियमों से असहमत हैं, तो डेटा प्रदर्शित नहीं किया जाएगा। "
        "पेज रीफ्रेश करके दोबारा कोशिश कर सकते हैं।"
    )
