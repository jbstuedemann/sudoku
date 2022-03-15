# Sudoku Solver

This project uses **OpenCV** and **TensorFlow** to scan images and screenshots for sudoku boards, then solves them using sudoku rules.

### Dependencies

- [TensorFlow](https://www.tensorflow.org/)
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [imutils](https://github.com/PyImageSearch/imutils)
- [mss](https://python-mss.readthedocs.io/)
- [argparse](https://docs.python.org/3/library/argparse.html)

### Usage

There are two main commands: ```--screen``` and ```--image IMAGE```

|Flags |Description
|-- |--
|```-h```/```--help``` | show this help message and exit
|```-s```/```--screen``` | take a screenshot and process it
|```-i IMAGE```/```--image IMAGE``` | use a given image and process it

