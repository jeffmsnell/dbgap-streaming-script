# dbgap-streaming-script  
Python 3 script to pull a stream of large files from one remote server to another where:   
1. the remote servers cannot directly communicate with one another  
2. the cumulative size of files is greater than local storage  


User should define initial variables (remote and local dirs, hostname, username, passwords, etc), create list of files in remote directory, and create public / private keys (link below).    

1. Paramiko transfers files from user defined remote to local directory 
2. Aspera is the dbgap transfer method of choice and the script handles it as follows:  
a. Aspera script to transfer from local directory to dbgap is created  
b. Aspera script executed  
3. Local file and script are deleted  
4. A few housekeeping items are performed 

Additionally, it will be useful to review the dbgap instructions -- the important parts abbreviated here:

Instructions:  
https://www.ncbi.nlm.nih.gov/sra/docs/submitdbgap/  

Private key: ```~/mykey```  
Public key: ```~/mykey.pub```  

Aspera executable: ```~/.aspera/connect/bin/ascp```  

Example aspera command line usage:  
```bash
ascp -i <key file> -Q -l 200m -k 1 <file(s) to transfer> asp-sra@gap-submit.ncbi.nlm.nih.gov:<directory>
```  
Where:  
```<directory>``` is either test or protected  
```<key file>``` is a private key file (full pathname)

Users who will upload a large number of files are recommended to loop over files individually to avoid wildcards in the ascp command. 
An example in Bash would be:  
```bash
for F in ./*.bam
do
ascp -i <key file> -Q -l 200m -k 1 $F asp-sra@gap-submit.ncbi.nlm.nih.gov:<directory>
done
```
 
If a passphrase was used on the private key, an environmental variable can be used to enter the passphrase for each upload in the loop.  
```bash
export ASPERA_SCP_PASS=<passphrase>
```

Example submission command:  
```bash
~/.aspera/connect/bin/ascp -i ~/mykey -Q -l 2000m -k 1 ~/file1.bam asp-sra@gap-submit.ncbi.nlm.nih.gov:/protected
```  
