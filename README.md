# ECM2434

### [Contributors](https://github.com/Josh-Money/ECM2434-Group-Software-Project/graphs/contributors)

## Gamification of Sustainabilty on Campus

A web app which uses gamification to promote sustainability on campus for students/staff at the University of Exeter.

Welcome to our web app, an application designed to help users explore the campus and become sustainable students. Our app offers an engaging, gamified experience that inspires users to explore the campus while learning about sustainable living and ways to positively impact the environment.

Our app allows users to scan QR codes located throughout the campus and complete quizzes and articles which help provide sustainable learning insights into the area where the qr code was found. The users earn points from completeting the quizzes and reading the articles, then they are placed on the app's leaderboard.

Our app features a user-friendly, accessible design with a modern and intuitive interface that promotes engagement and exploration. Whether you're a student, visitor, or staff member, our web app provides a fun and educational way to embrace sustainability.

## Advanced Features

- Deployed website
- Fully responsive on mobile
- Full admin functionality
- Many features e.g. profiles, leaderboard, qr scans, events page

## Links
- Deployed website: https://ecoquest.pythonanywhere.com/
- Trello: https://trello.com/b/6XgNdnja/project

## Table of Contents

- [Getting Started](#getting-started)
- [Built With](#built-with)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Testing](#testing)
- [Initial Contributions](#initial-contributions)
- [License](#license)

## Getting Started

These instructions will allow you to set up the project for development and testing on your local machine.

## Built With

- Django
- Bootstrap
- SQL
- Python

## Prerequisites

This section includes the software you will need to run the app and how to install it. You will need to install these in the virtual enviroment you are working in.

[Python](https://www.python.org/) you can download this from the website.

## Installation

Here is a step by step on how to get the developement enviroment working.

1. Clone the repository:

  ```bash
  git clone https://github.com/Josh-Money/ECM2434-Group-Software-Project/
  ```

2. Change into the project directory:

  ```bash
  cd ECM2434-Group-Software-Project/game
  ```

3. Create a virtual environment:

  ```bash
  python -m venv env
  ```

4. Activate the virtual environment:

  ```bash
  source env/bin/activate # on Linux/MacOS
  env\Scripts\activate.bat # on Windows
  ```

5. Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

6. Run migrations:

  ```bash
  python manage.py migrate
  ```

7. Create a superuser. You can login into the site as superuser and then into django admin interface.

  ```bash
  python manage.py createsuperuser
  ```

8. Run the development server:

  ```bash
  python manage.py runserver
  ```

  At this point you can go to http://127.0.0.1:8000/ to access the website normally or go to http://127.0.0.1:8000/admin/ to sign into your admin account.

To reset the database:

```bash
python manage.py flush
```

## Testing

### Testing Plan

This section outlines the testing strategy for ensuring the reliability and functionality of the web application. The tests cover unit testing, integration testing, and user acceptance testing.

### 1. Unit Testing  
Unit tests verify the functionality of individual components within the application. The tests focus on models, views, and forms.

- **Run unit tests:**
  ```bash
  python manage.py test

## Initial Contributions

### Will Cooke -> [Home page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/home)

### Marcos Vega -> [Artices page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/articles)

### Josh Money -> [Leaderboard page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/leaderboard)

### Tim Mishakov-> [Leaderboard home implementation](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/home)

### Nitzan Lahav -> [Login page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/login)

### Michael Porter -> [Login page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/login)

### Lucas Doye -> [Profile page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/profile)

The rest of the details of our contributions are found in the workload unit file and the trello page.

## License

MIT License

Copyright (c) 2023 Syntax Squad

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
