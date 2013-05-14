from marketsim import scheduler, bind
from colorsys import hsv_to_rgb
from subprocess import Popen
import random
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
    h = random.uniform(0., 1.) 
    s = random.uniform(0.2, .8)
    v = random.uniform(0.3, .8)
    
    def toHex(x):
        return hex(int(x*255))[2:]

    r, g, b = hsv_to_rgb(h, s, v)
    
    return toHex(r) + toHex(g) + toHex(b)

graphDataHeader = """
ImportFileCSV('{0}', linked=True)
To(Add('xy', name='{1}', autoadd=False))
"""

class OutputStream(object):
    
    def __init__(self, filename):
        self._filename = filename
        self._file = None
        
    def reset(self):
        if self._file: 
            self._file.close(self)
        self._file = file(self._filename, 'w')
    
    def __getstate__(self):
        return {'_filename': self._filename}

    def __setstate__(self, dict):
        self._filename = dict['_filename']
        self._file = None
        self.reset()
        
    def write(self, s):
        self._file.write(s)
 
    def flush(self):
        self._file.flush()
        os.fsync(self._file)       
   
class CSV(object):
    """ Represents a time serie to be written into a file 
    """
    
    def __init__(self, directory, filename, source, label, attributes={}):
        """ Initializes time serie writer
        filename - name of a file to write to 
        source - indicator with values to be saved
        label - time serie label
        """
        self._fullname = directory + filename
        self._filename = filename
        self._file = OutputStream(self._fullname)
        self._label = label
        self._sched = scheduler.current()
        
        self._source = source
        
        source.advise(self)
        
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
            
        self.reset()
        
        
    def __call__(self, _):
        """ Called when the source has chaged
        """
        x = self._source.value
        if x is not None: # for the moment we don't know what to do with breaks in data
            self._file.write(str(self._sched.currentTime) + ',' + str(x) + ',\n')
            
    def reset(self):
        self._file.reset()
        self._file.write('Time'+self._label+','+self._label+',\n')
        
            
    @property
    def source(self):
        return self._source
    
    _properties = { "source" : None }
        
    def exportToVsz(self, f):
        """ Exports time serie to Vsz file
        """
        self._file.flush()
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
# Export(r'{0}.png', page={1})

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
        
    @property
    def series(self):
        return self._datas
    
    _properties = { "series" : None }
        
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
        filename = (label+'.csv').replace('\\','_')
        self._datas.append(CSV(myDir(), filename, source, label, attr))
        
    def addTimeSeries(self, series):
        for x in series:
            self.addTimeSerie(x)
            
    def __iadd__(self, series):
        self.addTimeSeries(series)
        return self
        
    def exportTo(self, f, idx):
        """ Exports graph to some Vsz file
        """
        f.write(graphHeader.format(self._name))

        for ts in self._datas:
            ts.exportToVsz(f)
            
        f.write(graphTrailer.format(self._name, idx))
        
def run(name):
    if not 'VEUSZ_EXE' in os.environ:
        print "Path to Veusz executable is not specified in VEUSZ_EXE environment variable"
        print "Hoping that 'veusz' executable is in standard paths"
        print "You may look also for the results manually in Veusz script: " + myDir()+name+".vsz"
        veusz_exe = 'veusz'
    else:
        veusz_exe = os.environ['VEUSZ_EXE']
    Popen(veusz_exe + ' ' + os.path.abspath(myDir()+name+".vsz"), shell=True)
        

def render(name, graphs):
    """ Draws a sequence of graphs into a Veusz workspace and launches veusz
    """
    with open(myDir() + name+".vsz", "w") as f:
        idx = 0
        for g in graphs:
            g.exportTo(f, idx)
            idx += 1
    run(name)
    