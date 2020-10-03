# CS235 -- Assignment 2

### Functional requirements met
- Browsing movies
    - Able to navigate movie list
    - Properly calculate previous, next, first, and last page
    - For each movie there is a hyperlink to the movie details page, where the review listed as well
- Searching for movies by actor, genre, and director
    - Able to search by either actor, genre, or director
    - Implemented fuzzy search as well (by using editdistance)
- Registering, loging in, and loging out users
    - Able to register for users and login/logout
    - Also able to persist user to disk file, there is a `users.csv` file under both `adapters/datafiles` and `tests/datafiles`
    - Registered users can be load back into memory repo after app restart
- Reviewing movies
    - For registered users, able to review movies
    - Reviews will also be persisted to disk to prevent data lost after app restart
- New cool features
    - Persistence of users and reviews data
    - For review data, the user who reviewed the movie and delete the review in movie details page
    - Users other than the one who put the review wouldn't be able to see the delete button

### Non functional requirements met
- Conformance to the project structure used for sample Flask application
    - The project contains mainly `movie` and `tests`, where all blueprints stay in the `movie` directory
    - Files are organized for each submodule, includes `domainmodel`, `adapters`, `movie`, `home`, `review`, etc.
- User interface
    - CSS was used to style HTML pages
    - Used jinja2 for HTML templating
- Web interface
    - Appropriate definition of entry points
    - Appropreate use of HTTP protocol
- Testing
    - Test cases covered from unit test to integration end to end test
- Application of the Repository Pattern
    - Abtract class of `AbstractRepository` is used as the interface
    - `MemoryRepository` is one concrete implementation for data storage and retrieve
- Use of Blueprint
    - Blueprints are used, include: `movie_bp`, `review_bp`, `auth_bp`
- Authentication
    - Signed cookies and Flask WTForms are used for security