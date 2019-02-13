#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from Articles import Article 

def checkFilePath(mypath):
	import os
	if not os.path.isdir('/'.join(mypath.split('/')[:-1])):
		os.makedirs( '/'.join(mypath.split('/')[:-1]) )			
	f = open(mypath,'w')
	f.close()	
def save_XML(XMLPath, indexPath, articleList ):

	def prettyPrintXml(xmlFilePathToPrettyPrint):
		from lxml import etree
		assert xmlFilePathToPrettyPrint is not None
		parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
		document = etree.parse(xmlFilePathToPrettyPrint, parser)
		document.write(xmlFilePathToPrettyPrint, pretty_print=True, encoding='utf-8')			
	def generate_XML_page(article_object):
		import XML_templates as tp
		def give_paragrafXML(paragraph):
			return tp.paragrafTemplate%paragraph
		def give_allArticleText(article_object):
			try:
				return tp.all_text%article_object.get_allBulkText()
			except Exception as e:
				return ''
		''' bura '''

		paragraphList = []
		for p in article_object.get_bulkParagraphs():
			paragraphList.append(give_paragrafXML(p))
		map = {}
		map['ParagraphList_XMLtext'] = '\n '.join(paragraphList)
		map['Id'] = article_object.get_Id()
		map['Title'] = article_object.get_Title()
		map['infoBox_type'] = article_object.get_infoBox_type()
		map['infoBoxText'] = article_object.get_infoBoxText()
		map['allBulkText'] = article_object.get_allBulkText()
		map['AllText_XMLText'] = give_allArticleText(article_object)

		return tp.template%map
	''' 2'''
	if len (articleList) == 0 :
		log = '!'+'-'*10+'  There is no Page to Save -- FileName(%31s)'%XMLPath.split('/')[-1]+'-'*10+'!'
		print log
		return log
	checkFilePath(XMLPath)



	f = open(XMLPath,"w")
	f.write('<Pages>\n\t')

	indexfile = open(indexPath,"w")	
	# -------
	indexData = []
	for i,article_object in enumerate(articleList):
		indexFileString = "%s#%s#%d\n"
		if type(article_object)==type(Article()): # article object 
			articleXML_text =  generate_XML_page(article_object).encode('utf-8')
			indexFileString = indexFileString%(article_object.get_Id(), article_object.get_Title(), i+1 )
		elif type(article_object) == type(tuple()): 
			all_xml_test_as_string, Title, Id = article_object
			indexFileString = indexFileString%( Id , Title, i+1 )
			articleXML_text = all_xml_test_as_string
		else:
			articleXML_text = article_object
			indexFileString = (indexFileString%( 'Indexlenememiş' , 'Indexlenememiş', i+1 )).decode('utf-8')
		f.write( articleXML_text )

		indexfile.write( indexFileString.encode('utf-8') )
	f.write('</Pages>')		
	f.close()
	indexfile.close()
	# ---- 
	try:	
		prettyPrintXml(XMLPath)
	except Exception as e:
		print e
		print '!! [prettyPrintXml] Execution Had Some Errors!!'
	log =  '!'+'-'*2+' %6d Article Saved Successfully -- FileName(%31s)'%(len(articleList),XMLPath.split('/')[-1])+'-'*10+'!'
	print log
	return log

def save_Uniq_InfoBoxTypes(path,data):
	checkFilePath(path)
	f = open(path,'w')
	for BK_type,hit_count in data:
		line = '%s#%d\n'%(BK_type.encode('utf-8'),hit_count)
		f.write( line )

def save_Graph(output_path,data,min_repetition,title):
	''' Function draws list of list form data
		[ ['BK Type' , hitCount],
		  ['BK Type' , hitCount],
		  ['BK Type' , hitCount]....]
	'''
	def draw(x,y,title,saving_path):
		import matplotlib.pyplot as plt
		plt.title(title)
		plt.plot(x, y)
		plt.xticks(x, x, rotation='vertical')
		fig =plt.gcf()
		fig.set_size_inches(20, 11)
		#plt.savefig(saving_path)
		plt.savefig(saving_path,format='eps', dpi=1000)
		#plt.show()

	x_list = [x for x,y in data if y>=min_repetition ]
	y_list = [y for x,y in data if y>=min_repetition ]
	draw(	x = x_list, 
			y = y_list, 
			title = title, 
			saving_path = output_path+title)
	#print output_path+title