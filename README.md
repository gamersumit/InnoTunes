# InnoTune Backend

Welcome to the InnoTune Backend repository! This project is built using Django Rest Framework to support a music application with robust features including role-based user authentication, music uploads by artists, playlist management, and real-time updates using WebSockets.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [API Documentation](#api-documentation)
6. [Screenshots](#screenshots)
7. [Frontend Link](#frontend-link)
8. [Mobile APK](#mobile-apk)
9. [License](#license)

## Introduction

InnoTune is a comprehensive music platform designed to provide an immersive musical experience. It allows artists to upload and manage their music, while users can enjoy listening, creating playlists, and engaging with the community in real-time.

## Features

- **Role-Based Authentication**: Secure login, registration, email verification, and password reset.
- **Artist Features**: Upload and manage music based on genres and albums.
- **User Features**: Listen to music, create playlists, like songs, and manage recently played tracks.
- **Social Features**: Follow and interact with friends, view real-time activities, and manage collaborations.
- **Search Functionality**: Search by artist, song name, album, playlist, and more.
- **Commenting**: Users can comment on songs.
- **Media Management**: Support for audio, video, and images stored using Cloudinary.
- **Real-Time Updates**: Managed using Django Channels and WebSockets.
- **Extensive Documentation**: API documentation using Swagger.

## Technologies Used

- **Backend Framework**: Django Rest Framework
- **Database**: PostgreSQL
- **WebSockets**: Django Channels
- **Media Storage**: Cloudinary
- **Task Scheduling**: Cronjobs
- **API Documentation**: Swagger

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" width="100"/>
  <img src="https://www.postgresql.org/media/img/about/press/elephant.png" alt="PostgreSQL" width="50"/>
  <img src="https://www.vectorlogo.zone/logos/websockets/websockets-icon.svg" alt="WebSockets" width="50"/>
  <img src="https://res.cloudinary.com/cloudinary/image/upload/v1531592180/cloudinary_icon.png" alt="Cloudinary" width="50"/>
  <img src="https://static1.smartbear.co/swagger/media/assets/swagger_logo.svg" alt="Swagger" width="50"/>
</p>

## Tools Used

- **IDE**: Visual Studio Code
- **Version Control**: Git, GitHub, GitDesktop

<p align="center">
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/vscode/vscode.png" alt="VSCode" width="50"/>
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/git/git.png" alt="Git" width="50"/>
  <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="50"/>
  <img src="https://desktop.github.com/images/desktop-icon.svg" alt="GitHub Desktop" width="50"/>
</p>


## Installation

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/innotune-backend.git
    cd innotune-backend
    ```

2. **Set Up Virtual Environment**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Database**
    - Make sure PostgreSQL is installed and running.
    - Create a database and update the `DATABASES` setting in `settings.py`.

5. **Run Migrations**
    ```sh
    python manage.py migrate
    ```

6. **Run the Server**
    ```sh
    python manage.py runserver
    ```

## API Documentation

The API is documented using Swagger. Once the server is running, you can access the documentation at BASE_ENDPOINT.


## Screenshots

Here are some screenshots to give you a visual overview of the InnoTune backend.

<p align="center">
  <img src="screenshots/Screenshot1.png" alt="Screenshot 1" width="200" style="margin: 10px;"/>
  <img src="screenshots/Screenshot2.png" alt="Screenshot 2" width="200" style="margin: 10px;"/>
  <img src="screenshots/Screenshot3.png" alt="Screenshot 3" width="200" style="margin: 10px;"/>
  <img src="screenshots/Screenshot4.png" alt="Screenshot 4" width="200" style="margin: 10px;"/>
</p>
<p align="center">
  <img src="screenshots/Screenshot5.png" alt="Screenshot 5" width="200" style="margin: 10px;"/>
  <img src="screenshots/Screenshot6.png" alt="Screenshot 6" width="200" style="margin: 10px;"/>
  <img src="screenshots/Screenshot7.png" alt="Screenshot 7" width="200" style="margin: 10px;"/>
  <img src="screenshots/Screenshot8.png" alt="Screenshot 8" width="200" style="margin: 10px;"/>
</p>

## Frontend Link

The frontend of the InnoTune project is handled by another team and can be accessed [here](https://innotune.vercel.app).

## Mobile APK

You can download the InnoTune mobile application APK [here](link-to-your-apk-file).

