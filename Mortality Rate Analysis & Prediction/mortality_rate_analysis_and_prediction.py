# -*- coding: utf-8 -*-
"""mortality_rate_analysis_and_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ily4pSIrRPCayjp5CFWg4cumtejVxGmm

#**MORTALITY RATE ANALYSIS AND PREDICITON**

<p align="center">
  <img width="600" height="325" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkQz50DoqEHuYF7JGsWxfdBPOagT-geA5X_A&usqp=CAU">
</p>

* A mortality rate is the number of deaths due to a disease divided by the total population. If there are 25 lung cancer deaths in one year in a population of 30,000, then the mortality rate for that population is 83 per 100,000.

* We use mortality statistics to: produce population estimates and population projections, both national and subnational, produce life expectancy estimates, and quality assure census estimates.

### The dataset being used is curated from WHO's Health Dataset catalog. It contains mortality rate for people worldwide classified on age and gender.
https://www.kaggle.com/datasets/navinmundhra/world-mortality

https://www.kaggle.com/code/vishesh1412/life-expectancy-prediction-feature-selection-ols/data

##IMPORT THE LIBRARIES
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import *
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

"""## Distribution graphs of column data

"""

def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'g', edgecolor = 'g')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 2.0, w_pad = 3.0, h_pad = 1.0)
    plt.show()

"""##IMPORT THE ADULT MORTALITY DATASET"""

nRowsRead = 1000 
# Adult mortality.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('/content/Adult mortality.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = 'Adult mortality.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')

df1.info

df1 = df1.iloc[1:, :]
df1.head(20)

plotPerColumnDistribution(df1, 15, 9)

"""##IMPORT THE MATERNAL MORTALITY DATASET"""

nRowsRead = 1000 
# Maternal mortality.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df2 = pd.read_csv('/content/Maternal mortality.csv', delimiter=',', nrows = nRowsRead)
df2.dataframeName = 'Maternal mortality.csv'
nRow, nCol = df2.shape
print(f'There are {nRow} rows and {nCol} columns')

df2.head(10)

df2.info

plotPerColumnDistribution(df2, 24, 9)

"""## LOAD THE NO. OF DEATHS DATASET"""

nRowsRead = 1000 
# Number of deaths (thousands).csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df3 = pd.read_csv('/content/Number of deaths (thousands).csv', delimiter=',', nrows = nRowsRead)
df3.dataframeName = 'Number of deaths (thousands).csv'
nRow, nCol = df3.shape
print(f'There are {nRow} rows and {nCol} columns')

df3.head(10)

df3.info

plotPerColumnDistribution(df3, 10, 5)

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

"""### Hence, different visualization techniques can be used to get deeper insights into data and hence make predictive analysis

### Now to make predictions, we will make use of another dataset provided by WHO

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Basic Data Cleaning and Preprocessing</div>
<center>

Data cleaning and preprocessing is very essential to get an overall feel of the data. Preprocessing is important to feed the data further in the algorithms so that they can work effectively.
"""

data = pd.read_csv('/content/Life Expectancy Data.csv')

data

df = pd.DataFrame(data)
df.shape

"""We can see that our dataset contains 2938 rows and 22 attributes!

Now let's see the correlation coefficient of all the attributes with the other attributes, as this will tell us more about how the various attributes depend on each other and we'll get a better insight on the dependency of attributes over each other.
"""

df.corr()
# this will make a correlation matrix which computes the Pearsons correlation coefficent 
# of columns with each other.

"""Now let's make a heatmap out of the above matrix for a better visual understanding"""

corr = df.corr()
corr.style.background_gradient(cmap='nipy_spectral_r')

"""From the above heatmap, we can draw the following conclusions:
1. Percentage Expenditure and GDP are quite highly correlated (0.89)
2. Schooling is correlated nicely with Life Expectancy (0.75), which tells an interesting insight that can this be due to helthy lifestyle which one learns through the schooling process?
3. Hepatitis B is correlated with Diptheria (0.61), which can tell us that maybe these two depend on a common factor (might be some causants)

Now let's check for the missing values in our dataset so that we can impute those values with suitable data points

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Finding Missing Values</div>
<center>

Missing values can prove to be a major pain as they may affect the run of the algorithms as almost all the algorithms expect the full data but return error if some points are missing. So, cleaning the data is essential!
"""

