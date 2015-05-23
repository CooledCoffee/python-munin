Installation
============

pip install python-munin

Examples
========

First Plugin
------------

	import munin
	
	category = 'system'
	fields = [
	    'load1',
	    'load5',
	    'load15',
	]
	vlabel = 'load'
	
	def values():
	    with open('/proc/loadavg') as f:
	        data = f.read()
	    load1, load5, load15 = [float(s) for s in data.split()[:3]]
	    return {
	        'load1': load1,
	        'load5': load5,
	        'load15': load15,
	    }
	        
	if __name__ == '__main__':
	    munin.main()

Setting Thresholds
------------------

	from munin import Field
	import munin
	
	category = 'system'
	fields = [
	    Field('load1', warning=4, critical=6),
	    Field('load5', warning=4, critical=6),
	    Field('load15', warning=4, critical=6),
	]
	vlabel = 'load'
	
	def values():
	    with open('/proc/loadavg') as f:
	        data = f.read()
	    load1, load5, load15 = [float(s) for s in data.split()[:3]]
	    return {
	        'load1': load1,
	        'load5': load5,
	        'load15': load15,
	    }
	
	if __name__ == '__main__':
	    munin.main()
	
Dynamic Fields
--------------

	import munin
	import os
	
	category = 'system'
	vlabel = 'load'
	
	def fields():
	    files = os.listdir('/sys/devices/system/cpu')
	    return [f for f in files if f.startswith('cpu') and f[3:].isdigit()]
	
	def values():
	    for cpu in fields():
	        path = os.path.join('/sys/devices/system/cpu', cpu, 'cpufreq', 'cpuinfo_cur_freq')
	        with open(path) as f:
	            freq = int(f.read())
	        yield cpu, freq
	
	if __name__ == '__main__':
	    munin.main()
