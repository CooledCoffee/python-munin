# -*- coding: utf-8 -*-
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase, StreamsFixture
from munin.plugin import Plugin, Field

class FieldTest(TestCase):
    def setUp(self):
        super(FieldTest, self).setUp()
        self.streams = self.useFixture(StreamsFixture())
        
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

class ConfigTest(TestCase):
    def setUp(self):
        super(ConfigTest, self).setUp()
        self.streams = self.useFixture(StreamsFixture())
        self.useFixture(MonkeyPatch('sys.argv', ['/etc/munin/plugins/test_plugin']))
        
    def test_static(self):
        class TestPlugin(Plugin):
            category = 'category1'
            vlabel = '%'
            fields = [
                Field('a'),
                Field('b'),
            ]
        plugin = TestPlugin()
        plugin.config()
        self.assertMultiLineEqual('''graph_title Test Plugin
graph_category category1
graph_vlabel %
a.label a
b.label b
''', self.streams.stdout)
        
    def test_dynamic(self):
        class TestPlugin(Plugin):
            @property
            def category(self):
                return 'category1'
            
            @property
            def vlabel(self):
                return '%'
            
            @property
            def fields(self):
                return [
                    Field('a'),
                    Field('b'),
                ]
        plugin = TestPlugin()
        plugin.config()
        self.assertMultiLineEqual('''graph_title Test Plugin
graph_category category1
graph_vlabel %
a.label a
b.label b
''', self.streams.stdout)
        
class ExecuteTest(TestCase):
    def test(self):
        self.streams = self.useFixture(StreamsFixture())
        class TestPlugin(Plugin):
            def values(self):
                return {'a': 1, 'b': 2}
        plugin = TestPlugin()
        plugin.execute()
        self.assertEqual('''a.value 1
b.value 2
''', self.streams.stdout)
        