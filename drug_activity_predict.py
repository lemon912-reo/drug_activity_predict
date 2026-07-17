import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt


# ==============================
# 페이지 설정
# ==============================

st.set_page_config(
    page_title="AI Drug Discovery",
    page_icon="🧬",
    layout="wide"
)



# ==============================
# CSS
# ==============================

st.markdown(
"""
<style>

.main {
background-color:#f7fbfc;
}


h1 {
color:#075985;
font-weight:800;
}


h2 {
color:#0f766e;
}


.stButton button {

background-color:#0f766e;
color:white;

width:100%;
height:45px;

border-radius:10px;

font-weight:bold;

}

.card {

background:white;

padding:20px;

border-radius:15px;

box-shadow:0px 4px 12px rgba(0,0,0,0.1);

}

</style>

""",
unsafe_allow_html=True
)



# ==============================
# 모델 불러오기
# ==============================

model = joblib.load(
    "drug_activity_model.pkl"
)



# ==============================
# 제목
# ==============================


st.markdown(
"""
# 🧬 AI Drug Discovery Platform

## MMP13 Target-based Breast Cancer Candidate Screening

"""
)


st.markdown(
"""
<div class="card">

<b>Research Goal</b>

MMP13 표적 단백질과 관련된 후보 화합물의 분자 구조 정보를 기반으로  
Random Forest 모델이 예상 활성도(pIC50)를 예측하고  
신약 후보 우선순위를 평가합니다.

</div>

""",
unsafe_allow_html=True
)



st.write("")



# ==============================
# Sidebar
# ==============================

with st.sidebar:

    st.header("🧬 Model Information")

    st.write(
"""
Target

🎯 MMP13


Disease

🩺 Breast Cancer


Model

🤖 Random Forest Regression


Output

Predicted pIC50

"""
    )



# ==============================
# 파일 업로드
# ==============================


st.subheader(
"📂 Candidate Molecule Dataset"
)


uploaded_file = st.file_uploader(
    "candidate.csv 업로드",
    type="csv"
)



if uploaded_file:


    candidate = pd.read_csv(
        uploaded_file
    )


    st.write("입력 후보 물질")

    st.dataframe(
        candidate,
        use_container_width=True
    )



    if st.button(
        "🚀 AI Prediction 실행"
    ):


        with st.spinner(
            "AI 모델이 후보 물질을 분석 중입니다..."
        ):


            # -------------------------
            # fingerprint는 이미 저장되어 있다고 가정
            # -------------------------

            X = np.stack(
                candidate["fingerprint"].values
            )


            prediction = model.predict(X)


            result = candidate.copy()


            result["Predicted_pIC50"] = prediction


            result = result.sort_values(
                "Predicted_pIC50",
                ascending=False
            ).reset_index(drop=True)



            result.insert(
                0,
                "Rank",
                range(1,len(result)+1)
            )



            # 등급 추가

            def grade(x):

                if x>=8:
                    return "⭐ 매우 유망"

                elif x>=7:
                    return "🟢 유망"

                else:
                    return "추가 검토"


            result["Recommendation"] = (
                result["Predicted_pIC50"]
                .apply(grade)
            )



        st.success(
            "AI Prediction 완료"
        )



        # ==============================
        # 결과 출력
        # ==============================


        st.subheader(
            "🏆 Candidate Ranking"
        )


        st.dataframe(
            result[
            [
            "Rank",
            "molecule_chembl_id",
            "activity_type",
            "activity_value",
            "Predicted_pIC50",
            "Recommendation"
            ]
            ],
            use_container_width=True
        )



        # ==============================
        # Top 후보 그래프
        # ==============================


        st.subheader(
            "📊 Top Candidate Visualization"
        )


        top10 = result.head(10)



        fig,ax = plt.subplots(
            figsize=(10,5)
        )


        ax.bar(
            top10["molecule_chembl_id"],
            top10["Predicted_pIC50"]
        )


        ax.set_ylabel(
            "Predicted pIC50"
        )


        ax.set_xlabel(
            "Compound"
        )


        plt.xticks(
            rotation=45,
            ha="right"
        )


        st.pyplot(fig)



        # ==============================
        # Scatter Plot
        # ==============================


        st.subheader(
            "📈 Activity vs AI Prediction"
        )


        fig2,ax2 = plt.subplots(
            figsize=(8,5)
        )


        ax2.scatter(
            result["activity_value"],
            result["Predicted_pIC50"]
        )


        ax2.set_xlabel(
            "Experimental Activity Value"
        )


        ax2.set_ylabel(
            "AI Predicted pIC50"
        )


        st.pyplot(fig2)



        # ==============================
        # 최고 후보 강조
        # ==============================


        best = result.iloc[0]


        st.markdown(
        f"""
        <div class="card">

        🏆 <b>AI Selected Candidate</b>

        <br><br>

        Compound :
        {best['molecule_chembl_id']}

        <br>

        Predicted pIC50 :
        {best['Predicted_pIC50']:.3f}

        <br>

        Evaluation :
        {best['Recommendation']}


        </div>

        """,
        unsafe_allow_html=True
        )
