import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# ==============================
# Page Setting
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

.main{
background-color:#f7fbfc;
}


h1{
color:#075985;
font-weight:800;
}


h2{
color:#0f766e;
}


.card{

background:white;

padding:20px;

border-radius:15px;

box-shadow:0px 4px 12px rgba(0,0,0,0.1);

margin-bottom:20px;

}

</style>
""",
unsafe_allow_html=True
)



# ==============================
# Title
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

<br><br>

유방암 관련 표적 단백질 MMP13에 대한 후보 화합물을 선정하고,
AI 기반 모델(Random Forest)을 이용하여 예상 활성도(pIC50)를 평가하여
신약 후보 물질의 우선순위를 분석합니다.

</div>

""",
unsafe_allow_html=True
)



# ==============================
# Result Data
# ==============================


result = pd.DataFrame({

"Rank":[
1,2,3,4,5,6,7,8,9,10,
11,12,13,14,15,16,17,18,19,20
],

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
],

"Recommendation":[
"매우 유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"유망",
"-",
"-",
"-",
"-"
]

})



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


Prediction

Predicted pIC50

"""
    )



# ==============================
# Ranking Table
# ==============================

st.subheader(
"🏆 AI Candidate Ranking"
)


st.dataframe(
    result,
    use_container_width=True
)



# ==============================
# Top 5 Visualization
# ==============================

st.subheader(
"📊 Top 5 Candidate Molecules"
)


top5=result.head(5)



fig,ax=plt.subplots(
    figsize=(8,4)
)


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



# ==============================
# Best Candidate
# ==============================

best=result.iloc[0]


st.subheader(
"⭐ AI Selected Candidate"
)


st.markdown(
f"""

<div class="card">

<h3>{best['molecule_chembl_id']}</h3>


Predicted pIC50 :

<b>{best['Predicted_pIC50']:.3f}</b>


<br><br>


Evaluation :

<b>{best['Recommendation']}</b>


<br><br>

AI 모델 기준 가장 높은 예상 활성도를 보여
MMP13 억제 후보 물질 중 우선 검토 대상으로 선정되었습니다.

</div>

""",
unsafe_allow_html=True
)



# ==============================
# Interpretation
# ==============================

st.subheader(
"📌 Interpretation"
)


st.write(
"""
- pIC50 값이 높을수록 적은 농도에서 높은 활성을 보일 가능성이 있습니다.
- 본 결과는 AI 기반 초기 후보 물질 선별(screening) 단계입니다.
- 실제 신약 개발 과정에서는 추가적인 실험 검증이 필요합니다.
"""
)
