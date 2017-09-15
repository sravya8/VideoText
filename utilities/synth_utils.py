import scipy.io
class SynthUtil:

    def __init__(self, path):
        """ Loads the SynthText labels and sets the matlab cell array"""
        self.mat = scipy.io.loadmat(path)
        print('Loaded mat file')

    def get_index_from_filename(filename):
        """ Get index of mat file for a given file name"""
        for index,text in enumerate(self.mat['imnames'][0]):
            if text == filename:
                return index
        return -1

    def transform_synth_text():
        """ Text in SynthText are clubbed together with \n. 
        This utility function splits it out into a single dimensional text array for each image"""
        txt = []
        for i in range(self.mat['txt'][0].shape[-1]):# Each image
            new_text = []
            for j in range(self.mat['txt'][0][i].shape[-1]):#Number of text strings
                words = self.mat['txt'][0][i][j].split('\n')
                for k in words:
                    new_text.append(k.strip())
            txt.append(new_text)
        return np.asarray(txt)
        
    def visualize_synthtext(text_im, wordBB, text):
        """
        text_im : np image
        wordBB : 2x4xm matrix of word coordinates
        """
        plt.imshow(text_im)
        # plot the word-BB:
            
        for i in range(wordBB.shape[-1]): #Number of boxes
            bb = wordBB[:,:,i]
            bb = np.c_[bb,bb[:,0]]
            plt.plot(bb[0,:], bb[1,:], 'g', alpha=0.8)
            # visualize the indiv vertices:
            vcol = ['r','g','b','k']
            for j in range(4):
                plt.scatter(bb[0,j],bb[1,j],color=vcol[j])  
            plt.text(bb[0][0], bb[1][0], text[i].strip(), color='r')
        plt.show()

    def find_clean_inputs():
        """ Returns good indices where there is no missing text. """
        good_indices = []
        for index in range(self.mat['imnames'][0].shape[-1]):
            if(self.mat['wordBB'][0][index].shape[-1] == len(txt[index])):
                good_indices.append(index)
        return good_indices

    def save_clean_inputs(folder_path):
        os.mkdir(folder_path+'processed')
        folder_path= folder_path+'processed/'
        good_indices = find_clean_inputs(self.mat)
        wordBB = self.mat['wordBB'][0][good_indices]
        text = transform_synth_text(self.mat)[good_indices]
        imnames = self.mat['imnames'][0][good_indices]
        numpysave(folder_path,imnames,wordBB,text)

    def numpysave(folder_path,imnames,wordBB,text):
        np.save(folder_path+'imnames.npy', imnames)
        np.save(folder_path+'wordBB.npy', wordBB)
        np.save(folder_path+'text.npy', text) 

