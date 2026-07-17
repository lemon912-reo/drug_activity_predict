import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="AI Drug Discovery",
    page_icon="🧬",
    layout="wide"
)


# =========================
# 데이터
# =========================

data = {

"Rank": range(1,21),

"molecule_chembl_id":[
"CHEMBL440498",
"CHEMBL180616",
"CHEMBL361527",
"CHEMBL361527",
"CHEMBL181391",
"CHEMBL359716",
"CHEMBL180275",
"CHEMBL425341",
"CHEMBL178509",
"CHEMBL178163",
"CHEMBL181022",
"CHEMBL181372",
"CHEMBL361533",
"CHEMBL178749",
"CHEMBL178625",
"CHEMBL181562",
"CHEMBL178651",
"CHEMBL179177",
"CHEMBL180762",
"CHEMBL178652"
],

"Predicted_pIC50":[
8.805148,
7.412523,
7.238074,
7.238074,
7.234005,
7.181533,
7.160186,
7.160096,
7.152552,
7.152552,
7.127812,
7.118701,
7.104347,
7.066805,
7.058666,
7.020028,
6.994926,
6.570654,
6.542371,
6.357642
]

}


df=pd.DataFrame(data)



# 등급

def grade(x):

    if x>=8:
        return "⭐ 매우 유망"

    elif x>=7:
        return "🟢 유망"

    else:
        return "추가 검토"



df["Recommendation"] = df["Predicted_pIC50"].apply(grade)



# =========================
# 제목
# =========================

st.title(
"🧬 AI Drug Discovery Platform"
)


st.subheader(
"MMP13 Target-based Breast Cancer Candidate Screening"
)



st.info(
"""
MMP13 표적 단백질 관련 후보 화합물 20개를 대상으로
Random Forest 기반 AI 모델이 예상 활성도(pIC50)를 예측하고
후보 물질의 우선순위를 평가합니다.
"""
)



# =========================
# 전체 결과
# =========================

st.subheader(
"🏆 AI Prediction Ranking"
)


st.dataframe(
df,
use_container_width=True
)



# =========================
# Top5
# =========================

st.subheader(
"📊 Top 5 Candidate Visualization"
)


top5=df.head(5)



fig,ax=plt.subplots(figsize=(7,3))


ax.bar(
    top5["molecule_chembl_id"],
    top5["Predicted_pIC50"]
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



# =========================
# 최고 후보
# =========================

best=df.iloc[0]


st.success(
f"""
🏆 Best Candidate

Compound:
{best['molecule_chembl_id']}

Predicted pIC50:
{best['Predicted_pIC50']:.3f}

Evaluation:
{best['Recommendation']}
"""
)
