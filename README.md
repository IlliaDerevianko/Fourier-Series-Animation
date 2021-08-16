This project takes the idea that the Fourier series can decompose any function into the sum of periodical functions. In the complex plane, this can simply be represented as vectors that rotate at different frequencies.
The whole idea of this project is to read in a SVG file, find the length of these vectors and their initial direction and then animate it. As they all rotate, the last vector traces the approximate path of the closed curve from this SVG file.

The language used is Python. For numerical computation, no other modules that 'math' are used so everything is done from scratch. For animations I used 'tkinter' as it is simple enough and sufficient for the task.

The project does not aim to be able to read any SVG file. As there are many variations of valid formats used in SVG files, it is difficult to cover all the possible cases. This program does work with the portrait of Fourier himself. Source: https://www.dropbox.com/s/tnim0el257lfzom/Biocinematics_Fourier_Vector.svg?dl=0

There is still a bunch of improvements that can be done. Developing the file reader function, improving the performance by utilising optimised libraries, adding user interface and interaction
