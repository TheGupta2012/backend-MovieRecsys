# backend-MovieRecsys
:large_orange_diamond: This is the application involving the query processing for a Movie and Series Recommendation System.

## BASIS
- Count Vectorization and cosine similarities among the dataset 
- Used sklearn text processing functions and 
## **QUERY STRUCTURE** :point_down:
> BASE LINK : https://movie-recsys.herokuapp.com/movie?query=

  - The *query* parameter present in the link serves as the link to the API 
  - Any query is written after the *=* sign. 
  - Ensure there is **no space** between **query and =** as it is reserved for generating default recommendations.
  - "https://movie-recsys.herokuapp.com/movie?query=ShahRukhKhan"

- You may type any actor, actress, movie or genre to get recommendations for similar movies or series
- The query doesn't really have to be absolutely correct, Leo Di Caprio also works for Leonardo Di Caprio 
- :sparkles: See for yourself - [Leo](https://movie-recsys.herokuapp.com/movie?query=LeoDicaprio) and [Leonardo](https://movie-recsys.herokuapp.com/movie?query=LeonardodiCaprio) (obviously some randomization in results to make it fun!)
- EXAMPLES
  - *Getting recommendations similar to Interstellar* : [Interstellar](https://movie-recsys.herokuapp.com/movie?query=Interstellar)
  - *Getting recommendations similar to Movies of Christopher Nolan* : [Christopher Nolan](https://movie-recsys.herokuapp.com/movie?query=ChristopherNolan)
  - *Getting recommendations for thriller movies* : [Thriller](https://movie-recsys.herokuapp.com/movie?query=thriller)


### :construction: To - Do 
  - Make a website accessing this API for recommendations 
  - Use an Image API to fetch recommendation images and display on website
  - **SOME TWISTS IMINENT** :wave:

