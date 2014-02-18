import urllib2
import urlparse
import lxml.html

def get_xiami_music_code(keywords):
	"""
		For the given keywords
		return the list of top N == count share code 
		for the blog usage.
	"""
	#xiami music search base url
	#For example: to search lana del rey's ride
	#http://www.xiami.com/search/search?key=ride+lana+del+rey&pos=1
	base_url = 'http://www.xiami.com/search?key='

	keywords = keywords.replace(' ','+') + '&pos=1'

	#url
	url = base_url + keywords

	#header
	header = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

	#request
	req = urllib2.Request(url = url, headers = header)

	#extract code links from content, using method find_class from lxml.html
	code_link_list = [i.attrib['href'] for i in lxml.html.find_class(urllib2.urlopen(req).read(), 'toplayer')]

	#parse the sid and return the result
	base_html_code_template_pre = '''
	<embed src="http://www.xiami.com/widget/'''
	base_html_code_template_back =''' 
	/singlePlayer.swf" 
	type="application/x-shockwave-flash" width="257" height="33" wmode="transparent"></embed>
	'''

	return [base_html_code_template_pre + '0_' + urlparse.urlparse(i).query.split('=')[1] + base_html_code_template_back for i in code_link_list]

	
if __name__ == '__main__':
	for i in get_xiami_music_code('ride'):
		print i
