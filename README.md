# backend-MovieRecsys
The application involving the query processing for a Movie and Series Recommendation System.

## **QUERY STRUCTURE**
> BASE LINK : https://movie-recsys.herokuapp.com/movie?query=

  - The *query* parameter present in the link serves as the link to the API 
  - Any query is written after the *=* sign. 
  - Ensure there is **no space** between **query and =** as it is reserved for generating default recommendations.
  - "https://movie-recsys.herokuapp.com/movie?query=ShahRukhKhan"

- You may type any actor, actress, movie or genre to get recommendations for similar movies or series
- EXAMPLES
  - *Getting recommendations similar to Interstellar* : [Interstellar](https://movie-recsys.herokuapp.com/movie?query=Interstellar)
  - *Getting recommendations similar to Movies of Christopher Nolan* : [Christopher Nolan](https://movie-recsys.herokuapp.com/movie?query=ChristopherNolan)
  - *Getting recommendations for thriller movies* : [Thriller](https://movie-recsys.herokuapp.com/movie?query=thriller)
