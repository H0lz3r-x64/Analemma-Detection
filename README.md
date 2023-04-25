# Analemma Detection

## Introduction

This project aims to detect the position of the sun in images. The code uses OpenCV-Python-Utilities library to find the brightest point of an image (sun), displays the steps and returns the center coordinates of the brightest point found. The function uses two methods; the minMax method and the robust method to find the brightest point. They work differently but generally the minMax method is better. The robust method is returned in case it didn't find anything and the distance from the minMax center to the previous center is more than 50px. This avoids the center to be at an entirely different location than the previous center was, which would be wrong. The code also includes a function that writes data to an excel file.

## Usage

The project can be used to detect the position of the sun in images.

## Requirements

The project requires Python 3.x and OpenCV-Python-Utilities library.

## Installation

1. Install Python 3.x.
2. Install OpenCV-Python-Utilities library.
3. Clone this repository.

## Usage

1. Run main.py.
2. The program will read all images from a specified directory.
3. The program will detect the position of the sun in each image.
4. The program will write data to an excel file.

## Conclusion

This project provides a simple way to detect the position of the sun in images using OpenCV-Python-Utilities library. It can be used for various applications such as solar panel tracking, weather forecasting, and more.

## Debug Images

Following images show some steps the program performs on the images.

![image](https://user-images.githubusercontent.com/91200978/231760610-c3ea42e4-1987-4e44-9b98-0983f3243729.png)
![image](https://user-images.githubusercontent.com/91200978/231760727-4a357eed-8829-4d6f-a396-37900bfc887d.png)
![image](https://user-images.githubusercontent.com/91200978/231760816-d33bb884-ac76-4bf7-bb7c-8ef3ff7ed484.png)
