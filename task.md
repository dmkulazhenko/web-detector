## Software Engineer

In this task, you are required to implement an object detection app that classifies objects from
an input video received by HTTP request.

The video input will be in MP4 format and will be up to 5 seconds.

The app has the following requirements:
1. In a distributed manner - (Multi threads/Multi processes/Multi docker containers
1. Scalable
1. Should be written in Python 3.7+ using flask.

Note: 
- The way the user should send the video is up to your choice (Can be a basic UI/CLI/other)
- Here’s a link to an open-source image detection library with models capable of doing fast image
detection tasks.
https://github.com/facebookresearch/detectron2
- Training the model is not required, and you can use one of the pre-trained models in your
app.
- We recommend using the OpenCV package for video processing.
- For a video input, the app should return an array with the list of objects contained in the video
with their probabilities for each of the frames, as received from the model.
For example:
[[‘dog’: 0.955, ‘cat’: 0.88, ‘person’: 0.99], [‘dog’: 0.925, ‘cat’: 0.74, ‘person’: 0.99], [‘cat’: 0.9, ‘ball’:
0.99]] for a video with 3 frames.

Please attach your code + architecture design for submission.
For any questions feel free to contact me.