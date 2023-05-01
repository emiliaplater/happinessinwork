## Table of contents

- [Description](#description)
- [Requirements](#requirements)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)

## Description
An eye centroids detector program is a computer program designed to detect and locate the positions of the centroids of the eyes in a video stream. The centroids are the points that represent the center of each eye. 

The program typically uses computer vision techniques such as image processing, feature detection, and machine learning algorithms to identify the eyes in the input video stream. Once the eyes are detected, the program calculates the centroid coordinates by analyzing the shape, size, and position of the eye regions.

In addition to detecting the centroids of the eyes, some eye centroids detector programs may also provide additional feature such as eye tracking on 3D graphic. This feature can be used for various applications such as driver monitoring systems, virtual reality, and human-computer interaction.

## Technologies
- Python:
> [opencv](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

> [NumPy](https://numpy.org/)

> [matplotlib.pyplot](https://matplotlib.org/stable/gallery/mplot3d/wire3d.html)

> [time](https://docs.python.org/3/library/time.html)

## Getting Started 
Creating a Virtual Environment:

- with Python:
```bash
python -m venv myenv
```
> Activate your virtual environment
```bash
source myenv/bin/activate # Linux
.\myenv\Scripts\activate # Windows 
```
> Install dependencies and add virtual environment to the Python Kernel
```bash
python -m pip install --upgrade pip
pip install ipykernel
python -m ipykernel install --user --name=myenv
```


- with miniconda3:
```bash
conda create -n myenv
conda install -n myenv opencv
conda env export > apple-metal.yml
```
*Do not forget to set the environment (current: myenv) in your IDE*


## Project Structure
- Setup the [environment](#getting-started) and install necessary [libraries](#technologies)

- Read video frames using the OpenCV library

- Select a region of interest (ROI) from the frame where eyes are expected to be present

- Convert the ROI to grayscale and apply Gaussian blur to smooth the image

- Apply a threshold to the grayscale image to create a binary image

- Find contours in the binary image using the [findContours](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga17ed9f5d79ae97bd4c7cf18403e1689a) function of OpenCV [[201]](https://docs.opencv.org/3.4/d0/de3/citelist.html#CITEREF_Suzuki85)

- Sort the contours based on their area in descending order

- Draw circles around the contours with the largest area, which are likely to be the eyes

- Find circles in the binary image using the [Edcircles](https://www.researchgate.net/publication/256822734_EDCircles_A_real-time_circle_detector_with_a_false_detection_control) function of Opencv [[6]](https://docs.opencv.org/3.4/d0/de3/citelist.html#CITEREF_Suzuki85)

- Calculate average coordinates from two algorithms

- Append coordinates for the graphic

- Display the frame with the detected eyes
