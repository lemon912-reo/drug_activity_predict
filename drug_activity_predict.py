import streamlit as st
import pandas as pd
import numpy as np
import joblib
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
import matplotlib.pyplot as plt
import base64

# 페이지 설정 
# =====================================
st.set_page_config(
    page_title="AI Drug Discovery",
    page_icon="🧬",
    layout="wide")

with open("hero.jpg", "rb") as f:
    hero_base64 = base64.b64encode(f.read()).decode("utf-8")

# CSS
# =====================================
st.markdown(
f"""
<style>
/* 전체 배경 */
.stApp {background:linear-gradient(135deg,#f0f8fa,#ffffff);}
/* 제목 */
h1 {color:#075985;font-weight:800;}
h2 {color:#0f766e;}

# hero
# =====================================
/* Hero Banner */
/* Hero */

/* Hero Banner */

.hero{

background:
linear-gradient(
90deg,
rgba(7,89,133,0.82),
rgba(15,118,110,0.70)
),

url("data:image/jpeg;base64,{hero_base64}");

background-size:cover;

background-position:center;

padding:45px;

border-radius:25px;

color:white;

margin-bottom:25px;

box-shadow:0px 10px 25px rgba(0,0,0,0.15);

}

.hero h1{

color:white;

font-size:42px;

font-weight:800;

}

.hero h3{

color:#dbeafe;

}

.hero p{

font-size:18px;

max-width:700px;

line-height:1.6;

}
/* 카드 */
.card {background:linear-gradient(135deg,#ffffff,#f8fafc);
padding:20px;
border-radius:20px;
border:1px solid #dbeafe;
box-shadow:
0px 8px 20px rgba(15,118,110,0.12);
text-align:center;}
.card h3 {color:#075985;}
/* 표 */
[data-testid="stDataFrame"] {border-radius:15px;box-shadow:0px 5px 15px rgba(0,0,0,0.08);}
/* Sidebar */
section[data-testid="stSidebar"] {background-color:#f0fdfa;}
</style>
""",
unsafe_allow_html=True)

# Title
# =====================================
st.markdown(
"""
<div class="hero">

<h1>
🧬 AI 기반 신약 후보 물질 예측 시스템
</h1>

<h3>
MMP13 Target-based Breast Cancer Candidate Screening
</h3>

<p>
AI 기반 분자 구조 분석과 활성도 예측을 통해
MMP13 억제 후보 화합물의 활성을 예측하고
신약 후보의 우선순위를 평가하는 플랫폼입니다.
</p>

</div>
""",
unsafe_allow_html=True
)


# Model Info
# =====================================
with st.sidebar:
    st.header("🧬 Model Information")
    st.write(
"""
Target

🎯 MMP13

Disease

🩺 Breast Cancer Model

🤖 Random Forest Regression

Output

Predicted pIC50
"""
)

# 모델 불러오기 
# =====================================
@st.cache_resource
def load_model():
    return joblib.load("drug_activity_model.pkl")
rf_model = load_model()

# 후보 화합물 불러오기 
# =====================================
@st.cache_data
def load_candidates():
    return pd.read_csv("predict.csv")
candidate = load_candidates()

# Morgan Fingerprint 생성기
# =====================================
morgan_gen = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048)