# using missingno library to get a feel of the missing entries

import missingno as msno
msno.bar(df)

"""Using the above bar chart, we can see that many attributes have missing values, like Hepatitis B has 2385 values, whereas the expected number of values for every attribute is 2938.
Now we have to find a way to fill in all these missing values as these may cause problems for our algorithm.
We'll use the impute method of pd.DataFrame.fillna and impute the previous values in all these missing fields, previous values can be a good way to fill in such entries.

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Imputing Missing Values</div>
<center>

There are many ways to impute the mission data points like:
* Fill the missing points with the mean of rest of the data
* Fill the missing values with previous values
* Fill the missing points with the median of rest of the dataset
<br><br> We'll fill the values with previous points
"""

pip install sklearn

"""To impute the missing values, we'll have to make sure that we run the imputer after dropping the attributes with textual data (we can use one-hot encoding for that but we don't need it here as the textual data has no missing points)."""

df_num = df.drop(["Country", "Status"], axis=1)

df_num

"""One interesting thing in this dataset is that the names of the columns are not written in a nice manner, like in some names there is a space before the name, in some after the name and in some names there is a space in both before and after the name like " BMI ". To tackle this, let's print the names of all the columns"""

df.columns.values.tolist()

"""We have stored all the numerical features in df_num dataframe and now we'll use this to impute the values!"""

df_num["Hepatitis B"].fillna( method ='ffill', inplace = True)
df_num["Alcohol"].fillna( method ='ffill', inplace = True)
df_num["Adult Mortality"].fillna( method ='ffill', inplace = True)
df_num["Polio"].fillna( method ='ffill', inplace = True)
df_num["Total expenditure"].fillna( method ='ffill', inplace = True)
df_num["GDP"].fillna( method ='ffill', inplace = True)
df_num["Population"].fillna( method ='ffill', inplace = True)
df_num["Schooling"].fillna( method ='ffill', inplace = True)
df_num["Income composition of resources"].fillna( method ='ffill', inplace = True)
df_num["Life expectancy "].fillna( method ='ffill', inplace = True)
df_num["Diphtheria "].fillna( method ='ffill', inplace = True)
df_num[" thinness 5-9 years"].fillna( method ='ffill', inplace = True)
df_num[" thinness  1-19 years"].fillna( method ='ffill', inplace = True)
df_num[" BMI "].fillna( method ='ffill', inplace = True)

"""We have imputed the missing values with the mean of the rest of the data points, now let's check if we have any more missing data"""

msno.bar(df_num)

"""We have imputed the values in all the missing data points, and as a result according to the above bar chart, we have no missing values left now.

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Plotting Chloropleth Maps</div>
<center>

Chloropleth maps or graphs can be a very good way to plot the data points on a map. It provides enhanced visuals and helps us to know about the data more easily!
"""

pip install plotly

df_chloropleth = df_num
df_chloropleth['Country'] = df['Country']
df_chloropleth

# we'll use this particular dataframe for making chloropleth maps

"""Let's make the chloropleth map for the BMI of different countries!"""

pip install pycountry

import pycountry
import plotly.express as px
import pandas as pd
URL_DATASET = r'/content/Life Expectancy Data.csv'
df1 = pd.read_csv(URL_DATASET)
list_countries = df1['Country'].unique().tolist()
d_country_code = {} 
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        d_country_code.update({country: ' '})

for k, v in d_country_code.items():
    df1.loc[(df1.Country == k), 'iso_alpha'] = v

fig = px.choropleth(data_frame = df1,
                    title = "BMI of various countries over the years",
                    locations= "iso_alpha",
                    color= " BMI ",  
                    hover_name= "Country",
                    color_continuous_scale= ['cyan','blue','midnightblue','darkblue'], 
                    animation_frame= "Year")

fig.show()

"""Looking at the above chloropleth map and analysing it, we see an overall increasing trends in the BMI of most of the countries! So, we can say that on an average, people are getting more and more obese.

Let's draw the same map for the Life Expectancy of the countries over the years
"""

