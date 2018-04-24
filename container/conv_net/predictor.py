# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import shutil
import json

import flask
import numpy as np

import torchvision

from fastai.imports import *

from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *

prefix = '/opt/ml/'

model_path = os.path.join(prefix, 'model')

MODEL_NAME = os.environ.get("MODEL_FILENAME", "lhr-summit-demo")

IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", "224"))

ARCH=getattr(torchvision.models.resnet, os.environ.get("ARCH", "resnet34"))

DATA_PATH = os.path.join(model_path, "data")
TRAIN_PATH = os.path.join(DATA_PATH, "train")
VALID_PATH = os.path.join(DATA_PATH, "valid")
TEST_PATH = '/tmp/test'

TEST_IMG = os.path.join(TEST_PATH, 'placeholder.jpg')

if not os.path.exists(TEST_PATH):
    os.makedirs(TEST_PATH, mode=0o755,exist_ok=True)
    print('Created dir: {}'.format(TEST_PATH))
    img_file = glob(TRAIN_PATH+'/**/*.jpg', recursive=True)[0]
    shutil.copyfile(img_file, TEST_IMG)

def get_data():
    tfms = tfms_from_model(ARCH, IMAGE_SIZE)
    return ImageClassifierData.from_paths(prefix, tfms=tfms, trn_name=TRAIN_PATH,
        val_name=VALID_PATH, test_name=TEST_PATH)


def write_test_image(stream):
    with open(TEST_IMG, "bw") as f:
        chunk_size = 4096
        while True:
            chunk = stream.read(chunk_size)
            if len(chunk) == 0:
                return
            f.write(chunk)

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ClassificationService(object):
    model = None                # Where we keep the model when it's loaded
    data = None              # Where we keep the data classes object

    @classmethod
    def get_data(cls):
        """Get the data class if not already loaded."""
        if cls.data == None:
            cls.data = get_data()
        return cls.data

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            data = cls.get_data()
            cls.model = ConvLearner.pretrained(ARCH, data, precompute=False, models_name='model')
            cls.model.load(MODEL_NAME)
        return cls.model

    @classmethod
    def get_classes(cls):
        """Get the data classes for the model."""
        data = cls.get_data()
        return data.classes

    @classmethod
    def predict(cls, img_path):
        """For the input, do the predictions and return them.

        Args:
            img_path (file path to image file): The path to the image to predict"""
        mdl = cls.get_model()
        data_classes = cls.get_classes()
        test_preds = mdl.predict(is_test=True)
        print("test_preds: {}".format(test_preds))
        print("test_preds.shape: {}".format(test_preds.shape))
        maxP = np.argmax(test_preds, axis=1) # Pick the index with highest log probability
        probs = np.exp(test_preds[:,1])
        print("probs : {}".format(probs))
        print("maxP: {}".format(maxP))
        actualclass = data_classes[maxP[0]]
        return actualclass, float(probs)

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ClassificationService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """

    print("cleaning test dir")
    for root, dirs, files in os.walk(TEST_PATH):
        for f in files:
            os.unlink(os.path.join(root, f))
    # write the request body to test file
    write_test_image(flask.request.stream)

    # Do the prediction on the image
    class_pred, conf_score = ClassificationService.predict(TEST_IMG)

    # Convert result to JSON
    result = { 'result': {} }
    result['result']['class'] = class_pred
    result['result']['confidence'] = conf_score

    return flask.Response(response=json.dumps(result), status=200, mimetype='application/json')
