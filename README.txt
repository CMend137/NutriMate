This is a README file for our Project: NutriMate. 
Below are steps on how to ensure the application is working seamlessly on all devices.
What you will need: 
Visual Studio Code 
Python
Streamlit 
google-generativeai
python-dotenv
pandas
numpy

PLEASE NOTE:
In order for the app to function, you must create a .env file AND you must go on 
Google AI Studio and create a custom API Key. Create the .env file, like so
"GEMINI_API_KEY=[INSERT YOUR KEY HERE WITHOUT BRACKETS OR QUOTATIONS]" 

Once all dependencies are installed, please navigate to app.py and run the following
command on the terminal:
streamlit run app.py


For a much more in-depth installation guide, please refer to instructions below: 
1.) Install Visual Studio Code
2.) Inside Visual Studio Code, make sure you install the latest form of Python. 
3.) Go on GitHub, and download the zip file. Then extract the zip file. (Disregard if Source Code is given)
4.) open the NutriMate file and locate app.py and open it. 
5.) On the top left had side, click File -> Open Folder… -> [Select the NutriMate folder you extracted earlier]
6.) Once you have the files open, you’ll see NutriMate-Main with several files. 
7.) Now that it’s setup, you’re going to need a Google Gemini API Key. Go to any web browser and go to Google AI Studio, sign in using any Google account and create an API Key. Once you have your key, you can name it NutriMate. Make sure it’s the free tier. Copy the key. 
8.) Navigate back to the extracted NutriMate-Main folder via file explorer (not the zipped one) right click anywhere inside of the folder and select New -> Text Document.
9.) Open the text doc. And write this GEMINI_API_KEY=YOUR KEY (replace YOUR KEY with the key from Google AI) 
10.) Save it. Now, close the text file. Right click the text file, select rename and call it .env. Save it.
11.) Now, in file explorer, look at the taskbar above. It should say “View” click it and the select Show -> File Name Extensions. Now, you should see the file we just made called env.txt or something. Rename it and remove .txt so it’s just called “.env” 
12.) Now go back to app.py located in Visual Studio Code (make sure you’re inside app.py, you’ll see it on the left hand side) 
13.) at the very top, click Terminal -> New Terminal. 
14.) You’re going to want to make sure you have all assets installed so, inside the terminal write the following commands (let them install one by one as these are the needed dependencies) 
python -m pip install streamlit
python -m pip install google-generativeai 
python -m pip install python-dotenv 
(it may ask you for an email, just click enter to bypass it)
15.) once everything is installed, back on the terminal you can run one of two things:
streamlit run app.py (this is if you installed it online via the internet)
