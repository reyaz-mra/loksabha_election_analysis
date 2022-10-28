import numpy as np
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.figure_factory as ff

import helper

df = pd.read_csv('election.csv')
df.rename(columns = {'CRIMINAL\nCASES': 'CRIMINAL CASES'}, inplace=True)
symbol = pd.read_csv('symbol.csv')
symbol.rename(columns = {'SYMBOL':'IMAGE'}, inplace=True)
new_df = df.merge(symbol, on='PARTY', how='left')

st.sidebar.title("Lok Sabha Election 2019 Analysis")
st.sidebar.image("https://img.freepik.com/free-vector/indian-loksabha-election-design_1017-17777.jpg?w=740&t=st=1666697703~exp=1666698303~hmac=122b1a70e71c8321dd170330ffe557669f60aa8f3d72d09604c828e944f86a45")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overall Analysis', 'Partywise Analysis', 'Statewise Analysis', 'Candidates')
)

if user_menu == 'Overall Analysis':
    st.title("Lok Sabha 2019 Election Result")
    winner_df = df[df['WINNER'] == 1]
    winner_df.groupby('PARTY').sum()
    sort_winner = winner_df.groupby('PARTY').sum().sort_values('WINNER', ascending=False).reset_index()
    winner_df = sort_winner[['PARTY', 'WINNER']]
    winner_df.rename(columns={'WINNER': 'SEATS'}, inplace=True)
    st.table(winner_df)

    st.title("Seat shares of all Parties ")
    fig = px.pie(winner_df, values='SEATS', names='PARTY', width=1000, height=1000)
    st.plotly_chart(fig)

    st.title("Bar chart of Seats for All Parties")
    fig = px.bar(winner_df, x="PARTY", y="SEATS", width=800, height=700)
    st.plotly_chart(fig)


    st.title("Categories of all canditaes of 2019 Lok Sabha")
    categ = df['CATEGORY'].value_counts().reset_index()
    categ.rename(columns={'index': 'CATEGORY', 'CATEGORY': 'No. of Candidates'}, inplace=True)
    fig = px.pie(categ, values='No. of Candidates', names='CATEGORY', width=800, height=700)
    st.plotly_chart(fig)

    st.title("Gender Ratio of all candidates of 2019 Lok Sabha Election")
    gender = df['GENDER'].value_counts().reset_index()
    gender.rename(columns={'index': 'GENDER', 'GENDER': 'COUNTS'}, inplace=True)
    fig = px.pie(gender, values='COUNTS', names='GENDER', width=700, height=700)
    st.plotly_chart(fig)



if user_menu == 'Partywise Analysis':
    st.sidebar.header("Party List")
    winner_df = df[df['WINNER'] == 1]
    party = helper.find_party(winner_df)
    selected_party = st.sidebar.selectbox("Select Party",party)
    total_member = df[df['PARTY'] == selected_party]
    #Candidates
    candidates = total_member.shape[0]
    #winner members
    find_win = df[df['PARTY'] == selected_party]
    total_win = find_win[find_win['WINNER'] == 1]
    winner_member = total_win.shape[0]
    #winning percent
    win_per = 100 * winner_member/ total_member.shape[0]
    percentage = format(win_per, '.2f') + '%'

    #PARTY IMAGE
    party = new_df['PARTY'] == selected_party
    image_for = new_df[party].iloc[0]['IMAGE']


    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.header("Party Name")
        st.title(selected_party)
    with col2:
        st.header("Party Symbol")
        st.image(image_for,width=200)
    with col3:
        st.header("Most Seats from")
        party = new_df['PARTY'] == selected_party
        party_df = new_df[party]
        party_state = party_df[party_df['WINNER'] == 1]
        most_seats = party_state['STATE'].value_counts().reset_index()
        most_seats.rename(columns={'index': 'STATE', 'STATE': 'SEATS'}, inplace=True)
        st.title(most_seats.iloc[0][0])

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.header("Total Candidates")
        st.title(candidates)
    with col2:
        st.header("Total Winner Candidates")
        st.title(winner_member)
    with col3:
        st.header("Win Percentage")
        st.title(percentage)



    st.title("No of seats won in different States")
    st.table(most_seats)


    st.title("Education of "+selected_party+" Candidates")
    party = new_df['PARTY'] == selected_party
    party_df = new_df[party]
    qualification = party_df['EDUCATION'].value_counts().reset_index()
    qualification.rename(columns={'index': 'DEGREE', 'EDUCATION': 'TOTAL MEMBERS'}, inplace=True)
    fig = px.pie(qualification, values='TOTAL MEMBERS', names='DEGREE', width=800, height=800)
    st.plotly_chart(fig)


    st.title("List of Candidates as per their Degree")
    education = helper.find_degree(party_df)
    selected_edu = st.selectbox("Choose any Option",education)

    candidates_df = party_df[party_df['EDUCATION'] == selected_edu]
    candidate_table = candidates_df[['NAME', 'GENDER', 'AGE', 'ASSETS', 'WINNER', 'STATE']]
    convert_dict = {'AGE': int}
    candidate_table = candidate_table.astype(convert_dict)
    st.table(candidate_table)

    st.title("Gender Ratio of "+ selected_party)
    gen_df = df[df['PARTY'] == selected_party]
    gender = gen_df['GENDER'].value_counts().reset_index()
    gender.rename(columns={'index': 'GENDER', 'GENDER': 'COUNTS'}, inplace=True)
    fig = px.pie(gender, values='COUNTS', names='GENDER', width=700, height=700)
    st.plotly_chart(fig)


