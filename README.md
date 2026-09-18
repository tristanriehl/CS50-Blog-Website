# CS50 Blog
#### Description:
Built as a CS50 final project, this Flask and SQLite application is a full-stack message board where users can post and share articles. The backend utilizes dynamic Flask routing to pull post data from a database and render individual Jinja pages for each article. Adapting design patterns from CS50 Finance and transitioning to native database libraries provided a rewarding hands-on foundation for future web development.

## Features

- **User Authentication**:
  - Secure user registration and login system with password hashing.
  - Password change functionality on the Account page.
- **Main Feed**:
  - Displays all user posts in reverse chronological order (most recent first).
  - Publicly viewable without requiring an account.
- **Post Creation**:
  - A dedicated Create page where authenticated users can draft and submit posts.
  - Input validation to ensure posts are not empty.
- **My Articles**:
  - A personalized dashboard where users can view all their posts.
  - Option to delete individual posts.
- **Responsive Design**:
  - Mobile-friendly layout adapted from CS50's Finance problem set UI.
- **Database Management**:
  - SQLite database to store user accounts and posts.
  - Efficient queries to retrieve and display data dynamically.

## Technologies Used

- **Python/Flask**: Backend framework for routing, handling requests, and rendering templates.
- **SQLite**: Database for storing user accounts and posts, transitioned from CS50’s SQL library to the standard SQLite library.
- **HTML/CSS**: Frontend structure and styling, with responsive design inspired by CS50’s Finance problem set.
- **JavaScript**: Client-side interactivity for form validation and dynamic updates.
- **Jinja2**: Templating engine for rendering dynamic content in HTML.
- **Bootstrap**: Used for responsive UI components and layout (if applicable).

## Installation and Setup

- git clone https://github.com/tristanriehl/CS50-Blog-Website.git
- pip install -r requirements.txt
- flask run
    
prerequisites:
    python 3.8+

## Potentially Future Additions

- Commenting on posts
- Editing your posts
- Adding different categories and filters so that people can look at their specific interests
- A search function

## Credits

- I reused the UI design from the CS50 finance problem set.
- I addtionaly used Claude AI to help me switch over from the CS50 library for Sqlite to Python’s built in Sqlite3 library.
