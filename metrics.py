import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('csv/leagues/Serie-A-Stats/2022-2023/league_table_overall.csv')

ATTACK = colored('attack', attrs=['bold'])
DEFENCE = colored('defence', attrs=['bold'])
UNDERPERFORMANCE = colored('underperformance', 'red', attrs=['bold'])
OVERPERFORMANCE = colored('overperformance', 'green', attrs=['bold'])

def xGGF(df):
    df['GF/xG'] = df['GF'] / df['xG']
    df['GF-xG'] = df['GF'] - df['xG']
    df = df[['Squad', 'GF/xG', 'GF-xG']]
    df = df.sort_values('GF-xG')
    print('[!] GF-xG: difference between scored goals and exp. scored goals\n[!] GF/xG < 1: {atk} {up}\n[!] GF/xG > 1: {atk} {op}\n[!] Sort by: best underperformance\n[!] Zero values excluded'.format(
        atk = ATTACK,
        up = UNDERPERFORMANCE,
        op = OVERPERFORMANCE)
    )
    print(df[df['GF/xG'] != 0])
    mask1 = df['GF-xG'] < 0
    mask2 = df['GF-xG'] >= 0
    fig, axs = plt.subplots(2)
    axs[0].title.set_text('GF-xG')
    axs[0].bar(df['Squad'][mask1], df['GF-xG'][mask1], color='red')
    axs[0].bar(df['Squad'][mask2], df['GF-xG'][mask2], color='green')
    df = df.sort_values('GF/xG')
    axs[1].title.set_text('GF/xG')
    axs[1].plot(df['Squad'], df['GF/xG'], marker = 'o')
    plt.show()

def xGAGA(df):
    df['GA/xGA'] = df['GA'] / df['xGA']
    df['GA-xGA'] = df['GA'] - df['xGA']
    df = df[['Squad', 'GA/xGA', 'GA-xGA']]
    df = df.sort_values('GA-xGA')
    print('[!] GA-xA: difference between allowed goals and exp. allowed goals\n[!] GA/xGA < 1: {d} {op}\n[!] GA/xGA > 1: {d} {up}\n[!] Sort by: best overperformance\n[!] Zero values excluded'.format(
        d = DEFENCE,
        up = UNDERPERFORMANCE,
        op = OVERPERFORMANCE)
    )
    print(df[df['GA/xGA'] != 0])
    mask1 = df['GA-xGA'] < 0
    mask2 = df['GA-xGA'] >= 0
    fig, axs = plt.subplots(2)
    axs[0].bar(df['Squad'][mask1], df['GA-xGA'][mask1], color='green')
    axs[0].bar(df['Squad'][mask2], df['GA-xGA'][mask2], color='red')
    df = df.sort_values('GA/xGA')
    axs[1].plot(df['Squad'], df['GA/xGA'], marker = 'o')
    plt.show()

def L5Pts(df):
    try:
        df['L5Pts'] = [df['Last 5'][id].split(' ').count('W') * 3 + df['Last 5'][id].split(' ').count('D') for id in range(len(df))]
        print(df[['Squad', 'L5Pts']])
    except(KeyError):
        print('No last 5 matches available')

def PtsL5(df):
    try:
        df['Pts/L5'] = df['L5Pts'] / 5
        print(df[['Squad', 'Pts/L5']])
    except(KeyError):
        print('No last 5 matches available')


xGGF(df)
#xGAGA(df)
#L5Pts(df)
#PtsL5(df)