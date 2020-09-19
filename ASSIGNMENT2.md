### Added `MemoryRepository`

- The combination of `(title, year)` was used to identify a unique movie from the first assignment, thus I added `id` field to `Movie` to represent this combination, also make the comparison case insensitive
- The methods of `get_first_movie` and `get_last_movie` share some common code, thus I factored out a private method called `_get_movie_by_idx` to re-use the code
- Also added `delete_movie` function to the repo
- Added unit tests for `MemoryRepository`

### Added `/movies` endpoint

- This is the url for listing all movies, each page will desplay 5 movies
- The blueprint is under `movie/movie/movie.py`
