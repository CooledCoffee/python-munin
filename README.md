Installation
============

pip install python-munin

Example
=======

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
	        
Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
