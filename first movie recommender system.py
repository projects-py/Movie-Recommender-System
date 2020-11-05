

#importing required libraries
import pandas as pd



#importing data
ratings = pd.read_csv('Documents\\Datasets\\movie recommender system dataset\\ratings.csv')
movies = pd.read_csv('Documents\\Datasets\\movie recommender system dataset\\movies.csv')


#data exploration
#checking what is in the data and merging these two files into one single file
ratings = pd.merge(movies,ratings)


#dropping features those aren't required
#these features can be used in recommendation with different criteria
ratings = ratings.drop(['genres','timestamp'],axis = 1)




print(ratings.shape)
print(ratings.head())



#we create a pivot table that have users in the rows 
#and movies in the columns and ratings as its values
userRatings = pd.DataFrame(ratings.pivot_table(index=['userId'],columns=['title'],values=['rating']))
userRatings.head()




#but in userRatings pivot table, there are alot of missing values
#so we set a threshold, if there are less that 10 values in a column, we drop that column
#as in real life, it is not viable that users would rate that much of movies
#and less than 10 ratings for a movie won't give much information
userRatings = userRatings.dropna(thresh=10,axis=1).fillna(0,axis=1)





#for the similarity, we use pearson correlation coefficients
corrMatrix = pd.DataFrame(userRatings.corr(method = 'pearson'))


#to assign names of columns as well as rows
A = []
for i in range(len(userRatings.columns)):
    A.append(userRatings.columns[i][1])
print(A)

corrMatrix.columns , corrMatrix.index = A,A






corrMatrix.head()





#defining a function that gives similar rating movies when we are given with movie_name and rating as well
def get_similar(movie_name,rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings
get_similar('12 Angry Men (1957)',5)




#movies those are to be recommended who watch these movies
#for romantic movie lover
romantic_movie_lover = [('(500) Days of Summer (2009)',5),('Alice in Wonderland (2010)',3)]
similar_movies = pd.DataFrame()
for movie_name,rating in romantic_movie_lover:
    similar_movies = similar_movies.append(get_similar(movie_name,rating))
similar_movies.sum().sort_values(ascending=False).head(10)



#movies those are to be recommended who watch these movies
#for action movie lover
action_movie_lover = [("Amazing Spider-Man, The (2012)",5),("Mission: Impossible III (2006)",4),("Toy Story 3 (2010)",2),("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)",4)]
similar_movies = pd.DataFrame()
for movie_name,rating in action_movie_lover:
    similar_movies = similar_movies.append(get_similar(movie_name,rating))
print(similar_movies.sum().sort_values(ascending=False).head(10))




