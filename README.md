# dbgap-streaming-script  
Python 3 script to pull a stream of large files from one remote server to another where the remote servers cannot directly communicate with one another.  

0a. Initialize parameters (remote and local dirs, hostname, username, passwords, etc)  
0b. Create list of files in remote directory    
1. Paramiko transfers files from user defined remote to local directory  
2a. Aspera script to transfer from local directory to dbgap is created  
2b. Aspera script executed  
3. Local file and script are deleted  
4. A few housekeeping items are performed  

