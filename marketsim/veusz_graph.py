from marketsim.scheduler import world
from colorsys import hsv_to_rgb
from random import uniform
import sys
from veusz.veusz_main import run
import os
import errno
import __main__


def ensure_dir(path):
    """ Ensures that directory given 'path' exists
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def myDir():
    """ Returns a directory for temporary files with respect to name of main module
    """
    d = r"_output/" + os.path.basename(__main__.__file__)
    ensure_dir(d)
    return d + r"/"


def randColor():
    """ Returns a color randomly chosen from HSV space
    """
    h = uniform(0., 1.) 
    s = uniform(0.2, .8)
    v = uniform(0.3, .8)
    
    def toHex(x):
        return hex(int(x*255))[2:]

    r, g, b = hsv_to_rgb(h, s, v)
    
    return toHex(r) + toHex(g) + toHex(b)

graphDataHeader = """
ImportFileCSV('{0}', linked=True)
To(Add('xy', name='{1}', autoadd=False))
"""
   
class CSV(file):
    """ Represents a time serie to be written into a file 
    """
    
    def __init__(self, filename, source, label, attributes={}):
        """ Initializes time serie writer
        filename - name of a file to write to 
        source - indicator with values to be saved
        label - time serie label
        """
        file.__init__(self, filename, 'w')
        self._filename = filename
        self._label = label
        
        self.write('Time'+label+','+label+',\n')
        
        def wakeUp(_):
            """ Called when the source has chaged
            """
            x = source.value
            if x is not None: # for the moment we don't know what to do with breaks in data
                self.write(str(world.currentTime) + ',' + str(x) + ',\n')
        
        source.advise(wakeUp)
        
        self._attributes = {
            'xData' : "Time"+label,
            'yData' : label,
            'marker': 'none',
            r'PlotLine/steps': u'left',
            r'PlotLine/color': u'#' + randColor(),
            'key' : label,
            }
        
        for k,v in attributes.iteritems():
            self._attributes[k] = v
        
    def exportToVsz(self, f):
        """ Exports time serie to Vsz file
        """
        self.flush()
        os.fsync(self)
        f.write(graphDataHeader.format(self._filename, self._label))
        for k,v in self._attributes.iteritems():
            f.write("Set('{0}', {1})\n".format(k,repr(v)))
        f.write("To('..')\n")
  

graphHeader = """
To(Add('page', name='page_{0}', autoadd=False))
Set('width', u'25cm')
To(Add('graph', name='graph_{0}', autoadd=False))
To(Add('axis', name='x', autoadd=False))
Set('label', u'Time')
To('..')
Add('axis', name='y', autoadd=False)
"""

graphTrailer = """
Add('key', name='key1', autoadd=False)
To('..')
To('..')
"""

def translateAttributes(src):
    """ Translates abstract attributes to Veusz graph attributes
    """
    res = {}
    if 'smooth' in src and src['smooth']:
        res[r'PlotLine/steps'] = 'off'
    return res
        
class Graph(object):
    """ Represents a single Veusz graph
    """
    
    def __init__(self, name):
        """ Initializes graph with some name
        """
        self._name = name
        self._datas = []
        
    def addTimeSerie(self, source, attributes = {}):
        """ Adds a time serie to the graph
        source should be a source of events (so to have advise method) 
        and have a value property 
        attributes -- veusz specific attributes that will be applied for this time serie  
        """
        label = source.label
        attr = translateAttributes(source.attributes)
        for k,v in attributes.iteritems():
            attr[k] = v
        filename = (myDir()+label+'.csv').replace('\\','_').replace(r'/','_')
        self._datas.append(CSV(filename, source, label, attr))
        
    def exportTo(self, f):
        """ Exports graph to some Vsz file
        """
        f.write(graphHeader.format(self._name))

        for ts in self._datas:
            ts.exportToVsz(f)
            
        f.write(graphTrailer)

def showGraphs(name, graphs):
    """ Draws a sequence of graphs into a Veusz workspace and launches veusz
    """
    with open(myDir() + name+".vsz", "w") as f:
        for g in graphs:
            g.exportTo(f)
    sys.argv = [sys.argv[0], myDir()+name+".vsz"]
    run()
    