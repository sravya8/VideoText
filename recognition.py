import sys
sys.path.append("crnn.pytorch")
import torch
from torch.autograd import Variable
import utils
import dataset
from PIL import Image

import models.crnn as crnn
import time

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer

model_path = 'crnn.pytorch/data/crnn.pth'
#img_path = '/home/sravya/data/muse/mydata/4.jpg'
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

#Intial model
model = crnn.CRNN(32, 1, 37, 256)
if torch.cuda.is_available():
    model = model.cuda()
print('loading pretrained model from %s' % model_path)
model.load_state_dict(torch.load(model_path))

#Utilities
#For decoding model output
converter = utils.strLabelConverter(alphabet)
#For preprocessing the input
transformer = dataset.resizeNormalize((100, 32))

def recognize_cropped(image):
    image = transformer(image.convert('L'))
    if torch.cuda.is_available():
        image = image.cuda()
    #Reshaping by adding another axis with length 1 at the beginning?
    # [1, 32, 100] -> [1, 1, 32, 100]
    image = image.view(1, *image.size())
    
    #Create pytorch variable and evaluate(infer) the model
    image = Variable(image)
    model.eval()
    preds = model(image)
    # preds.size() = [26, 1, 37]
    #Process preds for decoding
    _, preds = preds.max(2)
    preds = preds.transpose(1, 0).contiguous().view(-1)

    #Decode
    preds_size = Variable(torch.IntTensor([preds.size(0)]))
    raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
    sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
    return raw_pred, sim_pred
    #print('%-20s => %-20s' % (raw_pred, sim_pred))
 
@timefunc
def recognize(filename,wordBB):
    text = []
    for bb in wordBB:
        image = Image.open(filename)
        raw_pred, sim_pred = recognize_cropped(image.crop(bb))
        text.append(sim_pred)
    return text