#!/usr/bin/python3
#title           Blacklist collector in Python
#description     black list in python,
#author          JB
#date            2019 12
#version         wip, adding in the item from the bash ver as time allows
#usage           ./black-list-collection.py
#notes           python 3 had issues importing the modules, useing as installed
#ptyhon_version  installed centos , tested on ARM debian , V2 as installed on the platform
#PS              read the comments...


print("Starting Python IP Black List Collection...")


import os.path
from os import path
import urllib.request
from shutil import copyfile
import datetime
import re

# all the files are named ip dot star

# the listing of urls that publish bl
bl_list="ip.blacklist.sources.txt"

# my temp file
bl_temp="ip.temp.txt"

# output file of IP/SM
bl_collection="ip.subnet.blacklist.txt"

# output of IP only
bl_ip_collection="ip.blacklist.txt"

# ip perm black list
bl_ip_perm="ip.perm.blacklist.txt"

# ip white list perm
wl_ip_perm="ip.perm.whitelist.txt"

# lines from the temp file we did not use
reject="ip.reject_input.txt"

# the date
date_object = datetime.date.today()
# history file names
historysubnet=str(date_object)+ '.'+ bl_collection
historyip=str(date_object)+ '.'+ bl_ip_collection


# try to give useful messages
if os.path.exists(bl_list):
   ## print("I see the bl_list")
   pass
else:
   print("Erroor: I dont see the bl_list exiting. " + bl_list)
   exit()


if os.path.exists(bl_collection):
   # copy append
   with open(bl_collection) as temp1:
      temp1_data = temp1.read()
      temp1.close()

# target file
   with open(historysubnet,'a') as temp2:
     temp2.write(temp1_data)
     temp2.close()

else:
   print("Erroor: I dont see the Bl Sub Collection. Continuing. " + temp1)

if os.path.exists(bl_ip_collection):
   # copy append
   with open(bl_ip_collection) as temp1:
      temp1_data = temp1.read()
      temp1.close()

# target file
   with open(historyip,'a') as temp2:
     temp2.write(temp1_data)
     temp2.close()

else:
   print("Erroor: I dont see the BL IP Collection. Continuing. " + temp1)


# cruch older ip.collection.txt
bll = open(bl_list,'r' )
ipt = open(bl_temp,'w+' )


# basic error message, up to the sysadmin to figure out why
if bll.mode == 'r':
    pass
else:
    print("Unable to open BLL..." + bll_list)


# loop over bl souces and put to a temp file
# loop the urls the try block is for urls that are slow or offline
# ref https://docs.python.org/3.1/howto/urllib2.html
for line in bll:
    # print for run time debug
    ## print(line)
    try:


      u2 = urllib.request.urlopen(line)
      mydata = u2.read()
      mystr = mydata.decode("utf8")
      ## print(mystr)
      ipt.write("%s\n" % (mystr))
      u2.close()


    except:
      pass
# close for line in bll

bll.close()
ipt.close()


# open the ip temp and collections file dic and regex
# the key and value are the same , so IP/SM ==> key ==> value ,
# ipipcd is IP only collection
# ipsmcd is IP/SM collection
# C is collection, D is for dict
ipt = open(bl_temp,'r' )
ipc = open(bl_collection,'w+' )
ipip = open(bl_ip_collection,'w+' )
ipr = open(reject,'w+' )
ipsmcd   = {}
ipipcd   = {}
re_subnet="\d+\.\d+\.\d+\.\d+[/]\d+"
re_ip="^\d+\.\d+\.\d+\.\d+[^/-]"
re_text="[#a-zA-Z]|' +'"
re_iprange=".0[-]"

for line in ipt:
   ## print(line)
   line = line.replace('\n','')
   line = line.replace('\r','')

   if re.search(re_subnet,line):
      ## print "{}".format(line)
      ipsmcd[line] = line
   else:
      pass


   if re.search(re_ip,line):
      # save to IP then sub and save to IP/SM dict
      ## print "IP:{}:".format(line)
      ipipcd[line] = line
      line=re.sub(r'\d+$', '0/24' , line)
      ipsmcd[line] = line
   else:
      pass

   if re.search(re_iprange,line):
      # range ip style re replace range with slash 24 replace from the end of the line
      ## print "IP:{}:".format(line)
      line=re.sub(r'-\d+.\d+.\d+.255$', r'/24', line)
      ## print "FX:{}:".format(line)
      ipsmcd[line] = line
   else:
      pass



   if re.search(re_text,line):
      ipr.write("%s\n" % (line))
      ## print "Info:{}:".format(line)
   else:
      pass


# close the for line in ipt
# some one please tell my why python does not have formal loop close syntax ?

## print("===============")
# save the IP collection and IP/SM collection
for x in ipsmcd:
   ipc.write("%s\n" % (x))
# close the for x in ipsmcd


ipc.close()

for y in ipipcd:
   ipip.write("%s\n" % (y))
# close the for x in ipsmcd


ipip.close()

# append IP block perm
# ref https://docs.python.org/3/tutorial/inputoutput.html
# keep the work in the if block, message if missing , but we still want the work
# fipbp file ip perm black
if os.path.exists(bl_ip_perm):
   # copy append
   with open(bl_ip_perm) as fipbp:
      perm_data = fipbp.read()
      fipbp.close()


   with open(bl_ip_collection,'a') as ipip:
     ipip.write(perm_data)
     ipip.close()

else:
   print("Erroor: I dont see the bl_ip_perm. Continuing." + bl_ip_perm)

# remove perm whitelist items from the IP collection file, not doing perm sub nets at this time, JB
# wl_ip_perm="ip.perm.whitelist.txt"

# Ip collection at this stage has the BL perm appended to the end of the file
# open and laod the ip collection to a dict
if os.path.exists(bl_ip_collection):
   ipip = open(bl_ip_collection,'r' )
   ipipcd   = {}
   for line in ipip:
      ## print(line)
      line = line.replace('\n','')
      line = line.replace('\r','')
      ipipcd[line] = line


# close the for line in ipip loop
   ipip.close()
else:
   print("Erroor in opening IP collection for white list work.")


# open and load the ip white list to a dict
if os.path.exists(wl_ip_perm):
   fwip = open(wl_ip_perm,'r')
   wipcd = {}
   for line in fwip:
      ## print(line)
      line = line.replace('\n','')
      line = line.replace('\r','')
      wipcd[line] = line


# close the for line fwip
   fwip.close()
else:
   print("Erorr in open Ip White list for white list work.")


for line in wipcd:
  ## print(line)
  result = ipipcd.pop(line,None)
  ## print(result)


# save the result to the file as new, shoould have white list items removed.
# We have dict ipipcd and fwipcd at this stage
ipip = open(bl_ip_collection,'w+' )

# write the ipipcd to the ip colelction
for x in ipipcd:
   ipip.write("%s\n" % (x))


ipip.close()



print("The End...")

print("Count of IP subnet collection")
count = len(open(bl_collection).readlines(  ))
print(count)

print("Count of IP collection")
count = len(open(bl_ip_collection).readlines(  ))
print(count)

###############
