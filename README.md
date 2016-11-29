# driverThreading
Version Control of creation of parallelization of a serial processor

11/14/16 Update; Within the repository contains two driver files, the first being a serial processor, the second is the same processor which has been multithreaded using the python library Dask. In each of the two, we use time as our concrete benchmark to measure the difference in performance. When running the serial processor, the run time is around 80-85 seconds, depending on each run. The serial processor will go through each super nova attempt one at a time, starting the next when the previous finishes. The multithreaded one however will process all three supernova's at the same time, this causes the run time to be equal to the longest super nova. 

11/14/16 Update Part2; We've also added in the functionality of automatically being able to run the program without constantly changing the location of your directory.



11/29/16 Update; After this step was well developed we focused on the removal of hard coding the amount of super nova processed. Originally our program would process super nova based on however many we added to our program, this however was inefficient for hard testing and for practical use. The group took some time to brain storm a way to remove the hard coded super novae, and realized that adding the functionality of a range (of super novae to be processed) would not only allow for wide spread testing, but also demonstrate use cases. Originally, we thought of implementing a for loop as a means to cycle through the data we wanted, however it quickly became obvious that this would slow down the run time of our processor, fundamentally negating our efforts of creating efficiency. We settled on command line options, implemented in python, as a means to intuitively and unobtrusively allow for the user to process a desired amount of super novae. 
