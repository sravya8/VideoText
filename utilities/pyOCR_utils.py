from PIL import Image
import sys
import pyocr
import pyocr.builders

def get_pyOCRtool():
    """ Check pyOCR installation and returns the recommended OCR tool"""
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1) # TODO: Understand when to use system exit
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    return tool

def pyOCR_read(image_path, tool):
    """ Reads an image and returns word_boxes and text corresponding to it"""
    word_boxes = tool.image_to_string(
    Image.open(image_path),
    lang="eng",
    builder=pyocr.builders.WordBoxBuilder())
    return word_boxes

def visualizepyOCRBoxes(image_path):
    tool = get_pyOCRtool()
    word_boxes = pyOCR_read(image_path, tool)
    image = Image.open(image_path)
    im = np.array(image, dtype=np.uint8)
    fig, ax = plt.subplots(1)
    ax.imshow(im)
    for box in word_boxes:
        rect = patches.Rectangle(box.position[0], 
                  box.position[1][0], 
                  box.position[1][1],
                 linewidth=1, edgecolor='r', facecolor='none', label=box.content)
        ax.add_patch(rect)
    plt.show()

