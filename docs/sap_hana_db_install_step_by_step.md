# Prepare the environment
This section outlines the preparation required to set up a VM that is ready to host a HANA DB. 

## Terraform provisioning
* Spin up an EC2 instance with SUSE Linux Enterprise Server 15 SP3.  
* Ensure AWS SSM Agent is installed and running. 
* The EC2 instance needs to have an instance profile allowing Session Manager activities. SAP doesn't support all instance types availabe in AWS checkout the documentation and ensure using a supported one.
* Apply 4 additional EBS volumes of type GP3 (size: tbd)

### Security Group(s)
Attach an AWS Security Group allowing required traffic and follows least privilege principle:  

| Source        | Destination  | Protocol | Port | Comments                       |
|---------------|--------------|----------|------|--------------------------------|
| 172.30.0.0/16 | SUSE HANA DB | TCP      | 22   | Connection from Sandbox Server |
|               |              |          |      |                                |
|               |              |          |      |                                |
|               |              |          |      |                                |

## Configuration Management via Ansible
Once all AWS resources are provisioned, we continue to configure the server via Ansible. 

###  Apply recommended OS ssettings as per [SAP Note 2684254](https://sapphire365.sharepoint.com/:b:/r/sites/SapphireBeyondProgramme/Shared%20Documents/Automation/SAP%20Note%202684254.pdf?csf=1&web=1&e=ejeWi2) 

<u>Remarks</u>  
AWS Launchwizard for SAP ships a Python script to prepare the OS. Convert this script to Ansible and ensure following packages are installed:  

* rpm-build
* libssh2-1
* insserv
* bc
* firewalld
* nfs-kernel-server
* libxml2-tools
* xmlstarlet
* libcap-progs
* libltdl.so.7
* python3-cryptography
* tk
* libicu69
* vnc
* libgthread-2_0-0
* acl
* libicu60_2
* samba
* openssl
* python2-pyOpenSSL

### Data volumes required by SAP HANA
Create mountpoints  
- /usr/sap
- /hana/data
- /hana/shared
- /hana/log

and mount the 4 additional volumes. Ensure they are added to `/etc/fstab` to survive reboots (replace UUIDs):

```
UUID="e8423b46-763b-425c-b905-087df03e4717" /usr/sap xfs defaults,nofail 0 2
UUID="cf4fa927-fb78-4c25-b0d7-89cf3952500a" /hana/log xfs defaults,nofail 0 2
UUID="d9094f4d-623e-422a-9feb-364d4900a30c" /hana/data xfs defaults,nofail 0 2
UUID="34d53699-8971-4746-b13f-80cadfd248b6" /mnt ext4 defaults,nofail 0 2
UUID="740dc474-39f7-49f1-9706-0793ffc3a861" /hana/shared xfs defaults,nofail 0 2 
```

### Download Installation Media
S3 Bucket that holds the media: 
* s3://${AWS_ACCT}-test-bucket/B1_client/
* s3://${AWS_ACCT}-test-bucket/hana_setup/

**Ensure binaries are executable (`chmod 755 <file>`)**

# Install SAP HANA version for B1
This section describes the installation of the HANA DB. We use the installation media from from `s3://${AWS_ACCT}-test-bucket/hana_setup/`. 

## Populate property files required for silent installation mode (Config Management via Ansible ) 
The silent installation mode requires two files being populated: 
- **hdblcm.cfg** (Refer to the blueprint created on Wednesday 3rd of August) Adapt the following settings as per customer requirements
  * hostname
  * max_mem (90% of total mem)
  * SID (to be discussed)
- **hdblcm.cfg.xml** containing 3 passwords

## Install of HANA DB
from the install media directory run 

