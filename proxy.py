import urllib2
import datetime
import re

from operator import itemgetter

__all__ = ['runtest']

def fetch_proxy():

	#proxy_url = 'http://www.cnproxy.com/proxy1.html'
	#find the IP address from page 'proxy_url'
	#IP_re = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	#return IP_re.findall(urllib2.urlopen(proxy_url).read())

	proxy_url = 'http://pachong.org'
	content = urllib2.urlopen(proxy_url).read()

	#IP re
	IP_re = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' + r'</td>\s+<td>\d{1,5}')
	IP_list_origin = IP_re.findall(content)
	#replace
	p = re.compile(r'</td>\s+<td>')
	IP_list = [p.sub(':',IP) for IP in IP_list_origin]

	return IP_list


def visit(proxy, url):
	#proxy
	proxy_support = urllib2.ProxyHandler({'http':proxy})
	opener = urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)
	#header
	header = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
	#reuqest
	req = urllib2.Request(url = url, headers = header)

	start = datetime.datetime.now()
	try:
		urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		print e.code
		print e.read()
		return -1
	except urllib2.URLError as e:
		print 'URLError: %s' %url
		print e.reason
		return -2


	end = datetime.datetime.now()
	return (end - start).total_seconds()

def runtest():
	test_url = 'http://www.baidu.com'

	print'fetch proxy servers...'
	proxy_list = fetch_proxy()

	print'start test...'
	proxy_cost = []
	for proxy in proxy_list:
		total = 0.0
		print '----'
		print 'load %s' %test_url
		for i in range(10):
			cost = visit(proxy, test_url)
			print proxy + ' ' + str(cost)
			if cost > 0:
				total = total + cost
			else:
				total = -1
				break
		print total
		proxy_cost.append(total)

	tmp = zip(proxy_list, proxy_cost)
	tmp = sorted(tmp, key = itemgetter(1))

	return [proxy[0] for proxy in tmp if proxy[1] > 0]


if __name__ == '__main__':
	for i in runtest():
		print i