import pycountry
import plotly.express as px
import pandas as pd
URL_DATASET = r'/content/Life Expectancy Data.csv'
df1 = pd.read_csv(URL_DATASET)
list_countries = df1['Country'].unique().tolist()
d_country_code = {} 
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        d_country_code.update({country: ' '})

for k, v in d_country_code.items():
    df1.loc[(df1.Country == k), 'iso_alpha'] = v

fig = px.choropleth(data_frame = df1,
                    title = "Life Expectancy of various countries over the years",
                    locations= "iso_alpha",
                    color= "Life expectancy ",  
                    hover_name= "Country",
                    color_continuous_scale= ['cyan','blue','midnightblue','darkblue'], 
                    animation_frame= "Year")

fig.show()

"""In the same fashion we can draw the chloropleth maps of other attributes as well!

Now let's have a look at the distribution of some of the different columns

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Plotting Distributions of the Attributes</div>
<center>

Distributions of the attributes can be a very good way to get to know more about the data as using them we can reach to interesting conclusions and modelling the data becomes important!
"""

sns.distplot(df_num['Year']);

sns.distplot(df_num['Life expectancy ']);

sns.distplot(df_num['Alcohol']);

sns.distplot(df_num[' BMI ']);

"""# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Kolmogorov Smirnov Test and Comparisons | Distribution Analysis</div>
<center>

We can see that the BMI attribute does not look normally distributed, so let's run Kolmogorov-Smirnov test to see whether our auumption is true or not and to see that whether it works or not!

Now let's analyse the distributions using Kolmorogov- Smirnov test
"""

df_num.columns.values.tolist()

from scipy.stats import kstest, norm

#perform Kolmogorov-Smirnov test
kstest(df_num['Alcohol'], 'norm')

"""We observe that when we run Kolmorogov-Smirnov test on the "Alcohol" attribute, the p-value is 0, which is less than 0.05, so we reject the hypothesis and get to know that the data does not come from a normal distribution! Now let's run the same test on some other attributes.

We'll run the test on the following attributes and then have look at their graphs to see how close are we! 
"""

kstest(df_num[' BMI '], 'norm')

sns.distplot(df_num[' BMI ']);

"""Like we observed in our graph made above, the KS test also quantifies that the BMI is not normally distributed."""

kstest(df_num['Life expectancy '], 'norm')

sns.distplot(df_num['Life expectancy ']);

kstest(df_num['Year'], 'norm')

sns.distplot(df_num['Year']);
# this looks as two distributions overlap each other as we can see two peaks, or we can say
# that it is bimodal!

kstest(df_num[ 'Adult Mortality'], 'norm')

sns.distplot(df_num['Adult Mortality']);

# in the initial phase it looks gaussian, however later in phase, it resembles more as an 
# exponential distribution!

kstest(df_num[ 'infant deaths'], 'norm')

sns.distplot(df_num['infant deaths']);

# this resembles the poisson distribution!

"""# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Data Scaling | Normalization</div>
<center>

We can perform the feature scaling using two methods:
* Normalization: Making the values between 0 and 1
* Standardization: Transforming the data so that the mean is 0 and standard deviation is 1
<br><br>Since both of these are part of feature scaling, let's chose the first one and normalize the data and set it to be between 0 and 1.
"""

df_fin = df.drop(["Country", "Status"], axis=1)
df_fin

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df_norm = pd.DataFrame(scaler.fit_transform(df_fin), columns=df_fin.columns)
df_norm

"""We have stored our scaled data in df_norm DataFrame and now we'll use this dataframe to feed into the regression pipeline further!

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">SK Learn Pipeline</div>
<center>

Now we have to make a pipeline which takes the raw data as input and finally prepares the data we just finalized, including the scaled values!

We'll transform the data into final scaled format in just one cell as below:
"""

sk_data = pd.read_csv('/content/Life Expectancy Data.csv')
sk_num = sk_data.drop(["Country", "Status"], axis=1)

