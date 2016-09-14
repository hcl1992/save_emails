# save_emails

Task: 
to program a simple web application that is able to serve a POST endpoint. The main function of the endpoint is to store in the database an email for a particular group of recipients. The emails are then to be sent automatically at a later time.

part 1:
The endpoint should be a POST endpoint with these specs:

It should take 3 parameters:

1) event_id: id of the event. Integer type data. E.g: 1, 2, 12, 24

2) email_subject: subject of the email. String data type. E.g: “Email Subject”.

3) email_content : body of the email. String data type. E.g: “Email Body”.

timestamp: date and time of which the email should be sent. String data type. To be stored as a timestamp object in the database that you are using. E.g: “15 Dec 2015 23:12”

Emails should be saved in a database, for which one can come up with his own schema

part 2:
Emails saved should be executed according to the timestamp saved

with reference to 

http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
http://blog.miguelgrinberg.com/post/using-celery-with-flask 
http://www.cucumbertown.com/craft/scheduling-morning-emails-with-django-and-celery/
 
 1. Create a RESTful API with Python and Flask
 2. use celery to auto send the emails when a time is hit
 
 
