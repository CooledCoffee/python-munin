# -*- coding: utf-8 -*-
import inflection
import os
import six
import sys

class Field(object):
    def __init__(self, name, warning=None, critical=None):
        self.name = name
        self.warning = warning
        self.critical = critical
        
    def config(self):
        print('%s.label %s' % (self.name, self.name))
        if self.warning is not None:
            print('%s.warning %s' % (self.name, self.warning))
        if self.critical is not None:
            print('%s.critical %s' % (self.name, self.critical))
            
class PluginProxy(object):
    def __init__(self, auto_evaluate=False):
        self._mod = __import__('__main__')
        self._auto_evaluate = auto_evaluate
        
    def __getattr__(self, name):
        try:
            result = getattr(self._mod, name)
            if callable(result) and self._auto_evaluate:
                result = result()
            return result
        except AttributeError:
            raise Exception('Plugin module does not have "%s".' % name)
    
def main():
    if len(sys.argv) == 1:
        _execute()
    elif len(sys.argv) == 2 and sys.argv[1] == 'config':
        _config()
    else:
        raise Exception('Failed to parse command line.')
    
def _config():
    file_name = os.path.basename(sys.argv[0])
    plugin_name = os.path.splitext(file_name)[0]
    title = inflection.titleize(plugin_name)
    plugin = PluginProxy(auto_evaluate=True)
    print('graph_title ' + title)
    print('graph_category ' + plugin.category)
    print('graph_vlabel ' + plugin.vlabel)
    for field in plugin.fields:
        if isinstance(field, six.string_types):
            field = Field(field)
        field.config()
        
def _execute():
    plugin = PluginProxy()
    values = plugin.values()
    if isinstance(values, dict):
        values = values.items()
    elif hasattr(values, '__iter__'):
        values = list(values)
    else:
        raise Exception('Values type "%s" is not supported.' % type(values).__name__)
    lines = ['%s.value %0.3f' % (k, v) for k, v in values]
    lines.sort()
    print('\n'.join(lines))
    