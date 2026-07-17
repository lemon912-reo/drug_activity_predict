import streamlit as st
import pandas as pd


# -----------------------------
# 페이지 설정
# -----------------------------

st.set_page_config(
    page_title="AI Drug Discovery Platform",
    page_icon="🧬",
    layout="wide"
)


# -----------------------------
# CSS
# -----------------------------

st.markdown(
"""
<style>

.main{
background-color:#f7fbfc;
}

h1{
color:#075985;
font-weight:800;
}

.info-card{

background:white;
padding:20px;
border-radius:15px;

box-shadow:
0px 4px 12px rgba(0,0,0,0.08);

}

</style>

""",
unsafe_allow_html=True
)



# -----------------------------
# 제목
# -----------------------------

st.markdown(
"""
# 🧬 AI 유방암 억제 후보 물질 예측

## MMP13 Target-based Breast Cancer Candidate Screening

"""
)


st.markdown(
"""
<div class="info-card">

<b>🔬 연구 목적</b>

유방암 관련 표적 단백질 MMP13에 대한 후보 화합물의 활성 데이터를 기반으로 AI 모델이 예상 활성도(pIC50)를 평가하고
우선순위 후보 물질을 탐색합니다.

</div>

""",
unsafe_allow_html=True
)



# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("🧬 Research Information")

    st.write(
"""
🎯 Target  
MMP13

🩺 Disease  
Breast Cancer

🤖 Model  
Random Forest Regression

📊 Output  
Predicted pIC50

"""
)


# -----------------------------
# 파일 업로드
# -----------------------------


st.subheader("📋 Candidate Molecule Screening")


uploaded_file = st.file_uploader(
    "AI 예측 결과 CSV 업로드",
    type="csv"
)



if uploaded_file:


    df=pd.read_csv(uploaded_file)


    st.subheader(
        "Candidate Molecules"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


    st.divider()


    # 상위 후보 강조

    st.subheader(
        "🏆 AI Prediction Ranking"
    )


    if "Predicted_pIC50" in df.columns:


        df=df.sort_values(
            "Predicted_pIC50",
            ascending=False
        )


        df=df.reset_index(drop=True)


        df.insert(
            0,
            "Rank",
            range(1,len(df)+1)
        )


        st.dataframe(
            df,
            use_container_width=True
        )


        best=df.iloc[0]


        st.success(
            f"""
🥇 최우수 후보

{best['molecule_chembl_id']}

예측 pIC50 : {best['Predicted_pIC50']}
"""
        )


    else:

        st.warning(
        """
CSV 파일에 Predicted_pIC50 컬럼이 없습니다.
AI 예측 결과 파일을 업로드해주세요.
"""
        )
