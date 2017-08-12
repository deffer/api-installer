# API installer module

## Description

This module provides script and template to be used when new java API needs to be deployed to API box. Once this module is installed on the target system (API box), it can be used as following:

    sudo api-install my-api-name "My API desciption"
 
This should prepare an environment for new API (create users and groups, folders and template script for running jar files). It is also used to list installed APIs and their status - running or not, and the port. 

    sudo api-install list

Once API is "installed", deployment is as simple as copying a jar into `/usr/share/apis/my-api-name/` and running

    sudo systemctl start my-api-name
	
Logs can be found at

    /var/log/apis/my-api-name

### Monitoring
	
An extra cron job is also configured durin installation. The job is dumping all API statuses into a file every minute. This file is then serverd by nginx
at `/status` with the example configuration below (at the bottom):

    server {
      listen 8000;
      server_name  localhost;
      port_in_redirect off;
      
      location / {
         root /usr/share/nginx/html;
         index index.html;
      }
      
      location /ping {
        return 200 'gangnam style!';
        # because default content-type is application/octet-stream,
        # browser will offer to "save the file"...
        # if you want to see reply in browser, uncomment next line
        add_header Content-Type text/plain;
      }
        
       location /status {
        alias /var/apiservices/status;
        add_header Content-Type text/plain;
      }
    }

## Installing this module

The Jenkins job is configured to release and install new version of this library to all three environments on demand.

### How installation works

Under the hood, Jenkins will generate an *rpm* and upload it to a yum repository. The package will then be installed:  

    sudo yum --enablerepo REPO_NAME install api-installer

### Troubleshooting problems with installation
    
If REPO_NAME is unavailable, install manually by running

    sudo yum localinstall api-installer-0.9-1.noarch.rpm

To build rpm from sources, following instructions below.

Ensure you have an rpmbuild structure in your home folder as described [here](https://wiki.centos.org/HowTos/SetupRpmBuildEnvironment).
Copy `api.installer.spec` into SPECS folder.
Copy `api-install` and `api.initd.template` into SOURCES folder.

    cd rpmbuild
	rpmbuild --define 'BUILD_NUMBER '$BUILD_NUMBER -ba -D "version 0.12" ./SPECS/api.installer.spec

    
Produced rpm file can be installed locally as per instructions above.

As quick solution, you can also coopy everything manually:
Create folder `/etc/api-installer` and copy `api-install` and `api.initd.template` into it as *root:root 755*
Add link to `api-install` so that its available in sudo PATH.