if user_menu == 'Statewise Analysis':
    st.sidebar.header("States List")
    state_df = helper.find_state(new_df)
    selected_state = st.sidebar.selectbox("Choose an State", state_df)
    col1, col2 = st.columns(2,gap='large')
    with col1:
        st.header("State")
        st.title(selected_state)
    with col2:
        st.header("Total Parties")
        state_p = df[df['STATE'] == selected_state]
        state_p = state_p[state_p.PARTY != 'NOTA']
        total_p = state_p['PARTY'].unique().shape[0]
        st.title(total_p)

    col1, col2 = st.columns(2,gap='large')
    with col1:
        st.header("Total Lok Sabha Seats")
        st.title(state_p['CONSTITUENCY'].unique().shape[0])
    with col2:
        st.header("Most seats won by")
        state_p = new_df[new_df['STATE'] == selected_state]
        state_p = state_p[state_p.PARTY != 'NOTA']
        state_total = state_p[state_p['WINNER'] == 1]
        most_seat = state_total['PARTY'].value_counts().reset_index()
        st.title(most_seat.iloc[0][0])


    st.title("Seats won by different parties in "+ selected_state)

    most_seat.rename(columns={'index': 'PARTY', 'PARTY': 'SEATS'}, inplace=True)
    st.table(most_seat)


    st.title("Know about all political Parties of "+ selected_state)
    state_p = df[df['STATE'] == selected_state]
    state_p = state_p[state_p.PARTY != 'NOTA']
    all_parties = helper.find_party(state_p)
    selected_state_party = st.selectbox("Choose any Option",all_parties)
    one_party = state_p[state_p['PARTY']== selected_state_party]
    st.header("All Candidate detail of "+selected_state_party+ " in "+selected_state)
    convert_dict = {'AGE': int}
    one_party = one_party.astype(convert_dict)
    one_party_detail = one_party[['CONSTITUENCY','NAME','WINNER','GENDER','AGE','EDUCATION','ASSETS']]
    st.table(one_party_detail)



if user_menu == 'Candidates':
    state_list = helper.find_state(new_df)
    select_state = st.selectbox("Choose State", state_list)
    state_data = new_df[new_df['STATE']==select_state]

    constituency_list = helper.find_constit(state_data)
    select_constit = st.selectbox("Choose Constituency",constituency_list)
    constit_data = state_data[state_data['CONSTITUENCY'] == select_constit]

    member_list = helper.find_member(constit_data)
    select_member = st.selectbox("Choose Candidate", member_list)
    member_data = constit_data[constit_data['NAME'] == select_member]

    try:
        st.image(member_data['IMAGE'].iloc[0], width=250, caption="Party Symbol")
    except:
        print("")

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.header("Name")
        st.title(member_data['NAME'].iloc[0])
    with col2:
        st.header("Party")
        st.title(member_data['PARTY'].iloc[0])
    with col3:
        st.header("Gender")
        st.title(member_data['GENDER'].iloc[0])

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.header("Age")
        st.title(int(member_data['AGE'].iloc[0]))
    with col2:
        st.header("Qualification")
        st.title(member_data['EDUCATION'].iloc[0])
    with col3:
        st.header("Assets")
        st.title(member_data['ASSETS'].iloc[0])

    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.header("Total Electors")
        st.title(member_data['TOTAL ELECTORS'].iloc[0])
    with col2:
        st.header("Total Votes")
        st.title(member_data.iloc[:, [15]].iloc[0].iloc[0])
    with col3:
        st.header("Vote Percentage")
        perc = member_data.iloc[:, [16]].iloc[0].iloc[0]
        percent = format(perc, '.2f') + '%'
        st.title(percent)
    
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.header("Criminal Cases")
        st.title(member_data.iloc[:, [7]].iloc[0].iloc[0])
    with col2:
        st.header("Result")
        num = member_data['WINNER'].iloc[0]
        if num == 1:
            st.title("Won")
        else:
            st.title("Lost")






















