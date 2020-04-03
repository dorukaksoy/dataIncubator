# ---------------------------------------------------------------------------
# Author: Doruk Aksoy
# Date: 04/02/2020
# Data Incubator Application Challenge 2
# ---------------------------------------------------------------------------
import numpy as np
import pandas as pd

# Read in data from given files
data_2017 = pd.read_csv("PartD_Prescriber_PUF_NPI_17.txt",sep='\t')
data_2016 = pd.read_csv("PartD_Prescriber_PUF_NPI_16.txt",sep='\t')

# Question 1
"""
In 2017, what was the average number of beneficiaries per provider? 
Due to the suppression of data for those with few beneficiaries, 
we can only include those with more than 10 beneficiaries. 
"""
# Obtain non-suppressed beneficiaries per provider from the larger dataset 
non_supp_bene_count = data_2017.loc[data_2017['bene_count']>10,'bene_count']
# Find average
print("Q1:",np.round(non_supp_bene_count.mean(),5))

# Question 2
"""
Work out for each Specialty the fraction of drug claims that are 
for brand-name drugs. Include only providers for whom the relevant 
information has not been suppressed, and consider only specialties 
with at least 1000 total claims. What is the standard deviation of 
these fractions? 
"""
# Obtain non-suppressed relevant data from the larger dataset 
non_supp_claim_count = data_2017.loc[(data_2017['total_claim_count']>=1000) & (data_2017['brand_claim_count'].notna()), ['specialty_description','brand_claim_count','total_claim_count',]]
# Group by specialty
non_supp_fraction = non_supp_claim_count.groupby('specialty_description').sum()
# Calculate the fraction
non_supp_fraction['fraction'] = non_supp_fraction['brand_claim_count']/non_supp_fraction['total_claim_count']
# Print the result
print("Q2:",np.round(non_supp_fraction['fraction'].std(),5))

# Question 3
"""
Let's find which states have surprisingly high supply of opioids, 
conditioned on specialty. Work out the average length of an opioid 
prescription for each provider. For each (state, specialty) pair 
with at least 100 providers, calculate the average of this value 
across all providers. Then find the ratio of this value to an equivalent 
quantity calculated from providers in each specialty across all states. 
What is the largest such ratio? 
"""
# Filtering criteria
mask3 = (data_2017['opioid_claim_count']!=0) & (data_2017['opioid_claim_count'].notna())
# Obtain non-suppressed relevant data from the larger dataset 
non_supp_opioids = data_2017.loc[mask3,['specialty_description','nppes_provider_state','opioid_claim_count','opioid_day_supply']]
# Get (state, specialty) pairs
opioids_per_pair = non_supp_opioids.groupby(['specialty_description','nppes_provider_state'])['opioid_claim_count','opioid_day_supply'].sum()
# Find pairs with at least 100 providers
pairs_greater = opioids_per_pair.loc[opioids_per_pair['opioid_claim_count']>=100]
# Calculate the length of an opioid prescription
pairs_greater['opioid_length'] = pairs_greater['opioid_day_supply'] / pairs_greater['opioid_claim_count']
# Get the ratio
pairs_greater['ratio'] = pairs_greater['opioid_length'].mean() / pairs_greater['opioid_length']
# Find the largest ratio
print("Q3:",np.round(np.max(pairs_greater['ratio']),5))

# Question 4
"""
For each provider, estimate the length of the average prescription from 
the total_day_supply and total_claim_count. What is the median, in days, 
of the distribution of this value across all providers? 
"""
# Obtain non-suppressed relevant data from the larger dataset 
non_supp_ave_len_pres = data_2017.loc[data_2017['total_claim_count'].notna(),['total_day_supply','total_claim_count']]
# Calculate the length of the average prescription
non_supp_ave_len_pres['ave_len_pres'] = non_supp_ave_len_pres['total_day_supply'] / non_supp_ave_len_pres['total_claim_count']
# Find the average
print("Q4:",np.round(non_supp_ave_len_pres['ave_len_pres'].median(),5))

