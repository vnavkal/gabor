This repository contains some crude functions to detect lanes in a dashcam video.  It turns a video like [this](https://youtu.be/5v35T_XPGgw) into one that indicates the lane locations, like [this](https://youtu.be/s6d2HTr6qEQ).

Command-line usage:
```
visualize_activations.py [-h] [--frequency FREQUENCY]
                                [--num-frames NUM_FRAMES] --video-path
                                VIDEO_PATH [--num-processes NUM_PROCESSES]
                                [--rescaling-factor RESCALING_FACTOR]

Download YouTube driving video and attempt lane detection

optional arguments:
  -h, --help            show this help message and exit
  --frequency FREQUENCY
                        frequency at which video frames are sampled
  --num-frames NUM_FRAMES
                        number of frames to process
  --video-path VIDEO_PATH
                        path of input video
  --num-processes NUM_PROCESSES
                        number of processes to use for calculating
                        convolutions
  --rescaling-factor RESCALING_FACTOR
                        factor by which to rescale video (choosing a value
                        less than 1 can speed processing)
```
