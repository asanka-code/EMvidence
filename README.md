# EMvidence

<img src="EMvidence/static/img/logo-with-text.png" align="center" alt="Emvidence Logo" width="800">

## About
EMvidence is a tool that can be used to gather insights from electromagnetic (EM) side-channel emissions of computers. Users can capture EM traces of a device-under-test (DUT) through EMvidence using a software defined radio (SDR) hardware. Additionally, users can upload EM traces that are captured through other means into EMvidence as well. An EM trace can be analysed to gather insights of the DUT by enabling various EMvidence modules. Some EMvidence modules are provided by the developer while users have the freedom to build third-party modules according to their needs.

## Installation
The easiest way to use EMvidence is by downloading a pre-configured VM image and then running it on Oracle Virtual Box. The latest pre-configured images can be found in the following [Google Drive](http://example.com/) folder.
If you are planning to run EMvidence natively on a computer, consider the following instructions.

#### System requirements:
- The computer must have at least 8GB of RAM and sufficient disk space to hold your EM traces.
- We prefer Ubuntu operating system and the instructions assume so. If you are using something else, please check how to install the required packages on your preferred system.
- An Internet connection to download and install required packages.

#### Installing required packages:
1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for Python 3.7, which we need to install other required packages. 
2. Now, open a terminal and run the following commands to install required packages through conda.
```
$ conda install -c ryanvolz gnuradio
$ conda install -c conda-forge weasyprint
```

#### Downloading and running:
```
$ git clone https://github.com/asanka-code/EMvidence.git
$ cd EMvidence/EMvidence/
$ ./start.sh
```
Now, open a web browser and goto the URL http://0.0.0.0:5000/. You can login by using *emvidence* as the username and password.

## Usage
This section is yet to be written. This will be compelted soon.

#### To Do:

- Dashboard should display a summary of data and supported features of the framework.
- Settings page should facilitate adding a new user.