# till here we have dropped textual attributes

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean', missing_values=np.nan)
imputer = imputer.fit(sk_num[['Year',
 'Life expectancy ',
 'Adult Mortality',
 'infant deaths',
 'Alcohol',
 'percentage expenditure',
 'Hepatitis B',
 'Measles ',
 ' BMI ',
 'under-five deaths ',
 'Polio',
 'Total expenditure',
 'Diphtheria ',
 ' HIV/AIDS',
 'GDP',
 'Population',
 ' thinness  1-19 years',
 ' thinness 5-9 years',
 'Income composition of resources',
 'Schooling']])
sk_num[['Year',
 'Life expectancy ',
 'Adult Mortality',
 'infant deaths',
 'Alcohol',
 'percentage expenditure',
 'Hepatitis B',
 'Measles ',
 ' BMI ',
 'under-five deaths ',
 'Polio',
 'Total expenditure',
 'Diphtheria ',
 ' HIV/AIDS',
 'GDP',
 'Population',
 ' thinness  1-19 years',
 ' thinness 5-9 years',
 'Income composition of resources',
 'Schooling']] = imputer.transform(sk_num[['Year',
 'Life expectancy ',
 'Adult Mortality',
 'infant deaths',
 'Alcohol',
 'percentage expenditure',
 'Hepatitis B',
 'Measles ',
 ' BMI ',
 'under-five deaths ',
 'Polio',
 'Total expenditure',
 'Diphtheria ',
 ' HIV/AIDS',
 'GDP',
 'Population',
 ' thinness  1-19 years',
 ' thinness 5-9 years',
 'Income composition of resources',
 'Schooling']])

# Now we have also imputed the missiong values using mean method


from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
sk_norm = pd.DataFrame(scaler.fit_transform(sk_num), columns=sk_num.columns)
sk_norm

# We have also scaled our data, so our SK Learn pipeline is ready!

"""Above is the result when we used normalization, which scales the values between 0 and 1, now let's scale the data as done below using SKLearn pipeline"""

from sklearn.base import BaseEstimator, TransformerMixin

class fill_median(BaseEstimator, TransformerMixin):
    # Taking which column to modify as "col" parameter
    def __init__(self, col):
        self.col = col
    
    # Fit just calculated the median value and stores it as class variable
    def fit(self, X, y=None):
        self.median = X[self.col].median()
        return self
    
    # Transform updates all NaN values with median
    def transform(self, X):
        return X.fillna(self.median)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pre_pipe = Pipeline([
    ('fillna', fill_median(col=['Year',
 'Life expectancy ',
 'Adult Mortality',
 'infant deaths',
 'Alcohol',
 'percentage expenditure',
 'Hepatitis B',
 'Measles ',
 ' BMI ',
 'under-five deaths ',
 'Polio',
 'Total expenditure',
 'Diphtheria ',
 ' HIV/AIDS',
 'GDP',
 'Population',
 ' thinness  1-19 years',
 ' thinness 5-9 years',
 'Income composition of resources',
 'Schooling'])),
    ('Standard_scaling', StandardScaler())
])

# we are calling fit_transform() on pipeline, so the pipeline is learning parameters from input data.
# Later it also transforms the input data as per the "transform()" definition of each object
train_prepared = pre_pipe.fit_transform(sk_num)
train_prepared

"""Above is our final scaled values which we got using sklearn! However, we are not going to use the scaled data, as it may cause problems, so we'll go with normalized data instead.

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Splitting the Data in Test and Train Manually & Running Linear Regression</div>
<center>

Validation set is very imporatant to judge the algorithm before we decide it to show the unseen data, as once the model sees the test data, it may get biased and that's what we want to avoid.<br><br>
Cross validation refers to taking one data points of the data divided into n points (n is the hyperparameter), and then training the data on the rest of the parts. When training is complete, we test the model on the point which was left earlier!<br><br> 
First let's see how the regression runs without the validation set:
"""

sk_norm = sk_norm.drop(['Year'], axis = 1)

sk_norm

"""We dropped the year column as year in which the data was collected is not having any effect of the life expectancy"""

X = sk_norm.iloc[:,1:].values
y = sk_norm.iloc[:,0].values

"""We did this to separate dependent and independent variables"""

X

y

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X, y)

print(regressor.intercept_)

