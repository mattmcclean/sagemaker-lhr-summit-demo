# Introduction
This repository contains the source code, Jupyter notebooks, configuration etc. for the SageMaker demo presenteted at the AWS London Summit 2018.

# Step 1 - Build the Docker image for SageMaker model inference

Run the script to build and push the Docker image that will be used by the SageMaker Endpoint infrastructure to run the inference code.

```
$ cd ~/environment/sagemaker-lhr-summit-demo/container
$ ./build_and_push.sh sagemaker-summit-demo
```