# SMILES → Fingerprint
# =====================================
def smiles_to_fp(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = morgan_gen.GetFingerprint(mol)
    return np.array(fp)

# 추천 등급 함수
# =====================================
def recommendation(score):
    if score >= 8:
        return "⭐ 매우 유망"
    elif score >= 7:
        return "🟢 유망"
    else:
        return "추가 검토"

# 예측 함수
# =====================================
def predict_smiles(smiles):
    fp = smiles_to_fp(smiles)
    if fp is None:
        return None
    pred = rf_model.predict(np.array([fp]))[0]
    return pred





# Predict New Molecule
# =====================================
st.subheader("🧪 Predict New Molecule")
tab1, tab2 = st.tabs(["📚 추천 화합물", "✏️ 직접 SMILES 입력"])
with tab1:
    chembl = st.selectbox("후보 화합물을 선택하세요.",  candidate["molecule_chembl_id"])
    row = candidate[candidate["molecule_chembl_id"] == chembl].iloc[0]
col1, col2 = st.columns([1,2])
with col1:
    image_path = f"images/{chembl}.png"
    st.image(image_path, caption=chembl, use_container_width=True)
with col2:
    st.markdown("### 🔬 Molecule Information")
    st.write(f"**CHEMBL ID** : {chembl}")
    st.write(f"**Activity Type** : {row['activity_type']}")
    st.write(f"**Reported Value** : {row['activity_value']}")
    st.write(f"**SMILES**")
    st.code(row["smiles"], language="text")
if st.button("🧬 Predict pIC50", use_container_width=True):
    with st.spinner("AI가 분자 구조를 분석하는 중입니다..."):
        score = predict_smiles(row["smiles"])
        grade = recommendation(score)
st.success("Prediction Complete!")
st.markdown(
f"""
<div class="card">
<h2>Predicted pIC50</h2>
<h1>{score:.3f}</h1>
<h3>{grade}</h3>
</div>
""",
unsafe_allow_html=True)
if score >= 8:
    st.info("""
🧬 **AI Interpretation**

매우 높은 활성을 보일 것으로 예측되었습니다.

우선적으로 실험적 검증을 수행할 가치가 있는 후보입니다.
""")
elif score >= 7:
    st.info("""
🧬 **AI Interpretation**

활성이 기대되는 후보 화합물입니다.

후속 실험을 통한 검증이 권장됩니다.
""")
else:
    st.info("""
🧬 **AI Interpretation**

현재 모델 기준에서는 우선순위가 낮은 후보입니다.

추가적인 구조 최적화가 필요합니다.
""")
with tab2:
    smiles = st.text_area("SMILES를 입력하세요.")
    if st.button("Predict from SMILES"):
        score = predict_smiles(smiles)
        grade = recommendation(score)
        st.metric("Predicted pIC50", f"{score:.3f}")
        st.success(grade)
        

# Ranking Table
# =====================================
st.subheader("🏆 AI Prediction Ranking")
st.dataframe(result,use_container_width=True,hide_index=True)


# =====================================
# Top Candidate Cards
# =====================================
st.subheader("⭐ Top 5 Candidate Molecules")
cols = st.columns(5)
top5 = result.head(5)
for i, row in top5.iterrows():
    with cols[i]:
        image_path = f"images/{row['molecule_chembl_id']}.png"
        st.image(image_path, use_container_width=True)
        st.markdown(
        f"""
        <div class="card">
        <b>🏆 Rank {row['Rank']}</b><br><br>
        <b>{row['molecule_chembl_id']}</b>
        <br>
        pIC50
        <h2>{row['Predicted_pIC50']:.3f}</h2>
        {row['Recommendation']}
        </div>
        """,
        unsafe_allow_html=True)
        

# =====================================
# Visualization
# =====================================

st.subheader("📊 Candidate Ranking Visualization")

# Top 5 강조
result["Highlight"] = result["Rank"].apply(
    lambda x: "Top 5" if x <= 5 else "Others"
)

fig, ax = plt.subplots(figsize=(8,4))
colors = [
    "#0f766e" if r <= 5 else "#cbd5e1"
    for r in result["Rank"]]
bars = ax.bar(
    result["Rank"],
    result["Predicted_pIC50"],
    color=colors)
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x()+bar.get_width()/2,
        h+0.05,
        f"{h:.2f}",
        ha="center",
        fontsize=7)
ax.set_xlabel("Candidate Rank")
ax.set_ylabel("Predicted pIC50")
ax.set_title("AI Predicted Activity")
ax.grid(alpha=0.3)
st.pyplot(fig)


# =====================================
# Summary
# =====================================
best = result.iloc[0]
st.markdown(
f"""
<div class="card">
<h2>🧬 AI Screening Result</h2>
<br>
가장 높은 활성도를 예측한 후보는
<h3>{best['molecule_chembl_id']}</h3>
예측 활성도
<h1>{best['Predicted_pIC50']:.3f}</h1>
<b>{best['Recommendation']}</b><br><br>
Random Forest 모델 분석 결과,
해당 화합물이 MMP13 억제 후보 중
가장 높은 활성을 보일 것으로 예측되었습니다.
</div>
""",
unsafe_allow_html=True)

# 다운로드 기능 
# =====================================
csv = result.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Prediction Result",
    csv,
    file_name="prediction_result.csv",
    mime="text/csv"
)






