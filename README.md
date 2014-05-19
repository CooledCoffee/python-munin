Installation
============

pip install python-munin

Examples
========

Static Fields
-------------

	from munin import Plugin, Field
	
	class LoadPlugin(Plugin):
	    category = 'system'
	    fields = [
	        Field('load1', warning=4, critical=6),
	        Field('load5', warning=4, critical=6),
	        Field('load15', warning=4, critical=6),
	    ]
	    vlabel = 'load'
	    
	    def values(self):
	        with open('/proc/loadavg') as f:
			    data = f.read()
			load1, load5, load15 = [float(s) for s in data.split()[:3]]
	        return {
	            'load1': load1,
	            'load5': load5,
	            'load15': load15,
	        }
	        
	LoadPlugin().main()
	
Dynamic Fields
--------------

	from munin import Plugin, Field
	import os
	
	class CpuFreqPlugin(Plugin):
	    category = 'system'
	    vlabel = 'load'
	
	    @property
	    def fields(self):
	        cpus = _list_cpus()
	        return [Field(c) for c in cpus]
	
	    def values(self):
	        values = {}
	        cpus = _list_cpus()
	        for cpu in cpus:
	            path = os.path.join('/sys/devices/system/cpu', cpu, 'cpufreq', 'cpuinfo_cur_freq')
	            with open(path) as f:
	                freq = int(f.read())
	            values[cpu] = freq
	        return values
	
	def _list_cpus():
	    files = os.listdir('/sys/devices/system/cpu')
	    return [f for f in files if f.startswith('cpu') and f[3:].isdigit()]
	
	CpuFreqPlugin().main()

Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
