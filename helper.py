import numpy as np

def find_party(df):
    party = df['PARTY'].unique().tolist()
    party.sort()
    return party
def find_degree(df):
    degree = df['EDUCATION'].unique().tolist()
    degree.sort()
    return degree
def find_state(df):
    state = df['STATE'].unique().tolist()
    state.sort()
    return state
def find_constit(df):
    constit = df['CONSTITUENCY'].unique().tolist()
    constit.sort()
    return constit
def find_member(df):
    members = df['NAME'].unique().tolist()
    members.sort()
    return members

