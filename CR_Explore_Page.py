# Modules Imported
import streamlit as st
import pandas as pd
import plotly.express as px


# Loading Dataset
@st.cache(allow_output_mutation = True)
def load_dataset():
    df = pd.read_excel('data_WA.xlsx')
    return(df)  

def show_explore_page():
    st.markdown('--------------------------')
    df = load_dataset()     
    
    # Make Filtering Selection for Users
    # Person Age
    person_age = df['person_age'].unique().tolist()
    person_age_selection = st.sidebar.slider('Person Age', 
                                             min_value = min(person_age), 
                                             max_value = max(person_age), 
                                             value = (min(person_age), 
                                                      max(person_age)))
    
    # Income
    income = df['person_income'].unique().tolist()
    person_income_selection = st.sidebar.slider('Annual Income', 
                                                min_value = min(income), 
                                                max_value = max(income), 
                                                value = (min(income), 
                                                         max(income)))
   
    # Employment Length
    employment_length = df['person_emp_length'].unique().tolist()
    person_emp_length_selection = st.sidebar.slider('Employment Length', 
                                                    min_value = min(employment_length), 
                                                    max_value = max(employment_length), 
                                                    value = (min(employment_length), 
                                                             max(employment_length)))
    
    # Loan Amount
    loan_amount = df['loan_amnt'].unique().tolist()
    loan_amount_selection = st.sidebar.slider('Loan Amount', 
                                              min_value = min(loan_amount), 
                                              max_value = max(loan_amount), 
                                              value = (min(loan_amount), 
                                                       max(loan_amount)))
    
    # Loan Interest Rate
    loan_interest_rate = df['loan_int_rate'].unique().tolist()
    loan_interest_rate_selection = st.sidebar.slider('Loan Interest Rate', 
                                                     min_value = min(loan_interest_rate), 
                                                     max_value = max(loan_interest_rate), 
                                                     value = (min(loan_interest_rate), 
                                                              max(loan_interest_rate)))
    
    # Credit History Length
    credit_history_length = df['cb_person_cred_hist_length'].unique().tolist()
    credit_history_length_selection = st.sidebar.slider('Credit History Length', 
                                                        min_value = min(credit_history_length), 
                                                        max_value = max(credit_history_length), 
                                                        value = (min(credit_history_length), 
                                                                 max(credit_history_length)))
    
    # Loan Intent
    loan_intent = df['loan_intent'].unique().tolist()
    loan_intent_selection = st.sidebar.multiselect('Loan Intent', 
                                                   loan_intent, 
                                                   default = loan_intent)
    
    # Home Ownership
    person_home_ownership = df['person_home_ownership'].unique().tolist()
    person_home_ownership_selection = st.sidebar.multiselect('Home Ownership', 
                                                             person_home_ownership, 
                                                             default = person_home_ownership)
    
    # Loan Grade
    loan_grade = df['loan_grade'].unique().tolist()
    loan_grade_selection = st.sidebar.multiselect('Loan Grade', 
                                                  loan_grade, 
                                                  default = loan_grade)
   
    # Loan Status
    loan_status = df['loan_status'].unique().tolist()
    loan_status_selection = st.sidebar.multiselect('Loan Status', 
                                                   loan_status, 
                                                   default = loan_status)    
     
    # Historical Default
    historical_default = df['cb_person_default_on_file'].unique().tolist()
    historical_default_selection = st.sidebar.multiselect('Historical Default', 
                                                          historical_default, 
                                                          default = historical_default)
    
    
    # Filter dataframe based on selection 
    filter = ((df['person_age'].between(*person_age_selection)) 
            & (df['person_income'].between(*person_income_selection))
            & (df['person_emp_length'].between(*person_emp_length_selection))
            & (df['loan_intent'].isin(loan_intent_selection))
            & (df['person_home_ownership'].isin(person_home_ownership_selection))
            & (df['loan_grade'].isin(loan_grade_selection))
            & (df['loan_amnt'].between(*loan_amount_selection))
            & (df['loan_int_rate'].between(*loan_interest_rate_selection))
            & (df['loan_status'].isin(loan_status_selection))
            & (df['cb_person_default_on_file'].isin(historical_default_selection))
            & (df['cb_person_cred_hist_length'].between(*credit_history_length_selection)))
       
    # Print Number of records
    number_of_records = df[filter].shape[0]
    st.warning(f'Number of records: {number_of_records:,}')

    # KPI's
    total_loans_issued = df[filter][['loan_amnt']]
    avg_loans_int_rate = df[filter][['loan_int_rate']]
    median_income = df[filter][['person_income']]

    total_loans_issued = int(total_loans_issued.sum())
    avg_loans_int_rate = float(avg_loans_int_rate.mean())
    median_income = float(median_income.median())
    
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.info(f'Total Loans Issued:  \n$ {total_loans_issued:,}')
    with middle_column:
        st.info(f'Average Interest Rate:  \n {avg_loans_int_rate:.2f}')
    with right_column: 
        st.info(f'Median Annual Income:  \n$ {median_income:,.0f}')
        
    bar, scatter = st.columns(2)
         
    # Bar Chart Option 
    bar_option = bar.selectbox('Choose a variable', ('loan_intent', 
                                                        'person_home_ownership', 
                                                        'loan_grade', 
                                                        'cb_person_default_on_file'))
    bar.markdown('')

    # Make Bar Chart
    groupby_li = df[filter].groupby(by = [bar_option]).count()[['person_age']]
    groupby_li = groupby_li.rename(columns = {'person_age': 'counts'})
    groupby_li = groupby_li.reset_index()
    
    @st.cache(max_entries = 10, ttl = 3600)
    def make_fig1():
        fig = px.bar(groupby_li, x = bar_option, y = 'counts', width = 640)
        fig.update_layout(title_text = f'<b>Bar Chart of {bar_option}</b>', title_x = 0.5)
        return fig
    
    # Show Bar chart
    bar.plotly_chart(make_fig1(), use_container_width = True)
    
    # Scatter Plot Selection
    scatter_y = scatter.selectbox('Y-Axis', ('person_income', 
                                            'person_age', 
                                            'person_emp_length', 
                                            'loan_amnt', 
                                            'loan_int_rate', 
                                            'cb_person_cred_hist_length', 
                                            'loan_percent_income'))
    scatter_x = scatter.selectbox('X-Axis', ('person_age', 
                                            'person_income', 
                                            'person_emp_length', 
                                            'loan_amnt', 
                                            'loan_int_rate', 
                                            'cb_person_cred_hist_length', 
                                            'loan_percent_income'))
    
   # Make Scatter Plot
    @st.cache(max_entries = 10, ttl = 3600)
    def make_fig2():
        fig2 = px.scatter(df[filter], x = scatter_x, y = scatter_y, width = 660)
        fig2.update_layout(title_text = f'<b>Scatter Plot of {scatter_y} against {scatter_x}</b>', title_x = 0.5)
        return fig2
    
    # Show Scatter Plot
    scatter.plotly_chart(make_fig2(), use_container_width = True)
    
    st.markdown('--------------------------')
    
    cm, pie = st.columns([20, 15])
    
    # Pie Chart Selection
    pie_option = pie.selectbox('Choose a variable', ('loan_status', 'cb_person_default_on_file'))
    
    # Make Pie Chart
    groupby_ls = df[filter].groupby(by = [pie_option]).count()[['person_age']]
    groupby_ls = groupby_ls.rename(columns = {'person_age': 'counts'})
    groupby_ls = groupby_ls.reset_index()
    
    @st.cache(max_entries = 10, ttl = 3600)
    def make_fig4():
        fig4 = px.pie(groupby_ls, values = 'counts', names = pie_option, width = 500)
        fig4.update_layout(title_text = f'<b>Pie Chart of {pie_option}</b>', title_x = 0.5)
        return fig4    
    
    # Show Pie chart of loan status
    pie.plotly_chart(make_fig4(), use_container_width = True)
    
    
    # Correlation Matrix Selection
    corr_mat_option = cm.multiselect('Variables', 
                                         ('person_age', 
                                          'person_income', 
                                          'person_emp_length', 
                                          'loan_amnt', 
                                          'loan_int_rate', 
                                          'loan_status', 
                                          'loan_percent_income', 
                                          'cb_person_cred_hist_length'), 
                                         default = ('person_age', 
                                                    'person_income', 
                                                    'person_emp_length', 
                                                    'loan_amnt', 
                                                    'loan_int_rate', 
                                                    'loan_status', 
                                                    'loan_percent_income', 
                                                    'cb_person_cred_hist_length'))
    # Create a dummy DataFrame for correlation matrix
    new_df = df[corr_mat_option]
    
    # Make Correlation Matrix
    @st.cache(max_entries = 10, ttl = 3600)
    def make_fig5():
        fig5 = px.imshow(new_df[filter].corr().round(2), text_auto = True)
        fig5.update_layout(title_text = '<b>Correlation Matrix</b>', title_x = 0.5)
        fig5.update_xaxes(tickangle = 90)
        fig5.layout.height = 600
        return fig5
    
    # Show Correlation Matrix
    cm.plotly_chart(make_fig5(), use_container_width = True) 
    
    st.markdown('--------------------------')  
    
    left, mid, right = st.columns([10, 50, 10])
    
    # Make Parallel Category Diagram of Loan Intent, Home Ownership, Loan Grade and Historical Default
    @st.cache(max_entries = 10, ttl = 3600)
    def make_fig3():
        fig3 = px.parallel_categories(df[filter], color_continuous_scale= px.colors.sequential.RdBu, 
                                          color = 'loan_status',
                                          dimensions = ['loan_intent', 
                                                        'person_home_ownership', 
                                                        'loan_grade', 
                                                        'cb_person_default_on_file'],
                                          labels = {col:col.replace('_', ' ') for col in df[filter].columns})
        fig3.update_layout(title_text = '<b>Parallel Category Diagram</b>', title_x = 0.5)
        return fig3  
    
    # Show Parallel Category Diagram
    mid.plotly_chart(make_fig3(),  use_container_width = True)
        
        