print(regressor.coef_)

"""With this we get to know that the line which best fits our data is:<br>
y = -2.78*x1 + 3.99*x2 + .....+ 0.3491<br><br>
However, we have not checked this line for accuracy using a test set and a training set, so let's try that approach!

Now let's make a part of code which splits the data into training and testing set so that we can see that how our model fares on the test set!
"""

import random
total=[]
for i in range (0,len(sk_norm)):
    total.append(i)
    
num_train = int(len(total)*0.8)
num_test = len(total) - num_train

set_train = random.sample(total, num_train) # we take random sample of 80% data for training
set_test = [i for i in total if i not in set_train] # we take rest of the 20% data for the test set

train = sk_norm.iloc[set_train,:] 
train

test = sk_norm.iloc[set_test,:] 
test

"""We have successfully splitted the data into the test and train sets respectively. The division is purely random and each time we run the code, a new training set and testing set will be created. Let's run the resgressor algorithm on this training set and then see it's accuracy using the testing set!"""

X = train.iloc[:,1:].values
y = train.iloc[:,0].values

x = test.iloc[:,1:].values
Y = test.iloc[:,0].values

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X, y)

predictions=regressor.predict(x)
predictions

r2_score = regressor.score(x,Y)

print(r2_score*100,'%')

"""So, according to our current model, the accuracy that we have got is 83.488%, which is a pretty good score!<br><br> Now let's run the same operation using a validation set!

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Validation Set & Cross Validation (Along with Linear Regression)</div>
<center>

Let's use the concept we used above to make a validation and run a cross validation setting and see our overall accuracy of the model on the training data!
"""

import random
acc = []

number = 10 # this is the hyperparameter which will decide that how many folds you want to use

for i in range (0, number):
    total=[]
    for i in range (0,len(sk_norm)):
        total.append(i)

    num_train = int(len(total)*0.8)
    num_test = len(total) - num_train

    set_train = random.sample(total, num_train) # we take random sample of 80% data for training
    set_test = [i for i in total if i not in set_train] # we take rest of the 20% data for the test set

    train = sk_norm.iloc[set_train,:] 
    test = sk_norm.iloc[set_test,:] 

    X = train.iloc[:,1:].values
    y = train.iloc[:,0].values

    x = test.iloc[:,1:].values
    Y = test.iloc[:,0].values

    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X, y)
    r2_score = regressor.score(x,Y)
    acc.append(r2_score)

avg = sum(acc)/len(acc)
print('The average percentage accuracy over the validation set is:')
print(avg*100, '%')

"""# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Feature Selection | Lasso Regularization</div>
<center>

Feature selection is one of the most important parts for any ML model. We always want to select those features which have the maximum effect on our final output. We'll perform the following operations for feature selection:
1. Lasso Method
2. OLS Regression
3. SK Learn

First Let's use the Lasso method for feature selection, and we'll count every feature with a non zero value after regularization
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Lasso

pipeline = Pipeline([
                     ('scaler',StandardScaler()),
                     ('model',Lasso())
])

search = GridSearchCV(pipeline,
                      {'model__alpha':np.arange(0.1,10,0.1)},
                      cv = 5, scoring="neg_mean_squared_error",verbose=3
                      )

search.fit(X,y)

search.best_params_

coefficients = search.best_estimator_.named_steps['model'].coef_

importance = np.abs(coefficients)
importance

"""We observe that according to the lasso regression, only the features with indices 1, 17 and 18 have the required effect on the final regression result, while the rest of the values hold little to no importance on the result!

Now let's see that which features are the ones which correspond to the above indices:
"""

indices = []
for i in range(0, len(importance)):
    if importance[i] > 0:
        indices.append(i)
indices

for i in range(0, len(indices)):
    print(train.columns[indices[i]])

"""Above are the features which are the best features according to the lasso method for feature selection, so now let's perform the linear regression with these features and see the accuracy!"""

df_lasso = sk_norm[["Life expectancy ", " thinness 5-9 years", "Income composition of resources"]]

import random
acc = []

number = 10 # this is the hyperparameter which will decide that how many folds you want to use