``` 
./DATA_UNITS/SAP HANA DATABASE 2.0 FOR B1/LINX64SUSE/SAP_HANA_DATABASE/hdblcm 
cat /mnt/hdblcm.cfg.xml | ./DATA_UNITS/SAP HANA DATABASE 2.0 FOR B1/LINX64SUSE/SAP_HANA_DATABASE/hdblcm --ignore=check_signature_file --read_password_from_stdin=xml --configfile=/mnt/hdblcm.cfg -b
```
Once the installer finishes it may print a result suggesting that the installation finished with warnings. Those warnings are expected and be ignored. 

## Post installations steps:
Activate script server
```
hdbsql -u SYSTEM -d SYSTEMDB -I /mnt/scriptserver.txt -p <password_system_user>
```
Add B1ADMIN user and grant permissions
```
hdbsql -u SYSTEM -d NDB -I /mnt/B1ADMIN_create.txt -p <password_system_user>
```

Validate installation: 
as user ndbadm run `HDB info`. The output should read like this: 

``` 
USER          PID     PPID  %CPU        VSZ        RSS COMMAND
ndbadm      21615    21614   0.6      20004       6884 -sh
ndbadm      21723    21615   0.0      14388       3852  \_ /bin/sh /usr/sap/NDB/HDB00/HDB info
ndbadm      21756    21723   0.0      38052       3848      \_ ps fx -U ndbadm -o user:8,pid:8,ppid:8,pcpu:5,vsz:10,rss:10,args
ndbadm       5609        1   0.0     715684      52684 hdbrsutil  --start --port 30003 --volume 3 --volumesuffix mnt00001/hdb00003.00003 --identifier 1659520241
ndbadm       5279        1   0.0     715628      52544 hdbrsutil  --start --port 30001 --volume 1 --volumesuffix mnt00001/hdb00001 --identifier 1659520206
ndbadm       5147        1   0.0      23524       3132 sapstart pf=/hana/shared/NDB/profile/NDB_HDB00_saphanat01
ndbadm       5154     5147   0.0     460148      72064  \_ /usr/sap/NDB/HDB00/saphanat01/trace/hdb.sapNDB_HDB00 -d -nw -f /usr/sap/NDB/HDB00/saphanat01/daemon.ini pf=/usr/sap/NDB/SYS/profile/NDB_HDB00_saphanat01
ndbadm       5174     5154   8.8    8935872    5822768      \_ hdbnameserver
ndbadm       5367     5154   0.2     455308     132424      \_ hdbcompileserver
ndbadm       5370     5154  77.9     987100     412904      \_ hdbpreprocessor
ndbadm       5416     5154  10.8    9108404    6063704      \_ hdbindexserver -port 30003
ndbadm       5419     5154   0.9    3702752    1205268      \_ hdbxsengine -port 30007
ndbadm       5831     5154   0.3    2374888     411672      \_ hdbwebdispatcher
ndbadm       9643     5154   1.0    3491316    1150996      \_ hdbscriptserver -port 30004
ndbadm       5046        1   0.0     502488      31600 /usr/sap/NDB/HDB00/exe/sapstartsrv pf=/hana/shared/NDB/profile/NDB_HDB00_saphanat01 -D -u ndbadm
```

## Install HANA Client
> SAP HANA provides client interfaces for connecting applications in the SAP HANA client software package. The SAP HANA client can be installed on UNIX/Linux and Microsoft Windows operating systems, and on an SAP HANA server host during server installation.

From the install media run:

```{bash}
./DATA_UNITS/SAP HANA CLIENT 2.0 FOR B1/LINX64SUSE/SAP_HANA_CLIENT/hdbinst --path=/usr/sap/hdbclient
```

## Install Application Function Library (AFL)
>You can dramatically increase performance by executing complex computations in the database instead of at the application sever level. SAP HANA provides several techniques to move application logic into the database, and one of the most important is the use of application functions. Application functions are like database procedures written in C++ and called from outside to perform data intensive and complex operations. 

From the install media run:

```{bash}
./DATA_UNITS/SAP HANA AFL 2.0 FOR B1/LINX64SUSE/SAP_HANA_AFL/hdbinst --sid=NBD
```



