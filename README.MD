# Social Media API

This Django API provides endpoints for a social media platform that allows users to create posts, follow other users, and comment on posts.

## Requirements

- Python 3.7 or higher
- Django 3.2 or higher
- Django REST framework

## Installation

Clone the repository:

```bash
$ git clone <repository-url>
$ cd social-media-api
```
Create and activate a virtual environment:

```bash
$ python3 -m venv env
$ source env/bin/activate
```
Install the dependencies:

```bash
$ pip install -r requirements.txt
```
Set up the database:

```bash
$ python manage.py migrate
```
Create a superuser:

```bash
$ python manage.py createsuperuser
```
Run the development server:
```bash
$ python manage.py runserver
```
The API should now be running locally at http://127.0.0.1:8000/api/users.

# API Endpoints
```bash
GET /api/users/: Retrieve a list of all users.
GET /api/users/{id}/: Retrieve details of a specific user.
POST /api/users/{id}/follow/{id}: Set the first user as a follower of the second user.
POST /api/users/: Create a new user.
GET /api/posts/: Retrieve a list of all posts with pagination and filters.
GET /api/posts/{id}/: Retrieve details of a specific post with its last three comments included.
POST /api/posts/: Create a new post.
GET /api/posts/{id}/comments/: Retrieve all comments for a specific post.
POST /api/posts/{id}/comments/: Add a new comment to a post.
```
**Note**: *All endpoints require authentication using token-based authentication.*

# Authorization
Token-based authentication is used to authenticate API requests. To authenticate, include the token in the request header.

Token "token-value"
To obtain a token, you can use the Django shell or authenticate through a login endpoint.

To create a token using the Django shell, run the following command:

```bash
$ python manage.py drf_create_token <username>

output:
    python manage.py drf_create_token user1
    Generated token 7baa3db5c2f07f617c87616716e689ca7c6692a8 for user user1
```
**Note**: You can use Postman to authenticate through a create user endpoint. To do so, send a POST request to http://127.0.0.1:8000/api/users with the username, password and followers list (could be an empty list) in the request body. The response will include the token.

# Running Tests:
To run the unit tests for the API endpoints and ORM queries, use the following command:

```bash
$ python manage.py test
```
# Optimization and Performance:
The project includes optimizations such as indexing and constraints on database fields to improve query performance. These optimizations aim to minimize the number of database hits and enhance overall performance.

# Contributing:
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License.