# driverThreading
Version Control of creation of parallelization of a serial processor

11/14/16 Update; Within the repository contains two driver files, the first being a serial processor, the second is the same processor which has been multithreaded using the python library Dask. In each of the two, we use time as our concrete benchmark to measure the difference in performance. When running the serial processor, the run time is around 80-85 seconds, depending on each run. The serial processor will go through each super nova attempt one at a time, starting the next when the previous finishes. The multithreaded one however will process all three supernova's at the same time, this causes the run time to be equal to the longest super nova. 

11/14/16 Update Part2; We've also added in the functionality of automatically being able to run the program without constantly changing the location of your directory.
