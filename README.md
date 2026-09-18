# CS50 Blog
#### Video Demo:  <https://youtu.be/J9W3IzmTEJg>
#### Description:
This project is a blog/message board website. Users can sign up and post whatever they want to the main feed page. This is sort of like a reddit or message board website.
I have always been interested in how these websites were made and before. Thanks to CS50, I now understand the basics of how these websites function. If I ever want to build a big web application one day, it will all be thanks to where it all started, which is CS50.

app.py is where the backend is written. I opted to use some borrowed code from the finance problem set due to it having similar functions to what a basic website needs. This allwed allowed me to focus on making the main changes needed for a blog website. Some of the changes in this process was moving some of the functions from helper.py such as the apology function. Additionaly, what I changed in app.py was that I added all of the functionality of the blog/message board website, such as the functions to create and store the articles.

 One of the challenges I faced however was when a new article was created, I had a hard time creating a new page for that specific article. I then learned that with flask, you can create a new page based off of the article ID. What this function does is that it takes the information of the article which is stored in the sqlite database and adds it to the article jinja template page. This allows me to display the article contents on a new page.

Additionaly, I chose to reuse the Finance problem set's frontend design due to its clean and minimalistic design. It ensures consistent accessibility between all devices without requiring extensive CSS modifications. This allowed me to stay focused on the main intellectually interesting part of the project which was the back end.

Another issue I ran into was moving away from the CS50 library. Moving away from the library was challenging because it meant that I had to learn new syntax but with the help of claude sonnet, I was able to learn and transition away from the CS50 library to understanding the built in sqlite3 database functions. It was very interesting learning how much the CS50 library can simplify the syntax and make the coding more intellectualy interesting rather than spending alot of time worrying about syntax, which was the case for this project.

This project was a rewarding climax of my CS50 journey, allowing me to transform my curiosity about web development into a functional blog/message board. Overcoming challenges like dynamic routing and SQLite transitions taught me the value of leveraging resources like documentation and AI tools to learn and expand my current knowledge. I’m proud of creating a online platform that encourages sharing ideas. This experience has oppened my eyes to how web applications work, and I’m excited to continue exploring new technologies and features.

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

- git clone https://github.com/tristanriehl/
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