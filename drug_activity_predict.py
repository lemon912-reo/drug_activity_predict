import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =====================================
# Page Setting
# =====================================

st.set_page_config(
    page_title="AI Drug Discovery",
    page_icon="🧬",
    layout="wide"
)



# =====================================
# CSS
# =====================================

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


.card {

background:white;

padding:15px;

border-radius:18px;

border:1px solid #e5e7eb;

box-shadow:
0px 6px 15px rgba(0,0,0,0.08);

text-align:center;

height:150px;

}


.card h3 {

color:#075985;

margin:5px;

}


.card h4 {

color:#0f766e;

margin:0;

}


</style>

""",
unsafe_allow_html=True
)



# =====================================
# Data
# =====================================


result = pd.DataFrame({

"Rank":
range(1,21),

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
8.805,
7.413,
7.238,
7.238,
7.234,
7.182,
7.160,
7.160,
7.153,
7.153,
7.128,
7.119,
7.104,
7.067,
7.059,
7.020,
6.995,
6.571,
6.542,
6.358
]

})


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



# =====================================
# Title
# =====================================


st.markdown(
"""
# 🧬 AI Drug Discovery Platform

## MMP13 Target-based Breast Cancer Candidate Screening

"""
)



st.markdown(
"""
<div class="card">

<b>🔬 Research Goal</b>

MMP13 관련 후보 화합물의 분자 구조 정보를 기반으로 Random Forest AI 모델이 예상 활성도(pIC50)를 예측하고  
신약 후보 물질의 우선순위를 평가합니다.

</div>

""",
unsafe_allow_html=True
)



# =====================================
# Model Info
# =====================================


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



# =====================================
# Ranking Table
# =====================================


st.subheader(
"🏆 AI Prediction Ranking"
)


st.dataframe(
result,
use_container_width=True,
hide_index=True
)



# =====================================
# Top Candidate Cards
# =====================================


st.subheader(
"⭐ Top 5 Candidate Molecules"
)


cols = st.columns(5)


for i in range(5):

    row=result.iloc[i]

    with cols[i]:

        st.markdown(
        f"""
        <div class="card">

        🏆 Rank {row['Rank']}

        <br><br>

        <b>{row['molecule_chembl_id']}</b>

        <br><br>

        pIC50

        <h3>
        {row['Predicted_pIC50']:.3f}
        </h3>

        {row['Recommendation']}

        </div>

        """,
        unsafe_allow_html=True
        )



# =====================================
# Visualization
# =====================================

st.subheader(
    "📊 Candidate Ranking Visualization"
)


# Top 5 강조
result["Highlight"] = result["Rank"].apply(
    lambda x: "Top 5" if x <= 5 else "Others"
)


fig, ax = plt.subplots(
    figsize=(6, 2.8)
)


# 색상 지정
colors = [
    "#0f766e" if rank <= 5 else "#cbd5e1"
    for rank in result["Rank"]
]


ax.bar(
    result["Rank"],
    result["Predicted_pIC50"],
    color=colors,
    width=0.7
)


# 제목
ax.set_title(
    "AI Predicted pIC50 Ranking",
    fontsize=10,
    pad=10
)


ax.set_xlabel(
    "Candidate Rank",
    fontsize=8
)


ax.set_ylabel(
    "Predicted pIC50",
    fontsize=8
)



# 축 폰트
ax.tick_params(
    axis="both",
    labelsize=7
)


# x축 간격
ax.set_xticks(
    result["Rank"]
)


# 격자
ax.grid(
    axis="y",
    alpha=0.3
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=False
)




# =====================================
# Summary
# =====================================


best=result.iloc[0]


st.markdown(
f"""
<div class="card">

<h3>🧬 AI Screening Result</h3>


가장 높은 예측 활성도를 보인 후보 물질은 <b>{best['molecule_chembl_id']}</b>이며, 예측 pIC50 값은 <b>{best['Predicted_pIC50']:.3f}</b>입니다.


AI 모델 기반 분석 결과, 해당 화합물이 MMP13 억제 후보 물질로서 가장 높은 우선순위를 가집니다.




</div>

""",
unsafe_allow_html=True
)
