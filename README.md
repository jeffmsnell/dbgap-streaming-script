# dbgap-streaming-script  
Python 3 script to pull a stream of large files from one remote server to another where:   
1. the remote servers cannot directly communicate with one another  
2. the cumulative size of files is greater than local storage  


User should define initial variables (remote and local dirs, hostname, username, passwords, etc) and create list of files in remote directory.  

1. Paramiko transfers files from user defined remote to local directory 
2. Aspera is the dbgap transfer method of choice and the script handles it as follows:  
a. Aspera script to transfer from local directory to dbgap is created  
b. Aspera script executed  
3. Local file and script are deleted  
4. A few housekeeping items are performed 