# Question 5
"""
Find the ratio of beneficiaries with opioid prescriptions to beneficiaries 
with antibiotics prescriptions in each state. Assume that each beneficiary
attends only a single provider. What is the difference between the largest
and smallest ratios? 
"""
# Filtering criteria
mask5 = (data_2017['opioid_bene_count']!=0) & (data_2017['opioid_bene_count'].notna()) & (data_2017['antibiotic_bene_count']!=0) & (data_2017['antibiotic_bene_count'].notna())
# Obtain non-suppressed relevant data from the larger dataset 
non_supp_opioid_antibiotic_bene_count = data_2017.loc[mask5,['opioid_bene_count','antibiotic_bene_count']]
# Calculate the ratio
non_supp_opioid_antibiotic_bene_count['ratio'] = non_supp_opioid_antibiotic_bene_count['opioid_bene_count'] / non_supp_opioid_antibiotic_bene_count['antibiotic_bene_count']
# Find the difference between the largest and smallest ratios
print("Q5:",np.round(np.max(non_supp_opioid_antibiotic_bene_count['ratio']) - np.min(non_supp_opioid_antibiotic_bene_count['ratio']),5))

# Question 6
"""
For each provider where the relevant columns are not suppressed, work out 
the fraction of claims for beneficiaries age 65 and older, as well as the 
fraction of claims for beneficiaries with a low-income subsidy. What is 
the Pearson correlation coefficient between these values? 
"""
# Filtering criteria
mask6 = (data_2017['total_claim_count']!=0) & (data_2017['total_claim_count'].notna()) & (data_2017['total_claim_count_ge65']!=0) & (data_2017['total_claim_count_ge65'].notna()) & (data_2017['lis_claim_count']!=0) & (data_2017['lis_claim_count'].notna())
# Obtain non-suppressed relevant data from the larger dataset 
non_supp_var_claim_count = data_2017.loc[mask6, ['total_claim_count','total_claim_count_ge65','lis_claim_count']]
# Calculate the fractions
non_supp_var_claim_count['fraction1'] = non_supp_var_claim_count['total_claim_count_ge65'] / non_supp_var_claim_count['total_claim_count']
non_supp_var_claim_count['fraction2'] = non_supp_var_claim_count['lis_claim_count'] / non_supp_var_claim_count['total_claim_count']
# Find the Pearson correlation coefficient between these values
print("Q6:",np.round(non_supp_var_claim_count.loc[:,'fraction1':'fraction2'].corr(method = 'pearson').unstack()[1],5))

# Question 7
"""
For each provider for whom the information is not suppressed, 
figure out the average cost per day of prescriptions in both 2016 and 2017.
Use this to estimate the inflation rate for daily prescription costs per 
provider. What is the average inflation rate across all providers? 
"""
# Filtering criteria for 2017 data
mask7a = (data_2017['total_claim_count']!=0) & (data_2017['total_claim_count'].notna()) & (data_2017['total_drug_cost']!=0) & (data_2017['total_drug_cost'].notna()) & (data_2017['total_day_supply']!=0) & (data_2017['total_day_supply'].notna())
# Obtain non-suppressed relevant data from the larger dataset for 2017 data
non_supp_cost_per_day_2017 = data_2017.loc[mask7a, ['total_claim_count','total_drug_cost','total_day_supply']]
# Filtering criteria for 2016 data
mask7b = (data_2016['total_claim_count']!=0) & (data_2016['total_claim_count'].notna()) & (data_2016['total_drug_cost']!=0) & (data_2016['total_drug_cost'].notna()) & (data_2016['total_day_supply']!=0) & (data_2016['total_day_supply'].notna())
# Obtain non-suppressed relevant data from the larger dataset for 2016 data
non_supp_cost_per_day_2016= data_2016.loc[mask7b, ['total_claim_count','total_drug_cost','total_day_supply']]
# Calculate cost per day of prescriptions
non_supp_cost_per_day_2017['cost_per_day'] = (non_supp_cost_per_day_2017['total_drug_cost'] / non_supp_cost_per_day_2017['total_claim_count']) * (non_supp_cost_per_day_2017['total_day_supply'] / non_supp_cost_per_day_2017['total_claim_count'])
non_supp_cost_per_day_2016['cost_per_day'] = (non_supp_cost_per_day_2016['total_drug_cost'] / non_supp_cost_per_day_2016['total_claim_count']) * (non_supp_cost_per_day_2016['total_day_supply'] / non_supp_cost_per_day_2016['total_claim_count'])
# Find averages of cost per day of prescriptions
ave_cost_per_day_2017 = non_supp_cost_per_day_2017['cost_per_day'].mean()
ave_cost_per_day_2016 = non_supp_cost_per_day_2016['cost_per_day'].mean()
# Calculate the inflation rate
ave_inflation = (ave_cost_per_day_2017-ave_cost_per_day_2016)/ave_cost_per_day_2016
# Print the result
print("Q7:",np.round(ave_inflation,5))
      
