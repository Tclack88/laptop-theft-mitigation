# Laptop Theft Mitigation

## Summary

This is a collection of python and shell scripts which serve as a means to recover a stolen laptop. It has the following features:
- A keylogger
- Webcam capture
- Local Network Scan
- Geolocator (approximate Based on WPS -- wifi equivalent of GPS)

These four tools used in conjunction help locate your stolen laptop as well as gather evidence for the authorities.

Read more detailed explanation and relevant background information [here][#] (link to be added soon)

Written for and tested in Ubuntu (18.04). Other platforms need to be tested.

non-standard python libraries needed:
	selenium		-	pip3 install python3-selenium
	pyxhook			-	pip3 install --user pyxhook
	xvfb			-	apt-get install xvfb  		# frame buffer
	pyvirtualdisplay	-	pip3 install pyvirtualdisplay 	# py3 xvfb wrapper


## Step 1: Create a guest account requiring no password and configure
We want this because we need your thief to be able to log in to computer (triggering the code) and sign into wifi (sending the files)

`sudo adduser guest` 
create temporary password
locate guest in your /etc/shadow file
change it's password from something like 
`guest:$6$m4CpcgBw$i9XLGaUNToClOJ1X5Grug/COUjlkhoPv1:15048:0:99999:7:::`
to
`guest:U6aMy0wojraho:15048:0:99999:7:::`
(ubuntu only solution)

Add guest to sudoers
`usermod -aG sudo guest`

The guest now dangerously can enact sudo commands without a password. If you haven't already, you need to add a root password THEN set the default sudo password to the root password:

`sudo passwd root`

`sudo EDITOR=/usr/bin/vim visudo` (the "EDITOR=..." is optional, but nano sucks)

At the top of the document you will see something like this:
```bash
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

Add the following
`Defaults	rootpw`
and while your at it
`Defaults	editor=/usr/bin/vim` (because nano sucks)

You should have the following at the top, keep everything else the same:

``` bash
Defaults        env_reset
Defaults        editor=/usr/bin/vim
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Defaults        rootpw
```

NOTE: You should definitely do this with visudo instead of editing directly with "sudo vim /etc/sudoers", because if you screw up, you can fix it as the administrator with your administrator password with `pkexec visudo`. For instance, the order of the above is important, change root password before setting Defaults to rootpw... Otherwise you can't perform any root commands ever again on your system

Give the guest passwordless sudo access to iwlist (necessary to get ALL networks in view rather than just the connected one). We do this by adding a file to the /etc/sudoers.d directory.

As root create the file `vim /etc/sudoers.d/iwlist` then add this single line:
`guest   ALL=NOPASSWD:   /sbin/iwlist`


Create the following directories in your guest account:

`/home/guest/bin/.bin/tmp/`
And move the python and shell scripts to the .bin directory. If all goes to play, you should have the following:

```bash 
ls -l /home/guest/bin/.bin/
-rwxr-xr-x 1 guest guest 1721 Jul  1 12:24 geolocation.py
-rwxr-xr-x 1 guest guest 1403 Jul  1 12:24 keylog.py
-rwxr-xr-x 1 guest guest  127 Jul  1 13:42 mailout.sh
-rwxr-xr-x 1 guest guest  163 Jul  1 12:25 network.sh
-rwxr-xr-x 1 guest guest  157 Jul  1 11:19 norobo.sh
drwxrwxr-x 2 guest guest    0 Jul  1 16:29 tmp
-rwxr-xr-x 1 guest guest   92 Jul  1 12:25 wc.sh
```
(See optional extra steps below)

Download the latest chromedriver and put it in the guests ~/bin directory 
(NOT the ~/bin/.bin or the /bin)
make it executable if not already

## Step 2: Configure email from your terminal
You can do this with your current gmail account or create a special one for this.
Regardless, you will need to request a special app password from google. See link below.
Also this will enable you to send mail from your home account, it's not specific to the guest user, only your hostname.

Configure your ssmtp.conf file as follows (example in repo as well)

```bash
root=me@gmail.com               # Your gmail account
mailhub=smtp.gmail.com:587

AuthUser=me                     # This is your gmail address with '@gmail.com' removed

AuthPass=ejkerraevbjyutri       # very important, Don't use your gmail password, 
                                # request a 16 digit google app password here:
                                # https://support.google.com/mail/answer/185833?hl=en
useSTARTTLS=YES
rewriteDomain=gmail

hostname=mylinuxcomputername    # Very important, most online tutorials put gmail.com
                                # here, instead you need your linux hostname
FromLineOverride=YES
```

## Step 3: Set a cronjob 

As guest user, run `crontab -e` and add the following to run the script and send out the file in 30 minute intervals"
```bash
MAILTO=""
*/30 * * * * PATH="$HOME/bin/.bin:$PATH"; export DISPLAY=:0.0; cd ~/bin/.bin ; if [[ $(whoami) == guest ]]; then norobo.sh; fi
```


## Optional extra steps
- Consider changing the names, keylog.py for example may be suspicious for anyone who has heard of a keylogger, etc. Be sure to make the appropriate changes to the master file "norobo.sh"

- You may need to make it obvious to your potential thief that a guest account exists. Ubuntu doesn't display all accounts upon startup.

- Technically the MAILTO="" line in your cronjob is optional because otherwise you will get notifications every half hour to your gmail account even if you're not signed in as guest. If you want this constant reminder or you just don't care because it's not your home account, you may remove this line
