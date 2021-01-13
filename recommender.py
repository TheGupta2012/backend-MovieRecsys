import numpy as np
import pandas as pd
import random as random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from operator import itemgetter
from rapidfuzz import process

class Recommender:
    def __init__(self):
        '''
        This is a recommender class which contains
        all the functionality for providing recommendations
        given a query string.
        ATTRIBUTES ->
        movies : imdb data pre-processed according to need
        movie_dict : dict of movie names with indices {name : index}
        names : names of the people in the dataset
        genres : unique genres in movies dataset
        data_for_cosine : basis data for count vectorizer of data( can be made customizable )
        count_matrix: vectorized word count for the movies data
        cosine: pairwise cosine similarity calculated for the movies

        METHODS ->
        get_movies : to generate the movies for the class instance
        get_names : to generate the famous for names
        get_genre : to generate the unique genres
        get_dict_movie : to get the dictionary of movies with there indices for fast look-up
        get_cosine_data : get the raw data to be transformed for the recommender
        get_count_matrix : get the Count Matrix for the recommender
        get_cosine_sim : get the pairwise cosine similarity values for the recommender
        determine_query : to determine the type of the query we have recieved
        recommend_default : to get the best default recommendations
        recommend_name : to determine the movie recommendation on the basis of the person name
        recommend_genre : to determine the movie recommendation on the basis of the genre given
        recommend_movie : to determine the movie recommendation on the basis of movie name given
        '''
        self.movies = self.get_movies()
        self.movie_dict = self.get_dict_movie()
        self.names = self.get_names()
        self.genres = self.get_genre()
        self.data_for_cosine = self.get_cosine_data()
        self.count_matrix = self.get_count_matrix()
        self.cosine = self.get_cosine_sim()

    def get_movies(self):
        movies = pd.read_csv("data/movies.csv")
        return movies

    def get_names(self):
        names = pd.read_csv(r"data/small_names.csv")
        return names

    def get_genre(self):
        genre = set()
        for k in self.movies['genres']:
            g = k.split(",")
            for i in g:
                genre.add(i)
        return genre

    def get_dict_movie(self):
        movie_dict = {}
        for i in self.movies.index:
            movie_dict[self.movies["primaryTitle"][i]] = i
        return movie_dict

    def get_cosine_data(self):
        ''' This is currently a pre defined data function
        Can be customized using a weights dictionary to
        personalize recommendations '''
        rawdata = self.movies['titleType']+self.movies['startYear'].astype('str')+self.movies['genres'].apply(lambda x:str(x*2)) + self.movies['director_name'].apply(lambda x:str(x*3))+self.movies['cast'].apply(lambda x:str(x*3))
        return rawdata

    def get_count_matrix(self):
        count = CountVectorizer(analyzer='word',ngram_range=(1, 1),min_df=0, stop_words='english')
        count_matrix = count.fit_transform(self.data_for_cosine)
        return count_matrix

    def get_cosine_sim(self):
        cosine = linear_kernel(self.count_matrix,self.count_matrix)
        return cosine

    def determine_query(self,query = None):
        '''To determine which type of query has been
        asked by the user for the recommendation'''
        if query is None:
            return None
        # now check the query matched which of the
        # part the best...
        query = query.lower()
        if len(query.split(" ")):
            q = query.split(" ")[0]
        if("sci" in query or "fi" in query):
            q = 'sci-fi'
        if q in self.genres:
            return "Genre"
        # check for name query
        n_match = process.extractOne(query,list(self.names['primaryName']))
        # check for movie query
        m_match = process.extractOne(query,self.movie_dict.keys())

        name_perc = n_match[1]
        movie_perc = m_match[1]
        if(movie_perc > name_perc):
            return "Movie"
        else:
            return "Name"


    def recommend_genre(self,query):
        '''
        Return a recommendation based on the
        genre provided
        Returns randomized but top recommendations'''
        query = query.lower()
        if len(query.split(" ")):
            query = query.split(" ")[0]
        if("sci" in query or "fi" in query):
            query = 'sci-fi'
        rec_movie = []
        for i in self.movies.index:
            k = self.movies['genres'][i]
            m = self.movies['primaryTitle'][i]
            w = self.movies['weight_average'][i]
            if query in k.split(","):
                rec_movie.append([m,w])
        # itemgetter is a way to customize the sort function, gets the second element
        # of the list element
        rec_movie = sorted(rec_movie,key = itemgetter(1),reverse = True)
        rec_movie = rec_movie[:100]
        random.shuffle(rec_movie) # random shuffle
        return sorted(rec_movie[:12],key = itemgetter(1),reverse = True)

    def recommend_name(self,query):
        # can reduce the names dataset
        # how ? get all the movies that person is famous for
        # now , if the average of the weighted average of the movies
        # he is famous for is less than 6, remove him, YES! can reduce my time then
        '''
        Recommend movie based on actor/director/actress name
        '''
        query = query.lower() #transform a bit
        best_match = process.extractOne(query,list(self.names['primaryName']))
        # get the best matching name from the dataset
        query = best_match[0]

        # get the movies he/she is famous for
        df = self.names.loc[self.names['primaryName'] == query]
        movie_id = list(df['knownForTitles']) # get movie ids for person

        # make ids list of movies
        ids = []
        for k in movie_id:
            m = k.split(",")
            for i in m:
                ids.append(i)

        # got ids , now get movie names
        names = []
        for i in self.movies.index:
            t = self.movies['tconst'][i]
            if t in ids:
                names.append(self.movies['primaryTitle'][i])
        a = pd.DataFrame(columns=['primaryTitle','weight_average'])
        for n in names:
            a = a.append(self.recommend_movie(n)[:4])
        res = a.sort_values(by="weight_average",ascending = False).reset_index().drop("index",axis=1)
        res = list(res['primaryTitle'])
        random.shuffle(res)
        res = names + res # obviously include the movies the person is famous for
        return res[:15]

    def recommend_movie(self,query,type = None):
        ''' Recommend movie on the basis of movie only...'''
        query = query.lower()
        query = query.replace(" ","")
        query = query.replace("\"","")
        query = query.replace("\'","")
        for k in ".:!?&-":
            query = query.replace(k,"")
        if query not in self.movie_dict:
            # calculate the levenshtein distance and get the most similar
            # sounding movie name out of your movie list
            # rapid fuzz is amazingggggg
            best_match = process.extractOne(query,self.movie_dict.keys())
            query = best_match[0]

        # found the movie in the movie dictionary
        ind = self.movie_dict[query]
        sim = self.cosine[ind] #similarity
        ratings = list(self.movies['weight_average'])# ratings
        count = 0
        res = []
        for i,k in zip(sim,ratings):
            if(i!=1):
                res.append([count,i*k])
            count+=1
        res = sorted(res,key=itemgetter(1),reverse= True)
        res = res[:15]
        random.shuffle(res)
        d={}
        for k in res:
            I = k[0]
            d[I] = self.movies.iloc[I]
        df = pd.DataFrame.from_dict(d,orient="index",columns = self.movies.columns)
        df = df[['primaryTitle','weight_average']]
        if(type=='json'):
            df = list(df['primaryTitle'])
            return df
        else:
            return df.reset_index().drop("index",axis=1)
    def recommend_default(self):
        ''' Returns a random 15 recommendations out of the top 100
        movies in the dataset'''
        movie = self.movies[:150]
        movie = list(movie['primaryTitle'])
        random.shuffle(movie)
        return movie[:15]
    def get_recommendations(self,query= None):
        Type = self.determine_query(query)
        print(Type)
        if(Type is None):
            return self.recommend_default()
        if Type == 'Genre':
            return self.recommend_genre(query)
        elif Type == 'Name':
            return self.recommend_name(query)
        else:
            return self.recommend_movie(query,type = 'json')
