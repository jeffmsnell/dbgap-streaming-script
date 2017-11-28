#!/usr/bin/env python3

import paramiko
import os
import time

##########################################################################
remotedir = '/path/to/remote/directory/'
localdir = '/path/to/local/directory/'
hostname = ''
un = 'username'
pw = 'password_remote'
pw_aspera = 'password_aspera'

##########################################################################


arrFiles = ['file1.bam', 'file2.bam', 'file3.bam'] #...


arrUploaded = []
for remotefile in arrFiles:
    if remotefile not in arrUploaded:
        

        #1. get remote file to local:

        time_global_start = time.time()

        try:
            #connect to remote server
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, 
                        username=un,
                        password=pw)
            print('Connected')

            #open ftp connection
            sftp = ssh.open_sftp()

            #logic to get remote files that do not exist on local dir
            try:
                remotefiles = sftp.listdir(remotedir)
                localfiles = os.listdir(localdir)
                if remotefile not in localfiles:
                    print('Getting ' + remotefile + ' ...')
                    time_local_start = time.time()
                    getremote = remotedir + remotefile
                    getlocal = localdir + remotefile
                    sftp.get(getremote, getlocal) #to transfer to remote change to: sftp.put(getlocal,getremote)
                    time_local_stop = time.time()
                    time_local = time_local_stop - time_local_start
                    print('Got ' + remotefile + ' in: %.1fm' %(time_local/60))

            #error handling:
            except IOError:
                print('dir exists not')

            #disconnect:
            ssh.close()
            print('Disconnected')

        #error handling:
        except paramiko.SSHException:
            print("Connection Error")

        #2a. make script to transfer to NIH:
        print('Making ' + remotefile + ' script')
        with open('submission_script.bash', 'w') as f:
            f.write('#!/usr/bin/env bash\n\n')
            f.write('export ASPERA_SCP_PASS=' + pw_aspera + '\n')
            toWrite = '~/.aspera/connect/bin/ascp -i ~/mykey -Q -l 2000m -k 1 ~/' + remotefile + ' asp-sra@gap-submit.ncbi.nlm.nih.gov:/protected'            
            f.write(toWrite)
        os.system('chmod +x submission_script.bash')
        print('Made ' + remotefile + ' script')

        #2b. transfer local file to NIH:
        time_transfer_start = time.time()
        print('Transfering ' + remotefile + ' to NIH...')
        os.system('./submission_script.bash')
        time_transfer_stop = time.time()
        time_transfer = time_transfer_stop - time_transfer_start
        print('Transfered ' + remotefile + ' to NIH in: %.1fm' %(time_transfer/60))

        #3. delete local files:
        print('Deleting ' + remotefile + ' files')
        os.system('rm submission_script.bash')
        os.system('rm ' + remotefile)
        print('Deleted ' + remotefile + ' files')
        
        #4. a few last things
        arrUploaded.append(remotefile)
        time_global_stop = time.time()
        total_time = time_global_stop - time_global_start
        print('Total time for ' + remotefile + ' %.1fm\n' %(total_time/60))
