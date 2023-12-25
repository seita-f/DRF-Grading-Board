# Why I made this app?
As a university student, I always wish if I could know how the course I want to register looks and professor's reputation so that I could make the best decision in terms of choosing elective courses / professors.
That is why I created this app by adding features that I thought would be nice to have. Besides that, I have learned React in University and wanted to integrate it with Django.


# So what is this app?
After user authorization, each user can make a thread and grade class/professor between 0 to 5 and write its reputations. Another user basically can find a thread in main timeline or using seaching bar.
They also can write comment and grade in its theread as well. 


## Build With

### Environment
- Mac OS
- Atom

### Back-end 
- Django & Django Rest Framework <br>
  (Swagger)
- Python 3.11.0 venv
  
### Front-end (Currently working on this part)
- React
- Bootstrap

## Database Diagram


## Endpoints
| API | endpoint | HTTP Method | Description |
| --- | --- | --- | --- |
| **USER API** | `/user/create` | POST | register a new user |
| | `/user/token` | POST | create a new token |
| | `/user/me` | PATCH | update a profile |
| **POST API** | `/posts/` | GET| list all posts |
| | | POST | create a post |
| | `/posts/<id>` | GET | view details of post |
| | | PUT/PATCH | update post |
| | | DELETE | delete post |



## Screenshot (Version 1.0)


## Getting Started

```
# activate virtual env (mac)
$ source env/bin/activate

# or install requirments.txt
$ pip install -r requirements.txt

# run server
$ python manage.py runserver

# run test
$ python manage.py test
```

## Author
Seita Fujiwara 2023
