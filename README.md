# Tagore
The actual goal of this project is to optimise meeting/call transcript by taking feed from shared content, meeting invite email, chats in the meeting room etc.


Phase I
In this phase of implementation we have tried to cover below
1. Instead of live meeting/call, we have considerd recorded meeting/call
2. Considered screen shared content as the only feed to speech to text engine

Deviation from actual flow:
1. We have used google speech to text engine
2. Used google vision API for OCR


Flow:
User needs to select a meeting from browser - this will download the existing meeting's transcript and audio recording

Click on Optimise transcript on the browser - this will use the meeting's shared content (as image) as feed to speech to text engine and generate optimse transcript.



Environment setup (Mac)
1. clone this repo
2. cd Tagore/
3. Follow this url (https://cloud.google.com/vision/docs/setup) to setup vision API on google. (we dont need the CLI part)
4. Copy downloaded JSON key file in util directoy
5. You should have python3
6. you should have pip3
7. Run "pip install --upgrade google-cloud-vision"
8. Run "pip install --upgrade google-cloud-speech"
9. cd src/OCR 
10. python3 -m venv env
11. source env/bin/activate
12. export GOOGLE_APPLICATION_CREDENTIALS=<<your token path>>

  

Running the server and demo
1. Update src/JS/scripts/env.js with your own BEARER_TOKEN
2. Update src/JS/scripts/env.js
3. Copy the shared content as image file of the meeting (renamed to sample3.png) in resources/images 
4. Run server.py on terminal(find out the local ip which it runs)
5. Run the landingcopy.html on the address listed out afert running server.py for eg: http://[::]:8000/src/JS/landingcopy.html#
6. download location on browser to "Tagore/resources/touchfile"
7. Run src/FileNotification/FileChangeNotification.py on another terminal 

Demo vidcast
  
https://app.vidcast.io/share/093a9ac9-f5e4-42ee-8fd8-9e66ca2685e3

https://app.vidcast.io/share/e7a73fa3-7ced-42d9-8e80-b4537cebf8f3


  
Please share your feedback so that above steps can be reviewed and corrected.
