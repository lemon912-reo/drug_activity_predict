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

padding:20px;

border-radius:15px;

box-shadow:
0px 4px 12px rgba(0,0,0,0.08);

margin-bottom:20px;

}


.rank-card {

background:white;

padding:15px;

border-radius:12px;

box-shadow:
0px 3px 10px rgba(0,0,0,0.08);

text-align:center;

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

<b>🔬 Research Goal</b>

<br><br>

유방암 관련 표적 단백질 MMP13에 작용하는 후보 화합물을 대상으로  
분자 구조 정보를 기반으로 학습한 Random Forest 모델을 활용하여  
예상 활성도(pIC50)를 예측하고 후보 물질의 우선순위를 평가합니다.

</div>

""",
unsafe_allow_html=True
)



# ==============================
# Model Information
# ==============================

col1,col2,col3 = st.columns(3)


with col1:
    st.metric(
        "Target",
        "MMP13"
    )


with col2:
    st.metric(
        "Disease",
        "Breast Cancer"
    )


with col3:
    st.metric(
        "Model",
        "Random Forest"
    )



# ==============================
# Result Data
# ==============================


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



result["Recommendation"] = result["Predicted_pIC50"].apply(grade)



# ==============================
# Ranking Table
# ==============================


st.subheader(
"🏆 AI Prediction Ranking"
)


st.dataframe(
    result,
    use_container_width=True,
    hide_index=True
)



# ==============================
# Top 5 Cards
# ==============================


st.subheader(
"🥇 Top 5 Candidate Molecules"
)


top5=result.head(5)



cols=st.columns(5)


for i,(_,row) in enumerate(top5.iterrows()):

    with cols[i]:

        st.markdown(
        f"""

        <div class="rank-card">

        🏆 Rank {row['Rank']}

        <br><br>

        <b>{row['molecule_chembl_id']}</b>

        <br><br>

        pIC50

        <br>

        <b>{row['Predicted_pIC50']:.3f}</b>

        <br><br>

        {row['Recommendation']}

        </div>

        """,
        unsafe_allow_html=True
        )



# ==============================
# Visualization
# ==============================


st.subheader(
"📊 Candidate Activity Distribution"
)


fig,ax=plt.subplots(
    figsize=(8,6)
)


plot_df=result.sort_values(
    "Predicted_pIC50"
)


ax.barh(
    plot_df["molecule_chembl_id"],
    plot_df["Predicted_pIC50"]
)


ax.set_xlabel(
"Predicted pIC50"
)


ax.set_ylabel(
"Candidate Molecule"
)


plt.tight_layout()


st.pyplot(fig)



# ==============================
# Final Candidate
# ==============================


best=result.iloc[0]


st.markdown(
f"""

<div class="card">


<h3>🎯 AI Recommended Candidate</h3>


<b>Molecule ID</b>

<br>

{best['molecule_chembl_id']}


<br><br>


<b>Predicted pIC50</b>

<br>

{best['Predicted_pIC50']:.3f}


<br><br>


<b>Evaluation</b>

<br>

{best['Recommendation']}


</div>


""",
unsafe_allow_html=True
)
