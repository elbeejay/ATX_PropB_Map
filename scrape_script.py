"""Script to scrape Prop B for votes from the PDF of results."""
import numpy as np
import pandas as pd
import tabula
import matplotlib.pyplot as plt

# scrape the PDF into a pandas DataFrame with tabula
df = tabula.read_pdf('/home/jayh/Documents/gmt_tuts/austin_propb/L21_Final_Precinct_Summary_r.pdf',
                     pages='all', stream=True, lattice=False, guess=False)

# identify precincts and vote% for/against prop B
# store values in lists
precincts = []
vote_for = []
vote_against = []
for i in range(len(df)):
    # try to identify start index for prop B data
    # also identify start index for Prop C data (end of Prop B)
    Bmask = df[i]['May 1, 2021 General & Special Election'].str.contains('City of Austin Proposition B')
    Cmask = df[i]['May 1, 2021 General & Special Election'].str.contains('City of Austin Proposition C')
    # check if on this page, otherwise skip processing
    if (np.any(Bmask == True) == True) and (np.any(Cmask == True) == True):
        # give it a try but know there are exceptions
        try:
            # replace NaNs with False in masks
            Bmask = Bmask.replace(np.nan, False)
            Cmask = Cmask.replace(np.nan, False)
            # identify indices
            indB = df[i][Bmask].index[0]
            indC = df[i][Cmask].index[0]
            # pick out clipped dataframe from the big one
            # just containing Prop B data
            clipped = df[i].loc[indB:indC]
            # define mask based on expecting a % sign
            # note: assumes consistency between pages
            mask = clipped['May 1, 2021 General & Special Election'].str.contains('%')
            mask = mask.replace(np.nan, False)
            # identify indices for the for and against vote data
            for_vote_idx = clipped[mask].index[1]
            against_vote_idx = clipped[mask].index[2]
            # make floats
            _for_val = float(clipped.loc[for_vote_idx][0].split(' ')[-1][:-1])
            _against_val = float(clipped.loc[against_vote_idx][0].split(' ')[-1][:-1])
            # identify precinct id
            _precinct_id = df[i].loc[1][0][:3]

            # if we get this far without exception, append values to the lists
            precincts.append(_precinct_id)
            vote_for.append(_for_val)
            vote_against.append(_against_val)
        # exception passing
        except Exception:
            pass

# generate a stacked bar plot of vote split in each precinct
fig, ax = plt.subplots(dpi=300, figsize=(35, 3), facecolor='w')
width = 0.8
ax.bar(precincts, vote_for, width, label='For',
       facecolor=(100/255, 100/255, 200/255))
ax.bar(precincts, vote_against, width, label='Against', bottom=vote_for,
       facecolor=(200/255, 100/255, 100/255))
plt.plot(np.linspace(-1, 194), np.linspace(-1, 194)/np.linspace(-1, 194)*50,
         c='k', linestyle='--', linewidth=3, zorder=5,
         label='50:50')
plt.legend(title='Prop. B', loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=90)
plt.ylabel('Vote %')
plt.xlabel('Precinct ID')
plt.title('Austin May 2021 - Prop. B Results by Precinct')
ax.set_xmargin(0)
ax.autoscale()
plt.savefig('BarChartResults.png', bbox_inches='tight')
plt.close()

# convert lists into dataframe
df = pd.DataFrame(np.array([precincts, vote_for, vote_against]).T,
                  columns=['Precinct', 'For', 'Against'])
# save dataframe as csv
df.to_csv('ScrapedResults_PropB_perPrecinct.csv')
