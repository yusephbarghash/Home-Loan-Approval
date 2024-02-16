
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import sklearn

model  = joblib.load('model.pkl')
Inputs = joblib.load('inputs.pkl')


def Prediction(Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome,
               CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area):
    
    df = pd.DataFrame(columns= ['Gender', 'Married', 'Dependents', 'Education',
           'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
           'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Income', 'Monthly_Loan',
           'Net_Income', 'log_Income', 'log_Monthly_Loan', 'log_Net_Income'])
    
    df.at[0,"Gender"]= Gender
    df.at[0,"Married"]= Married
    df.at[0,"Dependents"]= Dependents
    df.at[0,"Education"]= Education
    df.at[0,"Self_Employed"]= Self_Employed
    df.at[0,"ApplicantIncome"]= ApplicantIncome
    df.at[0,"CoapplicantIncome"]= CoapplicantIncome
    df.at[0,"LoanAmount"]= LoanAmount
    df.at[0,"Loan_Amount_Term"]= Loan_Amount_Term
    df.at[0,"Credit_History"]= Credit_History
    df.at[0,"Property_Area"]= Property_Area

    df.at[0,"Income"]= df.at[0, 'ApplicantIncome'] + df.at[0, 'CoapplicantIncome']
    df.at[0,"Monthly_Loan"]= (df.at[0, 'LoanAmount'] * 1000 ) / df.at[0, 'Loan_Amount_Term']
    df.at[0,"Net_Income"]= df.at[0, 'ApplicantIncome'] - df.at[0, 'Monthly_Loan']
    df.at[0,"log_Income"] = np.log(df.at[0, 'Income'])
    df.at[0,"log_Monthly_Loan"]= np.log(df.at[0, 'Monthly_Loan'])
    df.at[0,"log_Net_Income"]= np.log(df.at[0, 'Net_Income'])
    
    cols_to_drop = [
        'ApplicantIncome', 
        'CoapplicantIncome', 
        'LoanAmount',
        'Loan_Amount_Term',
        'Income',
        'Monthly_Loan',
        'Net_Income'
    ]
    df.drop(cols_to_drop, axis=1, inplace=True)

    
    result = model.predict(df)
    return result[0]


def Main():
    
    Gender  = st.selectbox("Gender" , ['Male', 'Female'])
    Married = st.selectbox("Married" , ['No', 'Yes'])
    Dependents  = st.selectbox("Dependents" , ['0', '1', '2', '3+'])
    Education = st.selectbox("Education" , ['Graduate', 'Not Graduate'])
    Self_Employed  = st.selectbox("Self_Employed" , ['No', 'Yes'])
    ApplicantIncome = st.slider( "ApplicantIncome",min_value= 150 , max_value=90000 , step= 10 , value=5000)
    CoapplicantIncome = st.slider("CoapplicantIncome",min_value= 0 , max_value=45000 , step= 10 , value=1600)
    LoanAmount = st.slider("LoanAmount",min_value= 10 , max_value=700 , step= 1 , value=150)
    Loan_Amount_Term = st.slider("Loan_Amount_Term",min_value= 12 , max_value=480 , step= 1 , value=340)
    Credit_History = st.selectbox("Credit_History" , [0.0, 1.0])
    Property_Area  = st.selectbox("Property_Area" , ['Urban', 'Rural', 'Semiurban'])
    
    if st.button("Predict"):
        result = Prediction(Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome,
               CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area)
        if result == 0:
            st.error('Not Approved')
        elif result == 1:
            st.success('Approved')
    

Main()
