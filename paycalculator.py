import streamlit as st
import pandas as pd

st.image("DV_alone.png", caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
#st.subheader("presents...")

# Set the title and subtitle
st.title("Pay Award Calculator for Doctors and Dentists in training in England")
st.write("This calculator will give you an estimated pay award backpayment, it may not be 100% correct but will give you a chance to compare it to your payslip. If there are big discrepancies, you should raise it with your employer.")

# Create two columns
col1, col2 = st.columns(2)

#Setting Option Values

wknd_options = {
    '<1:8 -- 0%': 0.0,
    '<1:7 - 1:8 -- 3%': 3.0,
    '<1:6 - 1:7 -- 4%': 4.0,
    '<1:5 - 1:6 -- 5%' : 5.0,
    '<1:4 - 1:5 -- 6%': 6.0,
    '<1:3 - 1:4 -- 7.5%': 7.5,
    '<1:2 - 1:3 -- 10%': 10.0,
    '1:2 -- 15%': 15.0
}

nroc_options = {
    'Yes': 8,
    'No': 0
}

flex_options = {
    'Yes': 1000,
    'No': 0
}


grade_options1 = {
    'FY1': 29384,
    'FY2': 34012,
    'ST1': 40257,
    'ST2' : 40257,
    'ST3': 51017,
    'ST4': 51017,
    'ST5': 51017,
    'ST6': 58398,
    'ST7': 58398,
    'ST8': 58398,
}

grade_options2 = {
    'FY1': 32398,
    'FY2': 37303,
    'ST1': 43923,
    'ST2' : 43923,
    'ST3': 55329,
    'ST4': 55329,
    'ST5': 55329,
    'ST6': 63152,
    'ST7': 63152,
    'ST8': 63152,
}

# Column 1: Data Entry
with col1:
    st.header("April-July WS")
    # Data entry variables for column 1
    data0 = st.selectbox("Select your grade.", list(grade_options1.keys()), key="grade1")
    data0_index = list(grade_options1.keys()).index(data0)  # Get the index of the selected grade
    ltft = st.number_input("Proportion Full Time in %", min_value=0.0, max_value=100.0, value=100.0, step = 10.0, key="ltft1") / 100.0
    data1_key = f"Apr1_{ltft}"  
    data1 = st.number_input("Basic Pay (as per grade)", value=grade_options1[data0] * ltft, step = 1000.0, key="data1_key")*ltft
    data2 = st.number_input("Additional pay above 40 hours (Found on WS, in hours)", value=7.5, step = 0.1, key="Apr2", min_value=0.0, max_value=100.0)
    data3 = st.selectbox("Non-Resident on Call?", nroc_options, key="Apr3", index = 0)
    data4 = st.selectbox("Weekend allowance", wknd_options, key="Apr4", index = 3)
    data5 = st.number_input("Hours attracting 37% enhancement (in hours)", value=7.5, step = 0.1, key="Apr5", min_value=0.0, max_value=100.0)
    data6 = st.selectbox("Flexible Pay Premia?", flex_options, key="Apr6", index=1)

    data2_calc = (((data2)*((data1/52)/40))*52) #Calculates Additional Pay
    data3_calc = (nroc_options[data3]/100)*data1 #Calculates NROC
    data4_calc = (wknd_options[data4]/100)*data1 #Calculates WKND
    data5_calc = ((data5)*((data1/52)/40)*0.37)*52
    data6_calc = (flex_options[data6])
    total_1 = data1 + data2_calc + data3_calc + data4_calc + data5_calc + data6_calc

    data1_waward = (data1*1.06)+(1250*ltft)
    data2_waward = (data2*((data1_waward/52)/40))*52
    data3_waward = (nroc_options[data3]/100)*data1_waward
    data4_waward = (wknd_options[data4]/100)*data1_waward
    data5_waward = (data5*((data1_waward/52)/40)*0.37)*52
    data6_waward = data6_calc*1.06

    data1_award = data1_waward - data1
    data2_award = data2_waward - data2_calc
    data3_award = data3_waward - data3_calc
    data4_award = data4_waward - data4_calc
    data5_award = data5_waward - data5_calc
    data6_award = data6_waward - data6_calc

    data1_awardmth = data1_award/12
    data2_awardmth = data2_award/12
    data3_awardmth = data3_award/12
    data4_awardmth = data4_award/12
    data5_awardmth = data5_award/12
    data6_awardmth = data6_award/12
    total_awardmth1 = data1_awardmth + data2_awardmth + data3_awardmth + data4_awardmth + data5_awardmth + data6_awardmth



     # Create a DataFrame for the summary table
    summary_data = {
        "Pay Category": ["Basic Pay", "Additional Pay", "NROC", "Weekend Allowance", "Enhancement Hours", "Flexible Pay", "Total"],
        "Value": [f"£ {data1}", f"£ {data2_calc:.2f}", f"£ {data3_calc:.2f}", f"£ {data4_calc:.2f}", f"£ {data5_calc:.2f}", f"£ {data6_calc:.2f}", f"£ {total_1:.2f}"]
    }
    summary_df = pd.DataFrame(summary_data).set_index('Pay Category', drop=True)

    # Display the summary table
    st.write("Summary for April-July WS:")
    st.write(summary_df, index=False)

# Column 2: Data Entry
with col2:
    st.header("August WS")
    
    data13 = st.selectbox("Select your grade.", list(grade_options1.keys()), key="grade2")
    data13_index = list(grade_options1.keys()).index(data13)  # Get the index of the selected grade
    # Data entry variables for column 2
    ltft2 = st.number_input("Proportion Full Time in %", min_value=0.0, max_value=100.0, value=100.0, step = 10.0, key="ltft2") / 100.0
    data7_key = f"Apr1_{ltft2}"  
    data7 = st.number_input("Basic Pay (as per grade)", value=grade_options1[data13] * ltft2, key="Aug1")
    data8 = st.number_input("Additional pay above 40 hours (Found on WS, in hours)", value=5.5, key="Aug2", min_value=0.0, max_value=100.0)
    data9 = st.selectbox("Non-Resident on Call?", nroc_options, key="Aug3", index=1)
    data10 = st.selectbox("Weekend allowance", wknd_options, key="Aug4", index = 4)
    data11 = st.number_input("Hours attracting 37% enhancement (in hours)", value=1.75, key="Aug5", min_value=0.0, max_value=100.0)
    data12 = st.selectbox("Flexible Pay Premia?", flex_options, key="Aug6", index=1)

    data8_calc = ((data8)*((data7/52)/40))*52 #Calculates Additional Pay
    data9_calc = (nroc_options[data9]/100)*data7 #Calculates NROC
    data10_calc = (wknd_options[data10]/100)*data7 #Calculates WKND
    data11_calc = ((data11)*((data7/52)/40)*0.37)*52
    data12_calc = (flex_options[data12])
    total_2 = data7 + data8_calc + data9_calc + data10_calc + data11_calc + data12_calc

    data7_waward = (data7*1.06)+(1250*ltft2)
    data8_waward = (data8*((data7_waward/52)/40))*52
    data9_waward = (nroc_options[data9]/100)*data7_waward
    data10_waward = (wknd_options[data10]/100)*data7_waward
    data11_waward = (data11*((data7_waward/52)/40)*0.37)*52
    data12_waward = data12_calc*1.06

    data7_award = data7_waward - data7
    data8_award = data8_waward - data8_calc
    data9_award = data9_waward - data9_calc
    data10_award = data10_waward - data10_calc
    data11_award = data11_waward - data11_calc
    data12_award = data12_waward - data12_calc

    data7_awardmth = data7_award /12
    data8_awardmth = data8_award /12
    data9_awardmth = data9_award /12
    data10_awardmth = data10_award /12
    data11_awardmth = data11_award /12
    data12_awardmth = data12_award /12
    total_awardmth2 = data7_awardmth + data8_awardmth + data9_awardmth + data10_awardmth + data11_awardmth + data12_awardmth
    total_pay_award = total_awardmth1*4 + total_awardmth2

    formatted_total_awardmth2 = f"{total_awardmth2:.2f}"
    formatted_total_awardmth1 = f"{total_awardmth1:.2f}"

    formatted_total_pay_award = f"£{total_pay_award:.2f}"


  # Create a DataFrame for the summary table
    summary_data = {
        "Pay Category": ["Basic Pay", "Additional Pay", "NROC", "Weekend Allowance", "Enhancement Hours", "Flexible Pay", "Total"],
        "Value": [f"£ {data7}", f"£ {data8_calc:.2f}", f"£ {data9_calc:.2f}", f"£ {data10_calc:.2f}", f"£ {data11_calc:.2f}", f"£ {data12_calc:.2f}", f"£ {total_2:.2f}"]
    }
    summary_df = pd.DataFrame(summary_data).set_index('Pay Category', drop=True)

    # Display the summary table
    st.write("Summary for August WS:")
    st.write(summary_df, index=False)

st.header("How many days did you strike for?")
dataApr = st.number_input("How many days in April?", value=0, step = 1, key="AprStrike", min_value=0, max_value=100)
dataJun = st.number_input("How many days in June?", value=0, step = 1, key="JunStrike", min_value=0, max_value=100)
dataJul = st.number_input("How many days in July?", value=0, step = 1, key="JulStrike", min_value=0, max_value=100)
dataAug = st.number_input("How many days in August?", value=0, step = 1, key="AugStrike", min_value=0, max_value=100)

strikeDeduction1 = ((total_awardmth1/30) * (dataApr + dataJun + dataJul))
strikeDeduction2 = ((total_awardmth2/30) * 0)


tot_strikeDeduction = -(strikeDeduction1 + strikeDeduction2)
pay_w_deduction = total_pay_award + tot_strikeDeduction

formatted_pay_w_deductions = f"£{pay_w_deduction:.2f}"
formatted_strike_deduction = f"{tot_strikeDeduction:.2f}"


st.header("Estimated Final Pay Award (pre-tax)")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Backpaid Pay Award", value=formatted_total_pay_award, delta=f"£ 4({formatted_total_awardmth1}) + {formatted_total_awardmth2}")
with col2:
    st.metric(label="Pay Award with Strike Deduction", value=formatted_pay_w_deductions, delta=formatted_strike_deduction) 

st.header("What should your payslip look like?")

Basic_Arrs = (data1_awardmth*4 + data7_awardmth) - strikeDeduction1
Addn_Arrs = data2_awardmth*4 + data8_awardmth
nroc_arrs = data3_awardmth*4 + data9_awardmth
Wknd_Arrs = data4_awardmth*4 + data10_awardmth
Night_Arrs = data5_awardmth*4 + data11_awardmth
total_arrs = Basic_Arrs + Addn_Arrs + Night_Arrs + Wknd_Arrs + nroc_arrs

st.write("Backpaid Pay Award Breakdown:")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Basic Pay Arrs", value=f"£ {Basic_Arrs:.2f}")
    st.metric(label="Addn Ros Hrs NP Arrs", value=f"£ {Addn_Arrs:.2f}",) 
    st.metric(label="Night Duty 37% Arrs", value=f"£ {Night_Arrs:.2f}") 
with col2:
    st.metric(label="Weekend Arrs", value=f"£ {Wknd_Arrs:.2f}") 
    st.metric(label="NROC Arrs", value=f"£ {nroc_arrs:.2f}") 