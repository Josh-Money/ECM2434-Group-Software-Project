# ECM2434

### [Cointributors](contributors-url)

## Gamification of Sustainabilty on Campus

A web app which uses gamification to promote sustainability on campus for students/staff at the University of Exeter<br>

Welcome to our web app, an application designed to help users explore the campus and become sustainable students. Our app offers an engaging, gamified experience that inspires users to explore the campus while learning about sustainable living and ways to positively impact the environment.

Our app allows users to scan QR codes located throughout the campus and complete quizzes and articles which help provide sustainable learning insights into the area where the qr code was found. The users earn points from completeting the quizzes and reading the articles, then they are placed on the app's leaderboard.

Our app features a user-friendly, accessible design with a modern and intuitive interface that promotes engagement and exploration. Whether you're a student, visitor, or staff member, our web app provides a fun and educational way to embrace sustainability.

## Table of Contents

- [Getting Started](#start)
- [Built With](#build)
- [Prerequisites](#preq)
- [Installation](#installation)
- [Testing](#test)
- [Contributing](#contributing)
- [License](#license)

## Getting Started []()

These instructions will allow you to set up the project for development and testing on your local machine.

## Built With []()

- Django
- Bootstrap
- SQL
- Python

## Prerequisites []()

This section includes the software you will need to run the app and how to install it. You will need to install these in the virtual enviroment you are working in.

[Python](https://www.python.org/) you can download this from the website.

Pyzbar

```bash
pip3 install pyzbar
```

OpenCV

```bash
pip3 install opencv-python-headless
```

## Installation []()

Here is a step by step on how to get the developement enviroment working.

1. Clone the repository:

  ```bash
  git clone https://github.com/guy-watson/ecm2434-Group-26/
  ```

2. Change into the project directory:

  ```bash
  cd ecm2434-Group-26/(directory_name)
  ```

3. Create a virtual environment:

  ```bash
  python3 -m venv env
  ```

4. Activate the virtual environment:

  ```bash
  source env/bin/activate # on Linux/MacOS
  env\Scripts\activate.bat # on Windows
  ```

5. Install dependencies:

  ```bash
  pip3 install Django
  pip3 install opencv-python-headless
  pip3 install pyzbar
  ```

6. Run migrations:

  ```bash
  python3 manage.py migrate
  ```

7. Create a superuser. You can login into the site as superuser and then into django admin interface where you can edit the questions and answers for the quizzes.

  ```bash
  python3 manage.py createsuperuser
  ```

8. Run the development server:

  ```bash
  py manage.py runserver
  ```

  At this point you can copy the provided url into your browser to access the website.

To reset the database:

```bash
python3 manage.py flush
```

## Testing []()

To run the inbuilt tests input the following command when in the working directory:

```bash
python3 manage.py test
```

# Initial Contributions []()

## Will Cooke -> [Home page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/home)

## Marcos Vega -> [Artices page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/articles)

## Josh Money -> [Leaderboard page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/leaderboard)

## Tim Mishakov-> [Leaderboard home implementation](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/home)

## Nitzan Lahav -> [Login page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/login)

## Michael Porter -> [Login page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/login)

## Lucas Doyle -> [Profile page](https://github.com/Josh-Money/ECM2434-Group-Software-Project/tree/main/game/profile)

The rest of the details of our contributions are found in the workload unit file and the trello page.

# License[]()

MIT License

Copyright (c) 2023 NAMEEEEEEEEEE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[contributors-url]: https://github.com/Josh-Money/ECM2434-Group-Software-Project/graphs/contributors
