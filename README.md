# Magical-Tomcat-Installer
This is the Magical Tomcat Downloader &amp; Installer. Finds and downloads the latest Tomcat binary and also its dependencies (i.e., latest JDK/JRE).

## The Problem
My Organization heavily deploys applications on `Tomcat` servers. We have a fleet of application servers that are Tomcat (plus some other) and it has been so for many many years. Tomcat is reliable and has an active development history. Also, Tomcat is very secure and stable when used in an Enterprise setup. It can handle a good load of traffic and performs very well with proper resource utilization.

So as part of the __Enterprise Infrastructure Team__, our job is to provision more and more Tomcat servers, for deploying the ever
increasing number of applications, both customer facing and internally used ones or even web services, etc.

## Manual Setup
When performing the installation and setup manualy, it takes up a good amount of time and every time we are performing the exact same
set of steps. So, imagine we have to setup 100 such Tomcat instances. Yeah...right, that's gonna take a lot of time.
As part of the setup, we will also need to download and install the appropriate `JDK/JRE` required by the applications to be deployed.

## Automation to the Rescue
To avoid this repetition at work, I came up with an utility that performs the necessary checks and steps without any human intervention
and thus increases productivity by saving time wasted on the process of downloading/installing and setting up the infrastructure part.

All that is required now, is to run this utility with configurations correctly set, because that is what the utility listens to
and let it do its __`magic`__.

No need to manually indulge on doing the same on multiple servers, and thus less prone to human errors and also it enables us to keep
better track of the entire setup process and can be easily standardized across the various towers or domains.

The most important entity that one gains is, it saves a lot of __time__. What manually would have taken ~10-15 mins, can now be done in just a matter of seconds. Time is an important factor in the Enterprise Setup, because __`Time is Money and Money is Time`__.

## How to Use
Most of the customizations can be handled by configuring the settings defined in the configuration files. Please make sure to change the
default values to something that would suit your requirements.
Other than that, the application itself is quite modular and well split. Also, it is made to run cross-platform, one big plus when
you have a node farm comprising of multiple brands of platforms, grouped/clustered together to support the use cases.

The modularity enables you to __plug-and-play__ various combinations of the components, according to your needs. Here, I have provided you
with the library that holds the components of the utility. Its upto you to stitch them together as you see fit.

Also, the code itself is well documented and can be easily understood. I have documented the design decisions taken by me which can be
further optimized accordingly.

## Tasks Made Easy (Infrastructure Perspective)
- [x] Search the latest version of __`Tomcat Binary`__ on the Official Site.
- [x] Download the latest version and save it to disk.
- [x] Get the dependencies downloaded as well.
   - Find the latest `JRE/JDK` version on the Official Site.
   - Download the same and save it to disk.
- [x] Perform the extraction operation on the Downloaded Archived binaries.
- [x] Place the extracted binaries to the appropriate locations.
- [x] \(Optional) Create the Profile files for each of the extracted binaries.

## Tasks Made Easy (Person's Point of View)
- [x] No manual setup required.
- [x] Saves ample time for performing other important infrastrucutre tasks (Automation makes it `Super Fast!!!`).
- [x] Eliminating Human Errors.
- [x] No expertise required t perform the task (i.e., the downloading and extracting of the required binaries).
- [x] More time to relax and chill!!!

## What I Gain?
Well my focus is always on leveraging technology to make work more efficient and less cumbersome. Reducing the complexity and
other human factors was also the motivation behind this. Also, I gained a lot of insight on System Design and being able to decide
on using the appropriate tools for doing the job at hand in an Efficient and Manageable way.
