from marketsim import (event, _)

class _BreaksAtChanges_Impl(object):
    
    def __init__(self):
        self._value = None
        event.subscribe(self.source, _(self)._clean, self)
        
    def bind(self, ctx):
        self._scheduler = ctx.world
    
    def _clean(self, dummy):
        self._setup(None)
        self._scheduler.async(_(self, self.source())._setup)
        
    def _setup(self, x):
        self._value = x
        self.fire(self)
    
    def __call__(self):
        return self._value