for i in range (0, number):
    total=[]
    for i in range (0,len(df_lasso)):
        total.append(i)

    num_train = int(len(total)*0.8)
    num_test = len(total) - num_train

    set_train = random.sample(total, num_train) # we take random sample of 80% data for training
    set_test = [i for i in total if i not in set_train] # we take rest of the 20% data for the test set

    train = df_lasso.iloc[set_train,:] 
    test = df_lasso.iloc[set_test,:] 

    X = train.iloc[:,1:].values
    y = train.iloc[:,0].values

    x = test.iloc[:,1:].values
    Y = test.iloc[:,0].values

    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X, y)
    r2_score = regressor.score(x,Y)
    acc.append(r2_score)

avg = sum(acc)/len(acc)
print('The average percentage accuracy over the validation set is:')
print(avg*100, '%')

"""Now let's see the effect of feature selection using forward and backward using a library called mlxtend, we'll see forward selection first"""

import joblib

sys.modules['sklearn.externals.joblib'] = joblib

from mlxtend.feature_selection import SequentialFeatureSelector as sfs

X_bs = train.iloc[:,1:]
y_bs = train.iloc[:,0]

clf = LinearRegression()

# Build step forward feature selection
sfs1 = sfs(clf,k_features = X.shape[1],forward=True,floating=False, scoring='r2',cv=5)

# Perform SFFS
sfs1 = sfs1.fit(X_bs, y_bs)
sfs1

feat_names = list(sfs1.k_feature_names_)
print(feat_names)

from mlxtend.feature_selection import SequentialFeatureSelector as sfs

X_bs = train.iloc[:,1:]
y_bs = train.iloc[:,0]

clf = LinearRegression()

# Build step forward feature selection
sfs1 = sfs(clf,k_features = X.shape[1],forward=False,floating=False, scoring='r2',cv=5)

# Perform SFFS
sfs1 = sfs1.fit(X_bs, y_bs)
sfs1

feat_names = list(sfs1.k_feature_names_)
print(feat_names)

"""In the above cell we have performed feature selection with backward methodology, and we get the same result as forward!

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Feature Selection | OLS Regression</div>
<center>
"""

import statsmodels.api as sm

train = sk_norm.iloc[set_train,:] 
test = sk_norm.iloc[set_test,:] 

X = train.iloc[:,1:].values
y = train.iloc[:,0].values

x = test.iloc[:,1:].values
Y = test.iloc[:,0].values

x = sm.add_constant(X)

result = sm.OLS(y, X).fit()

print(result.summary())

"""Now, if we consider that a good p value would be a one greater than 0.05 or within 5%, then the attributes or features that we can reject are:
1. x1
2. x2
3. x5
4. x7
5. x8
6. x9
7. x10
8. x11
9. x12
10. x17
11. x18

So, effectively, the only features that are valuable for us or that have any impact on the dependent variable are:
1. Alcohol
2. percentage expenditure
3. Measles
4. GDP
5. Population
6. thinness 1-19 years	
7. thinness 5-9 years

So we see that out of the total of 18 attributes, the only one that we need are just 7, which shows the importance of feature selection in machine learning!
"""

df_ols = sk_norm[["Alcohol", "percentage expenditure", "Measles ", "GDP", "Population", " thinness  1-19 years", " thinness 5-9 years"]]

df_ols

"""Now we have the above datafram on which we can run our regression model and see how it performs!"""

import random
acc = []

number = 10 # this is the hyperparameter which will decide that how many folds you want to use

for i in range (0, number):
    total=[]
    for i in range (0,len(df_ols)):
        total.append(i)

    num_train = int(len(total)*0.8)
    num_test = len(total) - num_train

    set_train = random.sample(total, num_train) # we take random sample of 80% data for training
    set_test = [i for i in total if i not in set_train] # we take rest of the 20% data for the test set

    train = df_ols.iloc[set_train,:] 
    test = df_ols.iloc[set_test,:] 

    X = train.iloc[:,1:].values
    y = train.iloc[:,0].values

    x = test.iloc[:,1:].values
    Y = test.iloc[:,0].values

    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X, y)
    r2_score = regressor.score(x,Y)
    acc.append(r2_score)

