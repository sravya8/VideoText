import time
import datetime
import os
import glob
import random
from pyOCR_utils import get_pyOCRtool, pyOCR_read
from common import DATA_PATH, SYNTH_HOME

def test_get_pyOCRtool():
    start = time.time()
    tool = get_pyOCRtool()
    end = time.time()
    assert tool is not None
    print('Time taken to get pyOCR tool ' + str(datetime.timedelta(seconds=end - start)))
    
def test_pyOCR_read():
    images = glob.glob(SYNTH_HOME + '1/*')
    assert images[0] is not None
    tool = get_pyOCRtool()
    start = time.time()
    word_boxes = pyOCR_read(images[0], tool)
    end = time.time()
    assert word_boxes is not None
    print("Test test_pyOCR_read passed")
    print('Time taken: ' + str(datetime.timedelta(seconds=end - start)))

test_get_pyOCRtool()
test_pyOCR_read()
