# -*- coding: utf-8 -*-
import inflection
import inspect
import os
import six
import sys

class Plugin(object):
    category = None
    vlabel = None
    fields = None
    
    def main(self):
        if len(sys.argv) == 1:
            self.execute()
        elif len(sys.argv) == 2 and sys.argv[1] == 'config':
            self.config()
        else:
            raise Exception('Failed to parse command line.')
        
    def config(self):
        file_name = os.path.basename(sys.argv[0])
        plugin_name = os.path.splitext(file_name)[0]
        title = inflection.titleize(plugin_name)
        print('graph_title ' + title)
        print('graph_category ' + self.category)
        print('graph_vlabel ' + self.vlabel)
        for field in self.fields:
            if isinstance(field, six.string_types):
                field = Field(field)
            field.config()
    
    def execute(self):
        values = self.values()
        if isinstance(values, dict):
            values = values.items()
        elif hasattr(values, '__iter__'):
            values = list(values)
        else:
            raise Exception('Values type "%s" is not supported.' % type(values).__name__)
        lines = ['%s.value %0.3f' % (k, v) for k, v in values]
        lines.sort()
        print('\n'.join(lines))
    
    def values(self):
        raise NotImplementedError()

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
            