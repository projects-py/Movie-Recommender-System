#!/usr/bin/env python
# coding: utf-8

# In[136]:


#importing required libraries
import pandas as pd


# In[137]:


#importing data
ratings = pd.read_csv('Documents\\Datasets\\movie recommender system dataset\\ratings.csv')
movies = pd.read_csv('Documents\\Datasets\\movie recommender system dataset\\movies.csv')


# In[138]:


#checking what is in the data and merging these two files into one single file
ratings = pd.merge(movies,ratings)


# In[139]:


#dropping features those aren't required
ratings = ratings.drop(['genres','timestamp'],axis = 1)


# In[140]:


print(ratings.shape)
print(ratings.head())


# In[141]:


#we create a pivot table that have users in the rows 
#and movies in the columns and ratings as its values
userRatings = pd.DataFrame(ratings.pivot_table(index=['userId'],columns=['title'],values=['rating']))
userRatings.head()


# In[142]:


#but in userRatings pivot table, there are alot of missing values
#so we set a threshold, if there are less that 10 values in a column, we drop that column
#as in real life, it is not viable that users would rate that much of movies
#and less than 10 ratings for a movie won't give much information
userRatings = userRatings.dropna(thresh=10,axis=1).fillna(0,axis=1)


# In[146]:


#to assign columns and rows names
A = []
for i in range(len(userRatings.columns)):
    A.append(userRatings.columns[i][1])
print(A)


# In[147]:


#for the similarity, we use pearson correlation coefficients
corrMatrix = pd.DataFrame(userRatings.corr(method = 'pearson'))


# In[148]:


corrMatrix.columns , corrMatrix.index = A,A


# In[149]:


corrMatrix.head()


# In[150]:


#defining a function that gives similar rating movies when we are given with movie_name and rating as well
def get_similar(movie_name,rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings
get_similar('12 Angry Men (1957)',5)


# In[151]:


#movies those are to be recommended who wtach these movies
romantic_movie_lover = [('(500) Days of Summer (2009)',5),('Alice in Wonderland (2010)',3)]
similar_movies = pd.DataFrame()
for movie_name,rating in romantic_movie_lover:
    similar_movies = similar_movies.append(get_similar(movie_name,rating))
similar_movies.sum().sort_values(ascending=False).head(10)


# In[153]:


action_movie_lover = [("Amazing Spider-Man, The (2012)",5),("Mission: Impossible III (2006)",4),("Toy Story 3 (2010)",2),("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)",4)]
similar_movies = pd.DataFrame()
for movie_name,rating in action_movie_lover:
    similar_movies = similar_movies.append(get_similar(movie_name,rating))
print(similar_movies.sum().sort_values(ascending=False).head(10))


# In[ ]:




