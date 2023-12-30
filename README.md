# Why I made this app?
As a university student, I always wish if I could know how the course I want to register looks and professor's reputation so that I could make the best decision in terms of choosing elective courses / professors.
That is why I created this app by adding features that I thought would be nice to have. Besides that, I have learned React in University and wanted to integrate it with Django.


# So what is this app?
After user authorization, each user can make a thread and rate school/faculty/class/professor between 1 to 5 and write its reputations. Another user basically can find a thread in main timeline or using filter.
They also can write comment in its theread as well. 


## Build With

### Environment
- Mac OS
- Atom (IED)

### Back-end 
- Django & Django Rest Framework <br>
- Swagger
- Python 3.11.0 venv
  
### Front-end (Currently working on this part)
- React
- Bootstrap


## Endpoints
| API | endpoint | HTTP Method | Description |
| --- | --- | --- | --- |
| **USER API** | `/user/create` | POST | register a new user |
| | `/user/token` | POST | create a new token |
| | `/user/me` | GET | get a profile |
| | | PUT / PATCH | update a profile |
| **POST API** | `/post/` | GET| list all posts (+ filter function)|
| | | POST | create a post |
| | `/post/<id>` | GET | view details of post |
| | | PUT / PATCH | update a post |
| | | DELETE | delete a post |
| **COMMENT API** | `/post/<id>/comment` | GET| list all comments in the post |
| | | CREATE | create a new comment in the post |
| | `/post/<id>/comment/<comment_id>` | GET | get the certain comment in the post |
| | | PUT | update the certain comment in the post |
| | | DELETE | delete the certain comment in the post |

## Getting Started & Screenshots

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
Then, go to http://127.0.0.1:8000/api/docs#/

1. Create User
   1. open api/user/create
   2. Click try out
   3. Fill your account info and click execute


1. Token Auth


1. Make a post 


1. Make a comment






## Author
Seita Fujiwara 2023