# Question 8
"""
Consider all providers with a defined specialty in both years. Find the 
fraction of providers who left each specialty between 2016 and 2017. 
What is the largest such fraction, when considering specialties with 
at least 1000 proviers in 2016? Note that some specialties have a 
fraction of 1 due to specialty name changes between 2016 and 2017; 
disregard these specialties in calculating your answer. 
"""
num_providers = 1000
# Filtering criteria for 2017 data
mask8a = (data_2017['specialty_description'].notna()) & (data_2017['npi'].notna())
# Obtain non-suppressed relevant data from the larger dataset for 2017 data
specialties_and_providers_2017 = data_2017.loc[mask8a,['specialty_description','npi']]
# Find the number of providers per specialty
providers_by_specialties_count_2017 = specialties_and_providers_2017.groupby(['specialty_description'])['npi'].count()
# Find specialties with at least 1000 providers
key8a = (providers_by_specialties_count_2017>=num_providers).reset_index(name ='Include')
specialties_and_providers_with_key_2017 = pd.merge(specialties_and_providers_2017,key8a)
specialties_and_providers_count_greater_2017 = specialties_and_providers_with_key_2017.loc[specialties_and_providers_with_key_2017.Include,:]
# Group by specialties for fitting criteria
providers_by_specialties_2017 = specialties_and_providers_count_greater_2017.groupby(['specialty_description','npi'])['npi'].count().reset_index(name ='count')

# Filtering criteria for 2016 data
mask8b = (data_2016['specialty_description'].notna()) & (data_2016['npi'].notna())
# Obtain non-suppressed relevant data from the larger dataset for 2016 data
specialties_and_providers_2016 = data_2016.loc[mask8b,['specialty_description','npi']]
# Find the number of providers per specialty
providers_by_specialties_count_2016 = specialties_and_providers_2016.groupby(['specialty_description'])['npi'].count()
# Find specialties with at least 1000 providers
key8b = (providers_by_specialties_count_2016>=num_providers).reset_index(name ='Include')
specialties_and_providers_with_key_2016 = pd.merge(specialties_and_providers_2016,key8b)
specialties_and_providers_count_greater_2016 = specialties_and_providers_with_key_2016.loc[specialties_and_providers_with_key_2016.Include,:]
# Group by specialties for fitting criteria
providers_by_specialties_2016 = specialties_and_providers_count_greater_2016.groupby(['specialty_description','npi'])['npi'].count().reset_index(name ='count')

# Obtain number of unique specialties
n_unique_specialties_2016 = np.unique(providers_by_specialties_2016['specialty_description'])
# Create a numpy array to store the fractions
fractions = np.zeros(np.size(n_unique_specialties_2016,axis=0))
# For each specialty
for ind,spec in enumerate(n_unique_specialties_2016):
    # Obtain providers for 2016
    specialties_2016 = providers_by_specialties_2016[providers_by_specialties_2016['specialty_description'] == spec]['npi']
    try:
        # Obtain providers for 2017
        specialties_2017 = providers_by_specialties_2017[providers_by_specialties_2017['specialty_description'] == spec]['npi']
        # If the specialty still has the same name
        if (len(specialties_2017)!=0):
            # Calculate the fractions of providers who left each specialty between 2016 and 2017
            fractions[ind] = np.size(np.setdiff1d(specialties_2016,specialties_2017))/len(specialties_2016)
    except:
        continue
# Print the largest fraction
print("Q8:",np.round(np.max(fractions),5))    