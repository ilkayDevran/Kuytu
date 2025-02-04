#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from datetime import date
import os
'''Simple usage

from my_logging as my_outputs_and_logging

log = my_outputs_and_logging('Script_Porpuse')
log.logging('to notify any event or operation')
log.logging('works only english alfabet')
log.logging('json cleaning operation -> "olumtarihi" Done ')

log.save_log('Script_Porpuse',u'#.... 2344\n#.... 23454')

print log.get_output_path()

'''
class KuytuLog():
    def __init__(self,output_folder_name,createType = 'w'):
        self.output_folder_name = output_folder_name
        self.createType = createType
        self.create_files()
    def create_and_save_txt_file(self,file_name,text):
        #writing_type can be 'ab' or 'w'
        path = self.output_path+file_name+'.txt'
        with open(path, 'ab') as myfile:
            myfile.write( text )
            myfile.write(str('\n'))        

    def create_files(self):
        today = date.today().strftime('<%Y-%m-%d>')
        mypath = '../'+today+'Outputs-'+self.output_folder_name
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        log_path = mypath+'/'+self.output_folder_name+'_Report.txt'
        self.log_path = log_path
        self.output_path = mypath+'/'
        if self.createType == 'r':
            return
        f= open(log_path,"w")
        f.close()
        
    
    def create_a_file_in_a_folder(self,folder_name,file_name,text):
        mypath =self.output_path+folder_name
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        path = mypath+'/'+file_name+'.txt'
        with open(path, 'ab') as myfile:
            myfile.write( text )
            myfile.write(str('\n'))             

    def add_splitter(self):
        with open(self.log_path, "ab") as myfile:
            myfile.write( '----------------------------------------------------------------')
            myfile.write(str('\n'))    
    def logging(self,text):
        if type(text) == type([]):
            for t in text:
                with open(self.log_path, "ab") as myfile:
                    myfile.write( 'INFO : ')
                    myfile.write( t )
                    myfile.write(str('\n'))
        else:
            with open(self.log_path, "ab") as myfile:
                myfile.write( 'INFO : ')
                myfile.write( text )
                myfile.write(str('\n'))
            
    def save_log(self,title, text):
        with open(self.log_path, "ab") as myfile:
            myfile.write('\n\n'+ title+str(" ---------\n") )
            myfile.write( text + str("\n") )
            myfile.write("--------------------------\n\n")            
    def get_output_path(self):
        return self.output_path
'''
    def create_files():
        today = date.today().strftime('<%Y-%m-%d>')
        mypath = '../'+today+'Outputs_Bulk'
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        article_path = '../'+today+'Outputs_Bulk/All_Article.txt'
        counter_path = '../'+today+'Outputs_Bulk/infoBoxType_Counter.txt'
        log_path = '../'+today+'Outputs_Bulk/Extractor Report.txt'
        f= open(article_path,"w")
        f= open(counter_path,"w")
        f= open(log_path,"w")
        return article_path,counter_path,log_path
'''