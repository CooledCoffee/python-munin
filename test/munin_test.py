# -*- coding: utf-8 -*-
from fixtures2 import TestCase, StreamsFixture, PatchesFixture
from munin import Field, PluginProxy
import munin

class MuninTest(TestCase):
    def setUp(self):
        self.patches = self.useFixture(PatchesFixture())
        self.streams = self.useFixture(StreamsFixture())

class FieldTest(MuninTest):
    def test_simple(self):
        field = Field('a')
        field.config()
        self.assertEqual('''a.label a
''', self.streams.stdout)
        
    def test_thresholds(self):
        field = Field('a', warning=10, critical=100)
        field.config()
        self.assertEqual('''a.label a
a.warning 10
a.critical 100
''', self.streams.stdout)

class PluginProxyTest(MuninTest):
    def test_basic(self):
        self.patches.patch('__main__.category', 'system')
        proxy = PluginProxy()
        self.assertEqual('system', proxy.category)
        
    def test_auto_evaluate(self):
        self.patches.patch('__main__.category', lambda: 'system')
        proxy = PluginProxy(auto_evaluate=True)
        self.assertEqual('system', proxy.category)
        
class ConfigTest(MuninTest):
    def setUp(self):
        super(ConfigTest, self).setUp()
        self.patches.patch('sys.argv', ['/etc/munin/plugins/test_plugin'])
        
    def test_simple(self):
        # set up
        self.patches.patch('__main__.category', 'system')
        self.patches.patch('__main__.vlabel', '%')
        self.patches.patch('__main__.fields', ['a', 'b'])
        
        # test
        munin._config()
        self.assertMultiLineEqual('''graph_title Test Plugin
graph_category system
graph_vlabel %
a.label a
b.label b
''', self.streams.stdout)
        
    def test_fields(self):
        # set up
        self.patches.patch('__main__.category', 'system')
        self.patches.patch('__main__.vlabel', '%')
        self.patches.patch('__main__.fields', [Field('a'), Field('b')])
        
        # test
        munin._config()
        self.assertMultiLineEqual('''graph_title Test Plugin
graph_category system
graph_vlabel %
a.label a
b.label b
''', self.streams.stdout)
        
class ExecuteTest(MuninTest):
    def test_dict(self):
        # set up
        self.patches.patch('__main__.values', lambda: {'a': 1, 'b': 2})
        
        # test
        munin._execute()
        self.assertEqual('''a.value 1.000
b.value 2.000
''', self.streams.stdout)
        
    def test_list(self):
        # set up
        self.patches.patch('__main__.values', lambda: [('a', 1), ('b', 2)])
        
        # test
        munin._execute()
        self.assertEqual('''a.value 1.000
b.value 2.000
''', self.streams.stdout)
        
    def test_generator(self):
        # set up
        def _values():
            yield 'a', 1
            yield 'b', 2
        self.patches.patch('__main__.values', _values)
        
        # test
        munin._execute()
        self.assertEqual('''a.value 1.000
b.value 2.000
''', self.streams.stdout)
    