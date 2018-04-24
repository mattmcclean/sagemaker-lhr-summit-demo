# Introduction
This repository contains the source code, Jupyter notebooks, configuration etc. for the SageMaker demo presenteted at the AWS London Summit 2018.

# Setup

Launch a new Cloud9 instance. Make sure you have enough space on the EBS volume. You may have to stop the Cloud9 instance and resize the EBS volume as the default size is only 8 GB.

Ensure that an S3 bucket is created with the model artefacts. The S3 bucket should be named: ```sagemaker-<region_name>-<account_id>``` where *<region_name>* is the AWS region where the demo is being run and *<account_id>* is the AWS Account ID.

If you need to create the S3 bucket do so with this AWS CLI command:

```
aws s3 mb sagemaker-$(aws configure get region)-$(aws sts get-caller-identity --query 'Account' --output text)
```

# Step 1 - Build the Docker image for SageMaker model inference

Run the script to build and push the Docker image to ECS Container Registry (ECR) that will be used by the SageMaker Endpoint infrastructure to run the inference code.

```
$ cd ~/environment/sagemaker-lhr-summit-demo/container
$ ./build_and_push.sh sagemaker-summit-demo
```

# Step 2 - Create the SageMaker model

First check that the model artefacts have been uploaded to S3. They should reside in the S3 bucket name: ```sagemaker-<region_name>-<account_id>``` and key ```models/lhr-summit-demo/model.tar.gz```.

Do this in the AWS Management Console.

# Step 3 - Create the SageMaker Endpoint

Now we need to call the SageMaker APIs to first create a SageMaker endpoint configuration.

Do this in the AWS Management Console.

# Step 4 - Call the endpoint

Open a new SageMaker notebook instance and launch the notebook named *call_endpoint.ipynb* to call the SageMaker endpoint for this demo application.

