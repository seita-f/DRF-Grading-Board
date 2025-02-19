# Why I made this app?
As a university student, I always wish if I could know how the course I want to register looks and professor's reputation so that I could make the best decision in terms of choosing elective courses / professors.
That is why I created this app by adding features that I thought would be nice to have. Besides that, I have learned React in University and wanted to integrate it with Django.


# So what is this app?
After user authorization, each user can make a thread and rate school/faculty/class/professor between 1 to 5 and write its reputations. Another user basically can find a thread in main timeline or using filter.
They also can write comment in its theread as well. 


## Build With
### Back-end 
- Django & Django Rest Framework <br>
- Swagger
- Python 3.11.0 

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

## Getting Started & Brief introduction

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
    1. Open `POST /api/user/create` and click on the "Try it out" button.
    2. Fill in the required account information in the provided fields.
    3. Click the "Execute" button to submit the request and create a new user.
![Screen Shot 2023-12-30 at 17 43 37](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/4a7f6f3f-cb6d-4e0d-8383-20a3de06d604)


2. Token Auth 
    1. Open `POST api/user/token` and fill in the required account information
    2. Copy the provided token
   ![Screen Shot 2023-12-30 at 17 50 47](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/605fa237-2946-4ff2-9717-aa0e0c2e80a3)
   ![Screen Shot 2023-12-30 at 17 51 00](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/879683d3-db07-4e82-a14e-89909d121373)
    3. Click authorize button (Top Right of the Main Page), put `Token <copied token>` and click Authorize button.
  ![Screen Shot 2023-12-30 at 17 53 04](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/bb02a970-78f8-4c77-acc8-8cb795959e7e)


3. Make a post
    1. Open `POST api/post/` and fill in the required info for a post (For now, we have to pass primary key for shcool, faculty, class and professor.) and click execute button.
    ![Screen Shot 2023-12-30 at 18 20 45](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/12fcdf2c-6751-4780-93bf-375e3c031891)

    2. We can check created post executing GET api/post (add filter or blank)
  ![Screen Shot 2023-12-30 at 18 29 57](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/6c09c737-674d-4b06-9150-ccc2dfeb5f55)
  ![Screen Shot 2023-12-30 at 18 29 41](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/18525342-01d0-4894-9089-2d15e1dfb1f6)
 
<br>
(Auth user only can edit and delete his own post)
<br>
4. Make a comment
    1. Open `POST api/post/{id}/comment/`, pass post id, fill in the required info for a comment, and execute.
![Screen Shot 2023-12-30 at 18 33 28](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/01d3d8a9-1f28-4d28-ae86-61c3d6403fe1)

    2. We can check all comments in a certain post by executing `GET api/post/{id}/comment`
![Screen Shot 2023-12-30 at 18 34 48](https://github.com/seita-f/Grading-Board-DRF-React/assets/128184233/0695a8f8-cf6f-4e18-b7d9-266d3b030f43)
<br>
(Auth user only can fix and delete his own comment)


## Author
Seita Fujiwara 2023
