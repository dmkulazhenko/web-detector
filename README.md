# Web-Detector

Web-Detector — RESTful API service for object detection, based on [Detectron2](https://github.com/facebookresearch/detectron2). Web-Detector is a test task for a SWE.

-----

## Deployment

Web-detector designed to run on multiple high-performance nodes, below is an example of using docker-compose to run the web-detector on a single machine, from which you can quite easily understand what is going on.

### Requirements

1. Nvidia GPU (it should be OK with AMD GPU or only CPU, but I'm not sure, tested only on gtx 980ti);
2. [`docker>=20.10.6`](https://www.docker.com/), [`docker-compose>=1.29.1`](https://github.com/docker/compose);
3. [`nvidia-docker-toolkit>=1.3.3`](https://github.com/NVIDIA/nvidia-docker).

Btw, since the project depends very much on the environment and has only been tested on one machine, I will just leave it here:
- Kernel: 5.10.32-1-MANJARO 
- CPU: Intel i7-5930K (12) @ 4.600GHz 
- GPU: NVIDIA GeForce GTX 980 Ti 
- Memory: 15918MiB

##### Possible troubleshooting

> `services.detector_detector.deploy.resources.reservations value Additional properties are not allowed ('devices' was unexpected)`
- Are you sure you installed [`nvidia-docker-toolkit>=1.3.3`](https://github.com/NVIDIA/nvidia-docker)?
- Update docker / docker-compose;
- Comment `deploy` section of `docker-compose.yaml` (lines 68-73);

> `CudeError('Unknown Error') / CudaError('Out of memory') / CudaError('...')`
- Decrease `--autoscale` of workers in `docker-compose.yaml`;
  - Set `--autoscale 1,1` in service `detector_detector` (line 80);
  - Set `--autoscale 1,1` in service `detector_processor` (line 49). 

### Prepare env

1. `$> cp .env.example .env`;
2. Edit `.env` file (change passwords / secret keys).

##### Optional

1. Mount any fs-storage to `./video_storage`;
2. You can easily swap celery's backend (for now it uses redis, but it's pretty expensive, so you can use mongo :) ), just remove `redis` container from `docker-compose.yaml` and change `CELERY_BACKEND_URL` in `.env`.

### Start

1. `$> MIGRATE=true USER_ID=$UID docker-compose up --build`

### I'm in!
- Swagger spec for auth on [`localhost:5000/`](http://localhost:5000/);
- Swagger spec for API on [`localhost:5000/api`](http://localhost:5000/api);

##### Note for swagger auth
If you will use swagger to make some requests: you should add `Bearer ` to generated access token. E.g. token = `super-token` -> authorize in swagger using token = `Bearer super-token`.

-----

## How it works?

### Overall scheme

![Components scheme](https://github.com/dmkulazhenko/web-detector/blob/media/components.svg?raw=true)

Where:
- Processor queue — RabbitMQ Celery queue named `processor` for 'processor' celery workers;
- Detector queue — RabbitMQ Celery queue named `detector` for 'detector' celery workers;
- Processor worker — Celery autoscalable worker, processing tasks from 'processor' queue;
- Detector worker — Celery autoscalable worker, processing tasks from 'detector' queue;
- Video storage — just a mounted directory (host fs), can be (should be) easily replaced with any mountable fs storage;
- Results storage — Redis Celery backend, can be easily replaced with any celery-supported backend (e.g. mongodb).

### Processing scheme

![Processing scheme](https://github.com/dmkulazhenko/web-detector/blob/media/processing.svg?raw=true)

##### Step by step processing
1. Video uploads to flask app;
2. Flask app generates uuid4 for video and saves it to 'video storage';
3. Flask app creates new task `process_video` (in 'processor' queue) and passes uuid4 of video to it;
4. Processor worker takes task `process_video` from 'processor' queue and opens video (from 'video storage' by uuid4);
5. Processor worker splits video on frames;
6. Processor worker splits frames to chunks (you can change `CHUNK_SIZE` in `detector.processor.config`);
7. Processor worker creates chord of detector tasks `detect_frames` (in 'detector' queue) and callback `merge_chunks` (in 'processor' queue);
8. Detector worker takes task `detect_frames` from 'detector' queue;
9. Detector worker tries to load predictor object from thread-local storage, if no predictor here — creates and caches it;
10. Detector worker detect count of GPUs and start detection process not frame-by-frame, but in parallel manner on all GPUs. You can easily disable this `detector.detector.predictor`.
11. Detector worker detect all objects on all frames in chunk and saves result to redis (celery backend);
12. When all detector tasks completed — `merge_chunks` task executes on processor worker;
13. Processor worker takes all per-chunk results, merges and saves them to redis (celery backend);
14. Detection result can be easily obtained from redis (celery backend).

### Scaling
##### Horizontal
- Flask app / processor workers / dector workers use different docker images, so different environments, so can be easily scaled out;
- As far as processor/detector workers are celery-based - they have auto-sync, so we can easily increase number of nodes (even when service is live).

##### Vertical
- Detector workers image based on [nvidia-cuda](https://hub.docker.com/r/nvidia/cuda) and optimized for parallel run on multiple GPUs;
- As far as processor/detector workers are celery-based - they have simple autoscaling (start new workers on one node if needed).

-----

## Easy to change if needed
1. Redis as celery backend is pretty expensive (you can use mongo or what you want), update `.evn/CELERY_BACKEND_URL` and `docker-compose.yaml`;
2. Disable per-task GPU multiprocessing in `detect_frames` tasks, change `detector.detector.predictor`;
3. Adjust workers autoscaling, change `docker-compose.yaml` commands for `detector_processor` and `detector_detector`;

Also, you can save frames to fs storage (as videos), but this will require a little bit more changes, check `detector` package.
