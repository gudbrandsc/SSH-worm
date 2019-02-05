# SSH worm

## What is SSH worm?
SSH worm is a simple script that tries to brute-force its way into any machine on the same network using SSH. The script contains multiple safeguards to prevent a widespread of the worm, and are designed to brute-force a raspberry pi running Kali Linux for learning purposes. The functionality of the worm can be broken down to 3 simple steps: 

1. Scan the network for IP address and if SSH is running try and bruteforce the login / password 
2. If the worm succeeds, then upload a copy of itself to the host and install required libraries
3. Run the copy, so it can now scan and do (1)-(3) 

### How to use ?
There are a few libraries required to run the script, but they can all be installed using homebrew or pip.
**Required libraries:** 
- Python 
- Netifaces
- Paramiko

 ~~~~ 
 python replicator.py passwords.txt
 ~~~~ 
 ### Safeguards to prevent the widespread
 One of the first safeguards used to prevent widespread of the worm is the range of IP's that are used. Since I already know the IP address of the machine I wanted to connect to I limited the network scan to only 10 different IP's where 1 of them will match the IP of my Rasberry PI. This will not only make my script finish faster, but also prevent the worm from replicating itself onto any machine that in the network that could match any of my username/password combinations.
 
 The second safeguard that I added was the number of username/password combinations. Usually, brute-forcing require a lot of different combinations of common or default combinations. I already knew the username/password combination for my PI, and I did therefore not add a ton more combinations. So if I am so unlucky that any machine other then my Pi is within the IP range the odds of getting the correct username/password combination is very slim. 
 
 One last safeguard that is to be considered is that the worm will execute the script once it is copied over, and will not wait for the machine to connect to any other network. So the worm will only be able to spread on computers withing the same network, and it's simply not possible for a person to switch internet between the file copy and file execution. 