avg = sum(acc)/len(acc)
print('The average percentage accuracy over the validation set is:')
print(avg*100, '%')

"""We observe that by going with feature selection either with Lasso or OLS, we reduce our overall accuracy of the model which is a very bad case

# <div style="font-family: Trebuchet MS; background-color: #8A0030; color: #FFFFFF; padding: 12px; line-height: 1.5;">Feature Selection | SK Learn</div>
<center>

Now let's perform a backward feature selection with sklearn library and see the results that which features are selected and which are discarded
"""

from sklearn.feature_selection import SequentialFeatureSelector

X_bs = train.iloc[:,1:]
y_bs = train.iloc[:,0]
    
#Selecting the Best important features according to Logistic Regression
sfs_selector = SequentialFeatureSelector(estimator=LinearRegression(), n_features_to_select = 3, cv =10, direction ='backward')
sfs_selector.fit(X_bs, y_bs)
X_bs.columns[sfs_selector.get_support()]

"""So we see that according to the backward feature selection, the features that got selected are:
1. percentage expenditure
2. Population
3. thinness 1-19 years

Now let's see the same effect if we run the same with forward feature selection!
"""

#Selecting the Best important features according to Logistic Regression
sfs_selector = SequentialFeatureSelector(estimator=LinearRegression(), n_features_to_select = 3, cv =10, direction ='forward')
sfs_selector.fit(X_bs, y_bs)
X_bs.columns[sfs_selector.get_support()]

"""We observe that the features are the same even on running the feature selection with forward direction, so in this case, backward and forward feature selection has the same output

# CONCLUSION

The predicting factors do affect life expectancy in one way or the another. We performed various kinds of feature selections like Lasso, OLS, Sk Learn and even implemented forward and backward selection. We saw that leaving out some features do affect the average value of life expectancy. This simple has the reason that for example alcohol has adverse effect on the liver, which in turn affects our life expectancy. Same thing happes with various disease like Hepatitis or Measles, which further have the capacity to reduce our life expectancy <br><br>

B. Let's draw a graph and see that how life expectancy depends on the percentage expenditure factor:
"""

life = sk_norm['Life expectancy '].tolist()
exp = sk_norm['percentage expenditure'].tolist()

import matplotlib.pyplot as plt
plt.scatter(life, exp)
plt.show

life = df['Life expectancy '].tolist()
exp = df['percentage expenditure'].tolist()

import matplotlib.pyplot as plt
plt.scatter(life, exp)
plt.show

"""We observe an interesting situation here! We see that if the average life of a country is less that 65, then the effect of increasing the expenditure on health shows no relation, however, if the average age is between 65 to 85, then the avergae spending plays a tremendous part here! <br>
Thus, countries with average life expectance above 65 should spend more in order to improve the average lifespan

C. The correlation between infant mortality rate and adult mortality rate and the average lifespan is as follows:<br>
IMR and Lifespan: -0.196557<br>
AMR and Lifespan: -0.696359<br>
We see that the correlation between these two and average lifespan is negative, which means that if the infant mortality rate or the adult mortality rate rises, then the average lifespan decrease, which is quite intuitive

D. Let's see the correlation between the life expectancy and various lifestyle habits like Alcohol.<br>
Alcohol and Lifespan: 0.404877	<br>
So, we can say that alcohol affects the life expectancy upto some extent as seen by the correlation coefficient!

E. Let's draw a scatter plot for Schooling vs Lifespan and the analyse it using the correlation coefficient
"""

sch = df['Schooling'].tolist()

import matplotlib.pyplot as plt
plt.scatter(life, sch)
plt.show

"""We can see that schooling has a very strong direct correlation with the average lifespan, with a Pearson's correlation coefficient of 0.75. This may be due to the fact that schooling teaches many things about a healthy lifestyle and even first aids, which can be life saving in critical conditions

F. Life expectancy has a direct positive correlation with drinking alcohol with a correlation coefficient of 0.404877

G. The correlation coefficient of the population of a country and the life expectancy is -0.021538, which basically means that if the population rises, then the life expectancy decrease. This may be due to the fact the more population have severe effect on the capacity of the health system and it may crash because of this
"""