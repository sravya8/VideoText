from synth_utils import SynthUtil
from common import *
import random
import os
class TestSynthUtil:
   
    s = None
 
    def test_load_synthtext_labels():
        s  = SynthUtil(SYNTH_HOME + 'gt.mat')
        assert s.mat is not None

    def test_get_index_from_filename():
        filename = '1/' + random.choice(os.listdir(SYNTH_HOME + '1/'))
        assert SynthUtil.get_index_from_filename(filename) is not -1

    def test_visualize_synthtext(index):
        image = Image.open(SYNTH_HOME + str(s.mat['imnames'][0][index][0]))
    #   filename = '1/' + random.choice(os.listdir(SYNTH_HOME + '1/'))
    #    index = get_index_from_filename(filename)
        print(index)
        im = np.array(image, dtype=np.uint8)
        SynthUtil.visualize_synthtext(im, wordBB=s.mat['wordBB'][0][index], text=SynthUtil.mat['txt'][0][index])
        
    def test_transform_synth_text():
        txt = SynthUtil.transform_synth_text()
        assert len(txt) == len(s.mat['txt'][0])
        
    def test_save_clean_inputs():
        SynthUtil.save_clean_inputs(SYNTH_HOME)
        assert os.path.exists(SYNTH_HOME + 'processed/imnames.npy') == 1
        assert os.path.exists(SYNTH_HOME + 'processed/wordBB.npy') == 1
        assert os.path.exists(SYNTH_HOME + 'processed/text.npy') == 1
        assert np.load(SYNTH_HOME + 'processed/imnames.npy').size > 1
        assert np.load(SYNTH_HOME + 'processed/wordBB.npy').size > 1
        assert np.load(SYNTH_HOME + 'processed/text.npy').size > 1

TestSynthUtil.test_load_synthtext_labels()
#TODO: Fix accessing mat from various test functions
#TestSynthUtil.test_get_index_from_filename()
