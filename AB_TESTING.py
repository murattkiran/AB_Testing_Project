##############################################################
# AB Testing: Comparison of Facebook Bidding Methods
# in terms of the Number of Products Sold after Clicks."
##############################################################



###############################################################
# Project Tasks
###############################################################


#####################################################
# Task 1: Data Preparation and Analysis
#####################################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Step1: Step 1: Read the dataset ab_testing_data.xlsx consisting of control and test group data.
# Assign control and test group data to separate variables

df_control = pd.read_excel("ABTesti/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("ABTesti/ab_testing.xlsx", sheet_name="Test Group")


# Step 2: Analyze control and test group data.
def check_df(dataframe, head=5):
    print("############### Shape ################")
    print(dataframe.shape)
    print("########### Types ###############")
    print(dataframe.dtypes)
    print("########### Head ###############")
    print (dataframe.head(head))
    print ("########### Tail ###############")
    print ( dataframe.tail(head))
    print ( "########### NA ###############")
    print ( dataframe.isnull().sum())
    print ( "########### Quantiles ###############")
    print ( dataframe.describe().T )

check_df(df_control)
check_df(df_test)


# Step 3: After the analysis process, combine the control and test group data using the concat method.
df_main = pd.concat([df_control, df_test], ignore_index=True)
df_main.head()
df_main.tail()



#####################################################
# Task 2: Define the Hypothesis of A/B Test
#####################################################
# Step 1: Define the hypothesis.

# H0: M1 = M2 ("There is no statistically significant difference between the number of purchases for Maximum Bidding and Average Bidding.")
# H1: M1 != M2 ("There is a statistically significant difference between the number of purchases for Maximum Bidding and Average Bidding.")


# Step 2: Analyze the purchase averages for the control and test groups.
df_control["Purchase"].mean()
df_test["Purchase"].mean()
# The number of purchases ("Purchase") has increased with the new bidding method "Average Bidding."
# However, we need to test if this increase is statistically significant using hypothesis testing.



#####################################################
# Task3: Performing Hypothesis Testing
#####################################################

######################################################
# AB Testing for 'Purchase' Variable
######################################################

# Step 1: Perform hypothesis checks before hypothesis testing.
# These are Assumption of Normality and Homogeneity of Variance. Test separately whether the control and test groups
# comply with the assumption of normality over the Purchase variable.

"""Assumption of normality:
H0: The normal distribution assumption is satisfied.
H1: The normal distribution assumption is not satisfied.
p < 0.05 H0 is rejected, p > 0.05 H0 cannot be rejected.

Based on the test results, is the normality assumption satisfied for both the control and test groups?
Interpret the obtained p-value values.
"""

test_stat, pvalue = shapiro(df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891
# p-value > 0.05, H0 cannot be rejected.
# The assumption of normal distribution is satisfied

test_stat, pvalue = shapiro(df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9589, p-value = 0.1541
# p-value > 0.05, H0 cannot be rejected.
# The assumption of normal distribution is satisfied


# Step 2: Assumption of homogeneity of variance

"""Homogeneity of variance :
H0: The homogeneity of variance is satisfied.
H1: The homogeneity of variance is not satisfied.
p < 0.05 HO is rejected , p > 0.05 H0 cannot be rejected.
"""
test_stat, pvalue = levene(df_control["Purchase"], df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083
# p-value > 0.05 HO is not rejected, the homogeneity of variance is satisfied.


# When both assumptions are met, an 'Two-Sample Independent t-Test' is conducted.

test_stat, pvalue = ttest_ind(df_control["Purchase"],df_test["Purchase"], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493
# The p-value is greater than 0.05, so H0 cannot be rejected.
# Therefore, there is no statistically significant difference between the Control group, where the "maximum offer" campaign is presented,
# and the Test group, where the "average offer" campaign is presented.




##############################################################
# Task 4: Analysis of Results
##############################################################

# Step 1: Which test did you use, state the reasons.

# In this study, an Independent Two Sample T-test, also known as an AB test, was used to compare the means of two groups.
# The reason for choosing this test over the Mann Whitney U test (non-parametric) is that
# the 'Purchase' variables in the control and test groups have distributions that resemble a standard normal distribution, and the distributions of these two groups are similar to each other, indicating that their variances are homogeneous."




# Step 2: Advise the customer according to the test results you have obtained.

#Since there is no significant difference between the methods in terms of purchase outcomes, customers can choose either method.
# However, differences in other statistics should also be considered.
# Therefore, as a recommendation, it would be beneficial to evaluate these other differences and determine which method is more profitable.
# Of course, this would require extending the duration of the test to gather sufficient data for a more comprehensive analysis.


