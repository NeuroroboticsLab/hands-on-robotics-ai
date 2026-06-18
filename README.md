# Hands-on Robotics and AI: A School-Integrated Internship

This repository serves as the supplementary material for the research paper **"Hands-on Robotics and AI: A School-Integrated Internship"**. 

 * Schindler B., Lange S., Röhrbein F.: **Hands-on Robotics and AI: A School-Integrated Internship**. Proc. of Intl. Conf. on Robotics in Education (RiE). 2026. To Appear.

The repository contains the specific code templates, teaching instructions, and example solutions used in the internship curriculum for Grades 7–10.



## Further Reading and Teaching Material

Detailed documentation of the internship presentation, along with supplementary information and resources, can be found in the [documentation](doc/readme.md).

## Setup on Ubuntu (One-Time Preparation)

To program AVRs in Linux, you will need the free avr-gcc compiler, avr-libc, AVRDUDE, and other associated tools. Ubuntu users can get the required software by running:

`sudo apt-get install gcc-avr avr-libc avrdude build-essential`

Next, you should download the sources and prepare additional libraries:

* Download this [git repository](https://github.com/NeuroroboticsLab/hands-on-robotics-ai) to your system. 
* Open a Terminal and navigate into the `src` folder.
* *Additional libraries for the 3Pi Robot from Pololu are necessary. For this, there are two possibilities: 1) system-wide installation, or 2) local usage. We follow the 2nd approach. If you want instead a system-wide install, follow the [official documentation](https://www.pololu.com/docs/0J51/4).*
* The latest version of `libpololu-avr` should be downloaded from GitHub:
  ```bash 
    wget https://github.com/pololu/libpololu-avr/archive/refs/tags/151002.zip
  ```
* Then, extract it within our `src` direcory by:
  ```bash 
    unzip 151002.zip
  ```
* Replace the library's `Makefile` with the custom one (which is inside the `src`), which only compiles parts of it relevant to the 3Pi-Robot and installs the libs only into our project folder:
  ```bash 
    cp Makefile.libpololu libpololu-avr-151002/Makefile
  ```
* Now, change into the folder, compile and install the library locally:
  ```bash 
    cd libpololu-avr-151002
    make
    make install
  ```
* This will create the `include` and `lib` folder in the `src` directory. Now test it by going into the `3pi-Line` directory and compile:
  ```bash 
    cd ../3pi-Line; make
  ```

## Building and Flashing of Code

The programming port of the Pololu robots should be `/dev/ttyACM0`. After connecting the robot, you should see at least one virtual COM port available by typing `ls /dev/ttyACM*` in a terminal.

To start any program on the Pololu robot, you need to go to the src/{Wanted Task} folder you want to start. Inside open a Terminal and type `make program`. This will compile and send the code to the robot. The robot needs to be connected to the runing system and turned on.

## Task Modules and Example Projects

* [Line Following](src/3pi-Line/readme.md)
* [Maze Task](src/3pi-Maze/readme.md)
* ["Fun and Explore"](src/Fun_and_Explore/readme.md)

> :warning:
Some programs may fail to initialize the `motor_speed` variable, potentially causing it to be unset. As a result, the robot may start moving unexpectedly or without intentional command. To prevent this behavior, ensure that all motor speed values are properly initialized before use.