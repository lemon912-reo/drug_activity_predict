import streamlit as st
import pandas as pd
import numpy as np
import joblib

from chembl_webresource_client.new_client import new_client
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem



# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="AI Drug Discovery Platform",
    page_icon="🧬",
    layout="wide"
)


# =====================================================
# CSS 디자인
# =====================================================

st.markdown(
"""
<style>

.main {
    background-color: #f7fbfc;
}


h1 {
    color:#075985;
    font-weight:800;
}


h2 {
    color:#0f766e;
}


.stButton>button {

    width:100%;
    height:45px;

    border-radius:10px;

    background-color:#0f766e;

    color:white;

    font-size:16px;

    font-weight:bold;

}


.stButton>button:hover {

    background-color:#115e59;

}


div[data-testid="stMetric"] {

    background-color:white;

    border-radius:15px;

    padding:20px;

    box-shadow:
    0px 4px 12px rgba(0,0,0,0.08);

}


.info-card {

background-color:white;

padding:20px;

border-radius:15px;

box-shadow:
0px 4px 12px rgba(0,0,0,0.08);

margin-bottom:20px;

}


</style>

""",
unsafe_allow_html=True
)



# =====================================================
# 모델 및 ChEMBL 연결
# =====================================================

model = joblib.load(
    "drug_activity_model.pkl"
)


molecule = new_client.molecule



# =====================================================
# ChEMBL ID → SMILES
# =====================================================

def get_smiles(chembl_id):

    try:

        mol = molecule.get(
            chembl_id
        )


        if mol.get("molecule_structures") is None:

            return None


        return mol["molecule_structures"]["canonical_smiles"]


    except:

        return None



# =====================================================
# 약물명 → ChEMBL ID
# =====================================================

def search_chembl_id(name):

    try:

        result = molecule.search(name)


        if len(result)==0:

            return None


        return result[0]["molecule_chembl_id"]


    except:

        return None



# =====================================================
# SMILES → Fingerprint
# =====================================================

def smiles_to_fp(smiles):

    mol = Chem.MolFromSmiles(
        smiles
    )


    if mol is None:

        return None


    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius=2,
        nBits=2048
    )


    arr=np.zeros(
        (2048,),
        dtype=int
    )


    DataStructs.ConvertToNumpyArray(
        fp,
        arr
    )


    return arr

# =====================================================
# AI 예측
# =====================================================

def predict_pIC50(chembl_id):


    smiles=get_smiles(
        chembl_id
    )


    if smiles is None:

        return None,None


    fp=smiles_to_fp(
        smiles
    )


    if fp is None:

        return None,smiles


    X=np.array(fp).reshape(
        1,-1
    )


    prediction=model.predict(
        X
    )[0]


    return prediction,smiles



# =====================================================
# 활성 등급
# =====================================================

def recommendation(score):

    if score>=8:

        return "⭐ 매우 유망"

    elif score>=7:

        return "🟢 유망"

    else:

        return "추가 검토"



# =====================================================
# Sidebar
# =====================================================

with st.sidebar:


    st.header("🧬 AI Drug Discovery")


    st.write(
"""
**Target**

🎯 MMP13


**Disease**

🩺 Breast Cancer


**Model**

🤖 Random Forest Regression


**Input**

Chemical Structure


**Output**

Predicted pIC50

"""
)


    st.divider()


    st.caption(
        "ChEMBL + RDKit + Machine Learning"
    )



# =====================================================
# Main Title
# =====================================================


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

유방암 관련 표적 유전자 MMP13을 대상으로 화합물의 분자 구조 정보를 분석하고 
AI 모델을 활용하여 예상 활성도(pIC50)를 예측합니다.

</div>

""",
unsafe_allow_html=True
)



# =====================================================
# 분석 방법 선택
# =====================================================

mode = st.radio(
    "분석 방법 선택",
    [
        "후보 약물 리스트 비교",
        "직접 화합물 검색"
    ]
)



# =====================================================
# 1. 후보군 비교
# =====================================================


if mode=="후보 약물 리스트 비교":


    st.subheader(
        "📋 후보 화합물 Screening"
    )


    uploaded_file=st.file_uploader(
        "candidate.csv 업로드",
        type="csv"
    )


    if uploaded_file:


        candidate=pd.read_csv(
            uploaded_file
        )


        st.dataframe(
            candidate
        )


        if st.button(
            "AI Screening 실행"
        ):


            results=[]


            for chembl_id in candidate["molecule_chembl_id"]:


                score,smiles=predict_pIC50(
                    chembl_id
                )


                if score is not None:


                    results.append(
                    {
                    "molecule_chembl_id":chembl_id,
                    "Predicted_pIC50":round(score,3),
                    "Recommendation":recommendation(score)
                    }
                    )



            result_df=pd.DataFrame(
                results
            )


            result_df=result_df.sort_values(
                "Predicted_pIC50",
                ascending=False
            ).reset_index(drop=True)



            result_df.insert(
                0,
                "Rank",
                range(1,len(result_df)+1)
            )


            st.subheader(
                "🏆 AI Prediction Ranking"
            )


            st.dataframe(
                result_df,
                use_container_width=True
            )



# =====================================================
# 2. 직접 검색
# =====================================================


else:


    st.subheader(
        "🔍 Candidate Molecule Search"
    )


    input_type=st.selectbox(
        "검색 방법",
        [
            "ChEMBL ID",
            "약물명 / 화합물명"
        ]
    )


    user_input=st.text_input(
        "화합물 입력",
        placeholder="예: CHEMBL440498 또는 CTS-1027"
    )



    if st.button(
        "AI Prediction 실행"
    ):


        if input_type=="약물명 / 화합물명":

            chembl_id=search_chembl_id(
                user_input
            )

        else:

            chembl_id=user_input



        if chembl_id is None:


            st.error(
                "화합물을 찾을 수 없습니다."
            )


        else:


            score,smiles=predict_pIC50(
                chembl_id
            )



            if score is None:


                st.error(
                    "SMILES 정보를 가져올 수 없습니다."
                )


            else:


                st.success(
                    f"{chembl_id} 분석 완료"
                )



                st.subheader(
                    "📊 AI Prediction Result"
                )


                col1,col2,col3=st.columns(3)


                with col1:

                    st.metric(
                        "Predicted pIC50",
                        round(score,3)
                    )


                with col2:

                    st.metric(
                        "Activity",
                        recommendation(score)
                    )


                with col3:

                    st.metric(
                        "Target",
                        "MMP13"
                    )



                st.subheader(
                    "🧬 Molecular Information"
                )

                st.write("**SMILES Structure**")

                st.code(
                        smiles
                )


        
