# Modules import
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import pickle
from lime import lime_tabular
import shap
import time

# Model loading
@st.cache(allow_output_mutation = True)
def load_model():
    with open('steps.pkl', 'rb') as file: # Load the objects from pickle file
        pk = pickle.load(file)
    return pk

pk = load_model() # Load the objects from pickle file

# Get objects stored in pickle file
classifier = pk['model']
label_encoder = pk['label_encoder']
pt_yeo_johnson = pk['pt_yeo_johnson']
x_train_smote = pk['x_train_smote']

# Function for showing the prediction page
def show_predict_page():
    st.sidebar.warning('Instruction/Guidance for LIME  \n'
                       '1. The Blue coloured bar represent its suppport towards the non-default class, whereas the Orange coloured bar represent its support towards the default class  \n'
                       '2. The leftmost section will reveal the prediction probabilities of the non-default and default class  \n'
                       '3. The middle section will reveal the top 10 most important features that contribute to the prediction of each class  \n'
                       '4. The rightmost section consists of the top 10 features along with the values that are colour-coded according to the support towards the predictive class')
    st.markdown('--------------------------')
    
    # Input selection box 
    pho = ('MORTGAGE', 'OWN', 'RENT', 'OTHER')
    li = ('DEBT CONSOLIDATION', 'EDUCATION', 'HOME IMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE')
    lg = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    hd = ('N', 'Y')
    
    left, user_input, right = st.columns([2, 20, 2])
        
    with user_input:
        # To get users input
        income = st.number_input('Annual Income', value = 38000)
        home_ownership = st.selectbox('Home Ownership', pho)
        employment_length = st.slider('Employment Length (In Years)', 0, 50, value = 8)
        loan_intent = st.selectbox('Loan Intent', li)
        loan_grade = st.selectbox("Loan Grade - based on the borrower's credit profile (quality of the collateral etc). 'A' grade represent the lowest risk whereas 'G' grade is the riskiest", lg)
        loan_amount = st.number_input('Loan Amount', value = 88888)
        loan_int_rate = st.number_input('Loan Interest Rate', value = 8.8)
        historical_default = st.selectbox('Historical Default', hd)
        credit_history_length = st.slider("Credit History Length - the age of the accounts that appears in the borrower's credit report (active credit card(s) or loan(s))", 1, 30, value = 8)
    
    
    # Assigning binary values to One Hot Encoded values
    # Person Home Ownership
    if (home_ownership == 'MORTGAGE'):
        ho_MOR = 1
        ho_OWN = 0
        ho_OTH = 0
    elif (home_ownership == 'OWN'):
        ho_MOR = 0
        ho_OWN = 1
        ho_OTH = 0
    elif (home_ownership == 'OTHER'):
        ho_MOR = 0
        ho_OWN = 0
        ho_OTH = 1
    else:
        ho_MOR = 0
        ho_OWN = 0
        ho_OTH = 0       
    
    # Loan Intent
    if (loan_intent == 'DEBT CONSOLIDATION'):
        li_DEB = 1
        li_EDU = 0
        li_HIM = 0
        li_MED = 0
        li_PER = 0
        li_VEN = 0
    elif (loan_intent == 'EDUCATION'):
        li_DEB = 0
        li_EDU = 1
        li_HIM = 0
        li_MED = 0
        li_PER = 0
        li_VEN = 0
    elif (loan_intent == 'HOME IMPROVEMENT'):
        li_DEB = 0
        li_EDU = 0
        li_HIM = 1
        li_MED = 0
        li_PER = 0
        li_VEN = 0
    elif (loan_intent == 'MEDICAL'):
        li_DEB = 0
        li_EDU = 0
        li_HIM = 0
        li_MED = 1
        li_PER = 0
        li_VEN = 0  
    elif (loan_intent == 'PERSONAL'):
        li_DEB = 0
        li_EDU = 0
        li_HIM = 0
        li_MED = 0
        li_PER = 1
        li_VEN = 0
    else:
        li_DEB = 0
        li_EDU = 0
        li_HIM = 0
        li_MED = 0
        li_PER = 0
        li_VEN = 1
        
    # Loan Grade
    if (loan_grade == 'A'):
        lg_B = 0
        lg_C = 0
        lg_D = 0
        lg_E = 0
        lg_F = 0 
        lg_G = 0
    elif (loan_grade == 'B'):
        lg_B = 1
        lg_C = 0
        lg_D = 0
        lg_E = 0
        lg_F = 0 
        lg_G = 0
    elif (loan_grade == 'C'):
        lg_B = 0
        lg_C = 1
        lg_D = 0
        lg_E = 0
        lg_F = 0 
        lg_G = 0
    elif (loan_grade == 'D'):
        lg_B = 0
        lg_C = 0
        lg_D = 1
        lg_E = 0
        lg_F = 0 
        lg_G = 0
    elif (loan_grade == 'E'):
        lg_B = 0
        lg_C = 0
        lg_D = 0
        lg_E = 1
        lg_F = 0 
        lg_G = 0
    elif (loan_grade == 'F'):
        lg_B = 0
        lg_C = 0
        lg_D = 0
        lg_E = 0
        lg_F = 1 
        lg_G = 0
    elif (loan_grade == 'G'):
        lg_B = 0
        lg_C = 0
        lg_D = 0
        lg_E = 0
        lg_F = 0 
        lg_G = 1
        
    
    # Create DataFrame
    data = {'income': [income], 
            'employment_length': [employment_length],
            'loan_amount': [loan_amount],
            'loan_interest_rate': [loan_int_rate],
            'historical_default': [historical_default],
            'credit_history_length': [credit_history_length],
            'home_ownership_MORTGAGE': [ho_MOR], 
            'home_ownership_OTHER': [ho_OTH],
            'home_ownership_OWN': [ho_OWN],
            'intent_DEBT_CONSOLIDATION': [li_DEB],
            'intent_EDUCATION': [li_EDU],
            'intent_HOME_IMPROVEMENT': [li_HIM], 
            'intent_MEDICAL': [li_MED],
            'intent_PERSONAL': [li_PER], 
            'intent_VENTURE':[li_VEN],
            'loan_grade_B': [lg_B],
            'loan_grade_C': [lg_C],
            'loan_grade_D': [lg_D],
            'loan_grade_E': [lg_E],
            'loan_grade_F': [lg_F], 
            'loan_grade_G': [lg_G]}
    
    data = pd.DataFrame(data) # Create DataFrame
    
    # Data Pre-processing/Transformation
    data['historical_default'] = label_encoder.transform(data['historical_default'])
    data[['income', 
          'employment_length', 
          'loan_amount', 
          'loan_interest_rate', 
          'credit_history_length']] = pt_yeo_johnson.transform(data[['income', 
                                                                     'employment_length', 
                                                                     'loan_amount', 
                                                                     'loan_interest_rate', 
                                                                     'credit_history_length']])
    
    left, predict, right = st.columns([2, 20, 2])
    
    with predict:
        # Predict button
        predict = st.button('Predict')
    
        # Action if predict button is clicked
        if predict:
            with st.spinner('Predicting...'):
            
                prediction = classifier.predict(data.iloc[[0]])
                labels = ['Non-Default', 'Default']
                # LIME instance explanation 
                interpretor = lime_tabular.LimeTabularExplainer(training_data = np.array(x_train_smote), 
                                                                feature_names = data.columns, 
                                                                class_names = labels, 
                                                                mode = 'classification')
                exp = interpretor.explain_instance(data_row = data.iloc[0], predict_fn = classifier.predict_proba)
                exp.show_in_notebook(show_table = True)
        
            # Show result based on the prediction outcome
            if (prediction == 1):
                st.error('Customer **will default on their loan**:rage:') # Default Loan
                st.write("*LIME Instance Explanation:*")        
                components.html(exp.as_html(), height = 800)
            else:
                st.success('Customer **will meet their loan obligation**:smiley:') # Non-Default Loan
                st.write("*LIME Instance Explanation:*")        
                components.html(exp.as_html(), height = 800)
            
        # Button to show global explanation        
        show_global_explanation = st.checkbox('Show SHAP Global Explanation')
    
        # SHAP XAI - global explanation 
        explainer = shap.TreeExplainer(classifier)
        shap_values = explainer.shap_values(x_train_smote)
        st.set_option('deprecation.showPyplotGlobalUse', False)

    
        # Action to show global explanation if the checkbox is checked 
        if show_global_explanation:
            with st.spinner('Showing SHAP...'):
                # show SHAP global explanation distribution
                st.warning('Red colour indicates higher value of a feature, whereas Blue colour indicates lower value of a feature')
                shap_global_explanation = shap.summary_plot(shap_values, x_train_smote)
                return st.pyplot(shap_global_explanation)
        
