# AutomationTest111

Pre-Requisites to perform this operation:
1. Install python in ur endpoint and use Visual Studio to view thede and for better coding experience
2. Install MonogDB Compass to view the parsed log results in the endpoint and MongoDB server must running in the background
----> To start mongoDB server
       Create an empty directory in home path — mkdir -p ~/data/db
       Ensure MongoDB can access the directory: —chmod -R 775 ~/data/db
       Start MongoDB with Custom dbpath : — mongod --dbpath ~/data/db. It will starts mongoDB server
3. Ensure that "TOOL_PATH = "/Users/abht/Desktop/LogDecrypter/Mac" -this path as decrypter tool {ex: LogDecrypter} -for Mac
   For Windows - "TOOL_PATH = "/Users/abht/Desktop/LogDecrypter/Windows" {Ex: LogDecrypter.exe}
3. Run the abhi.py file {python abhi.py} - It should run without any error
   then it will generate one link {ex: http://127.0.0.1:5000} 
4. Copy this link in browser and it will open UI. 
5. Go to Upload log file section and upload any encrypted log file with extension (.log).
6. Results table will be fetched in results section.