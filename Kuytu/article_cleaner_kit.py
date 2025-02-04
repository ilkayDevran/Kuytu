#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author =__Uluç Furkan Vardar__

'''Simple usage



'''

import re
import json
import copy

def configure_BK_fieldsMaps():
    ''' User can easly add a new field in maps or banned fields here, 
        Also User can edit the map with in the program
    '''
    month = [   'Ocak',
                'Şubat',
                'Mart',
                'Nisan',
                'Mayıs',
                'Haziran',
                'Temmuz',
                'Ağustos',
                'Eylül',
                'Ekim',
                'Kasım',
                'Aralık']

    key_banned = ['imza',
                  'internet',
                  'resim',
                  'resimboyutu',
                  'websitesi',
                  'renkler',
                  'altyazı',
                  'plakşirketi',
                  'internetsitesi',
                  'resmiinternetsitesi'
                  'image',
                  'imagesize',
                  'homepage',
                  'resimadı',
                  'imdb',
                  'genişlet',
                  'screenshot',
                  'website',
                  'logo',
                  'resimyazısı']

    value_banned = ["<!--",
                    "null",
                    "yalın liste|",
                    "",
                    "flatlist|"]



    value_maps = {  'ad' :          [   'adı'       ,
                                        'isim'      ,
                                        'ismi'      ,
                                        'adi'       ,
                                        'name'      ,
                                        'karakteradı'],

                    'doğumtarihi' : [   'dogumtarihi','birthdate'],
                    'doğumyeri'   : [   'birthplace' ,'location'],
                    'meslek'      : [   'mesleği'    ],
                    'ulus'        : [   'nationality' ]
                    }
    county_map = {
                "KOR" :"Kore",
                "TUR" : "Türkiye",
                "GER" : "Almanya",
                "JAM" : "Jameika",
                "ESP" : "İspanya",
                "RUS" : "Rusya",
                "USA" : "ABD",
                "FRA" : "Fransa",
                "CHN" : "Çin",
                "UK"  : "Büyük Britanya",
                "ENG" : "İngiltere",
                "SVK" :"Slovakya",
                "SWE" : "İsviçre",
                "AUS" : "Avusturalya",
                "SSCB":"Sovyetler Birliği",
                "MEX" : "Meksika",
                "MAR" : "FAS"

    }


    maps = {}
    maps['county_map'] = county_map
    maps['value_maps'] = value_maps
    maps['month'] = month
    maps['key_banned'] = key_banned
    maps['value_banned'] = value_banned
    return maps
    


def clean_InfoBoxBulk( Bulk_InfoBoxText ):
    def step1(infoBox):
        #some cleanings
        infoBox = re.sub(r"\[\[Dosya.*\]\]","",infoBox)
        infoBox = re.sub(r"<br/>",",",infoBox)
        infoBox = re.sub(r"<br />",",",infoBox)    
        infoBox = re.sub(r"<br>",",",infoBox)
        #infoBox = infoBox.replace('[[','').replace(']]','').replace("\'\'\'",'').replace("''",'')
        #infoBox = infoBox.replace('{{','').replace('}}','')
        infoBox = re.sub(r"<ref(.|\n)*</ref>","",infoBox)
        infoBox = infoBox.replace(u'\xa0', u' ')
        return infoBox
    def step2(infoBox):
        #empty place will be deleted
        t = infoBox.split('\n')
        infoBox = []
        for i in range(0,len(t)):
            line = t[i]
            if ' ' == line or ' ' == line or '  ' == line or '' == line:
                continue
            elif line.count('=') == 1:
                if len(line[line.find('='):].replace(' ','')) <3:
                    continue
                else:
                    infoBox.append(t[i])
            else:
                infoBox.append(t[i])
        infoBox = '\n'.join(infoBox)
        return infoBox
    def step3(infoBox):
        text = infoBox
        try:
            lines = text.replace('<nl>','\n').split('\n')
            temp = {}
            for i in range(1,len(lines)):
                temp_key = ""
                temp_value = ""
                lines[i] = lines[i].strip()
                if lines[i].count('=') == 1:
                    if '|' in lines[i]:
                        m = re.search(".*\|(.*)=(.*)",lines[i])
                        #print lines[i]
                        temp_key = (m.group(1)).replace('|','').strip()
                        temp_value = m.group(2).strip()
                        temp[temp_key] = temp_value
                    else:
                        #print lines[i],"-----"
                        #print 'HATA!! PİPE YOK..'
                        continue
                else:
                    if '}}' == lines[i]:
                        continue
                    #print lines[i],"-----"
                    #print 'HATA! BİRDEN FAZLA EŞİTTİR/Yok......\n\n\n\n'
                    continue  
            return temp
        except Exception as e:
            return None
    def clean_jsonvalues(infobox):
        if infobox == None:
            return None
        maps = configure_BK_fieldsMaps()
        try:
            newjson = {}
            for key in infobox.keys():
                infobox[key] = infobox[key].encode('utf8')
                new_key = key.encode('utf8').replace(' ','').replace('_','').lower()

                # banned key 
                if new_key in  maps['key_banned']  or\
                     infobox[key] in maps['value_banned'] or \
                     '<!--' in infobox[key]:
                    continue

                ## Key cleaning
                new_key = key_map(new_key,maps).strip()

                ## Value cleaning
                new_value = infobox[key].replace("'",'').replace('\"','')
                if new_key != 'ad':
                    new_value =  clean_pipes(new_value).strip()
                else:
                    new_value =  remove_brackets_with_text(new_value)
                    if new_value == '':
                        return None
                
                if new_key == 'meslek' or  new_key == 'dalı' or  new_key == 'alanı':
                    parts = new_value.replace(' ,',',').replace(', ',',').replace(' , ',',').split(',')
                    parts = map(lambda x: x , parts)
                    if len(parts)>=2:
                        new_value = ', '.join(parts[:-1]) +' ve '+ parts[-1]
                    else:
                        new_value = ', '.join(parts)
                    

                if new_key == 'ulus' or  new_key == 'doğumyeri'  or  new_key == 'ülke':
                    if 'ayraksimge' in new_value:
                        new_value = clean_double_curly_brackets(new_value)
                    new_value =  clean_pipes(new_value).strip()
                    if maps['county_map'].get(new_value,'') !='':
                        new_value = maps['county_map'].get(new_value,'')

                if new_key == 'çağ':
                    new_value = new_value.replace(' felsefesi','')


                if new_key == 'tarz':
                    new_value = new_value.replace('flatlist|','')
                if new_key == 'oyunstili':
                    if new_value.find(';') != -1:
                        new_value = new_value[:new_value.find(';')]
                
                new_value =  clean_tags(new_value)
                new_value =  remove_brackets(new_value)                 
                
                if 'tarih' in new_key:
                    new_value =  date_map(new_value.strip(),maps)
                
                newjson[new_key] = clean_normal_brackets(new_value)#.title()
                
            return newjson
        except Exception as e:
            print e,'[Line: 168 ]'
            return None            
    #################################### ------------ ############################3        
    Bulk_InfoBoxText = step1(Bulk_InfoBoxText)
    Bulk_InfoBoxText = step2(Bulk_InfoBoxText)
    
    Bulk_InfoBoxText = step3(Bulk_InfoBoxText)

    Bulk_InfoBoxText = clean_jsonvalues(Bulk_InfoBoxText)
    
    return Bulk_InfoBoxText





#-----------------------------------------------------------------------------FOR 'clean_jsonvalues'
# . ['adı','isim','ismi','adi','name','karakteradı'] --> 'ad'
def key_map(data,maps ):
    for maped_value in maps['value_maps'].keys():
        if data in maps['value_maps'][maped_value]:
            return maped_value
    return data

def clean_normal_brackets(data):
    pattern= r'\([^\(|\)]*\)'
    try:
        data = re.sub(pattern,"",data)
        return data.strip()
    except Exception as e:
        return data 

# . [[asdasda]], deneme ---> , deneme
def remove_brackets_with_text( data):
    pattern= r'({{([^}}]*)}}|\[\[([^\]\]]*)\]\])'
    try:
        data = re.sub(pattern,"",data)
        return data.strip()
    except Exception as e:
        return data


# . [[Cenova]]{{,}} [[İtalya]] --> Cenova, İtalya
def remove_brackets( data):
    pattern= r'{{|}}|\[\[|\]\]'
    try:
        return re.sub(pattern,"",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
    except:
        return data

# . [[Film yapımcısı|Yapımcı]] , {{Film yönetmeni|Yönetmen}} --->Yapımcı, Yönetmen
def clean_pipes( data):
    pattern  = '(\[\[[^\]\]]*\|([^\]\]]*)\]\])|({{[^}}]*\|([^}}]*)}})' 
    p = re.compile(pattern, re.MULTILINE)
    try:
        if p:
            clean = p.sub(r'\2', data)
            if '|' not in clean:
                return clean
    except Exception as e:
        pass
    pattern  = '({{[^}}]*\|([^}}]*)}})|(\[\[[^\]\]]*\|([^\]\]]*)\]\])' 
    p = re.compile(pattern, re.MULTILINE)
    try:
        if p:
            clean = p.sub(r'\2', data)
            return clean
    except Exception as e:
        return data        


# . <br> --> ,
def clean_tags( data):
    try:
        data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))",", ",data)
    except:
        pass
    try:
        return re.sub(r"<.*?\/>|<.*?</.*?>",", ",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
    except:
        return data
    
# . {{Doğum tarihi|1818|5|5}} ---> 5 Mayıs 1818
# . {{ölüm tarihi ve yaşı|1883|03|14|1818|05|05}} ---> 14 Mart 1883
# . 1162 ---> 1162   
# . 123 ---> 123       
# . 2188 2 2 --->  2 Şubat 2188
# . 2188.2.2 --->  2 Şubat 2188

def test(a,date_value):
    if 'M.Ö. 570' in date_value:
        print 'burda',a
def date_map( date_value,maps ):
    date_value = '{{'+date_value+'}}'
    if '{{bilinmiyor}}' == date_value:
        return None


    
    orj = copy.deepcopy(date_value)
    converted_date = date_value
    try : 
        value = re.findall(r"(\|\d+|\d+)", date_value, re.MULTILINE) ## finding numbersafter pipes
        value = [int(w.replace('|', '')) for w in value]  # clean pipes |
        if len(value) == 3 or len(value) == 4:
            converted_date = "%s %s %s"%(value[2],  maps['month'][value[1]-1],value[0])
            
            return converted_date

        elif len(value) == 6 or len(value) == 7:
            year1 = int(value[0])
            year2 = int(value[0+3])
            if year1 >year2:
                converted_date = "%s %s %s"%(value[2],  maps['month'][value[1]-1],value[0])
                return converted_date
            else:
                converted_date = "%s %s %s"%(value[2+3],  maps['month'][value[1+3]-1],value[0+3])
                
                return converted_date
        elif len(value) == 1:
            if len(str(value[0])) == 4 or len(value[0]) ==3:
                converted_date = str(value[0])
                
                return converted_date
    except Exception as e:
        #print e
        pass
    
    try:
        '''
        value = orj                
        if value.count('-') >0:
            value = value[:value.find('-')]
            if 'M.' in value[:2] or 'MS' == value[:2] or 'MÖ' == value[:2]:
                converted_date = str(value.encode('utf-8'))
                return converted_date
        '''

        value = orj.replace(',',' ').replace('  ',' ').replace('.',' ')
        if len(value.split(' ')) == 3:
            if value.split(' ')[1].decode('utf-8') in  month:
                converted_date =  str(value)
            if value.split(' ')[1].isdigit():
                value = value.split(' ')
                converted_date = str(value[2])+' '+ str( month[value[1]-1]) + ' ' + str(value[0])
            return converted_date            
    except Exception as e:
        #print e
        pass

    #print orj,'burdaa'
    # path {{Ölüm yılı ve yaşı|1428|1401}}
    try:
        reg = "[^\|]*ve yaşı\|(\d*)\|\d*"
        match = re.search(r"[^\|]*ve yaşı\|(\d*)\|\d*", orj)
        return match.group(1)  
    except Exception as e:
        pass


    # path {{death year and age|1978|1924}}
    try:
        reg = "[^\|]*ve yaşı\|(\d*)\|\d*"
        match = re.search(r"[^\|]*year and age\|(\d*)\|\d*", orj)
        return match.group(1)  
    except Exception as e:
        pass
    # path {{19 Ağustos 1905 (79 yaşında)}}
    #      {{13 Haziran 1904 (72-73 yaşlarında)}}
    #{{26 Şubat 1564 (Vaftiz olduğu tarih)}}
    try:
        #reg = "\{\{([^\(|^\)]*)\(\d*\syaşında"
        match = re.search(r"\{\{([^\(|^\)]*)\([^\)|^\(]*\)", orj)
        return match.group(1)  
    except Exception as e:
        pass


    #{{234}}
    try:
        #reg = "\{\{(\d*)\}\}"
        match = re.search(r"\{\{(\d*)\}\}", orj)
        return match.group(1)  
    except Exception as e:
        pass

        
    #{{234 civarı}}
    try:
        #reg = "\{\{(\d*) civarı\}\}"
        match = re.search(r"\{\{(\d*) civarı\}\}", orj)
        return match.group(1)  
    except Exception as e:
        pass
    # {{MÖ 245}}
    # {{M.Ö 234}}
    try:
        #reg = "\{\{[M]|[M.][Ö]|[Ö.]\s(\d*)\}\}"
        match = re.search(r"\{\{M.*Ö.* (\d*)\}\}", orj)
        return 'M.Ö. '+str(match.group(1))
    except Exception as e:
        pass
    try:
        #reg = "\{\{[M]|[M.][Ö]|[Ö.]\s(\d*)\}\}"
        match = re.search(r"\{\{M.*S.* (\d*)\}\}", orj)
        return 'M.S. '+str(match.group(1))
    except Exception as e:
        pass

    if len(orj) > 40:
        return None

    return orj[2:-2]
    #----------------------------------------------
#-----------------------------------------------------------------------------------------


def clean_Bulk_Text( Bulk_Text ):
    # delete '[[Dosya.*]]'
    Bulk_Text = clean_dosya(Bulk_Text)

    print Bulk_Text,'---'
    # . [[asdasda]], deneme ---> , deneme
    Bulk_Text = remove_brackets_with_text(Bulk_Text)
    print Bulk_Text,'---'
    # . [[Cenova]]{{,}} [[İtalya]] --> Cenova, İtalya
    Bulk_Text = remove_brackets(Bulk_Text)
    print Bulk_Text,'---'
    # . [[Film yapımcısı|Yapımcı]] , {{Film yönetmeni|Yönetmen}} --->Yapımcı, Yönetmen
    Bulk_Text = clean_pipes(Bulk_Text)


    print Bulk_Text,'---'
    # delete <.*?>.*?</.*?> TAGS
    Bulk_Text = clean_tags_regex(Bulk_Text)
    print Bulk_Text,'---'
    #  [[ ... | ... ]]
    #Bulk_Text = clean_pipes_in_double_square_brackets(Bulk_Text)     
    print Bulk_Text,'---'
    # delete {{...}} double curly brackets
    #Bulk_Text = clean_double_curly_brackets(Bulk_Text)
    print Bulk_Text,'---'
    # remove ' """ ' and  " ''' " in sentence
    Bulk_Text = clean_triple_quoates(Bulk_Text)
    print Bulk_Text,'---'
    Bulk_Text = clean_unknown(Bulk_Text)
    print Bulk_Text,'---'
    return Bulk_Text

# ----- Little functions

def clean_dosya( data):
    try:
        return re.sub(r"\[\[Dosya.*\]\]","",data)
    except:
        return data
# . [[asdasda]], deneme ---> , deneme
def remove_brackets_with_text(data):
    pattern= r'({{([^}}]*)}}|\[\[([^\]\]]*)\]\])'
    try:
        data = re.sub(pattern,"",data)
        return data.strip()
    except Exception as e:
        return data
# . [[Cenova]]{{,}} [[İtalya]] --> Cenova, İtalya
def remove_brackets(data):
    pattern= r'{{|}}|\[\[|\]\]'
    try:
        return re.sub(pattern,"",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
    except:
        return data

# . [[Film yapımcısı|Yapımcı]] , {{Film yönetmeni|Yönetmen}} --->Yapımcı, Yönetmen
def clean_pipes(data):
    pattern  = '(\[\[[^\]\]]*\|([^\]\]]*)\]\])|({{[^}}]*\|([^}}]*)}})' 
    p = re.compile(pattern, re.MULTILINE)
    try:
        if p:
            clean = p.sub(r'\2', data)
            return clean
    except Exception as e:
        return data

def clean_pipes_in_double_square_brackets( data):
    try:
        return re.sub(r"\[\[[^\[\{]*\|","",data).replace('[','').replace(']','') # \[\[.*?\|
    except:
        return data.replace(']','').replace('[','')        

def clean_tags_regex(data):
    try:
        data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))",", ",data)
    except:
        pass
    try:
        return re.sub(r"<.*?\/>|<.*?</.*?>",", ",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
    except:
        return data      



def clean_double_square_brackets( data):
    # Cancelled for now
    try:
        data = re.sub(r"\(.*\)","",data).replace(']]','') # \(.*\) # \(.*?\[\[[\D].*?\]\].*?\)
    except:
        pass
    try:
        data = data.replace('[[','').replace(']]','')
    except :
        return data

def clean_double_curly_brackets(data):
    try:
        return re.sub(r"\(({{.*?(.|\s).*?}})\)|({{.*?(.|\s).*?}})","",data)
    except:
        return data        

def clean_unknown(data):
    try:
        return infoBox.replace(u'\xa0', u' ')
    except:
        return data
def clean_triple_quoates( data):
    try:
        return data.replace("'''",'').replace("''",'').replace('"','').replace("\'\'\'",'').replace("''",'')
    except:
        return data 


def clean_double_equation_mark( data): #==
    try:
        return re.sub(r"==.*?==","", data)
    except:
        return data

#-------------- for text
def process_bulk_text(text):
    """Clean given input text
        
        Parameters:
            text -> str
                A dirty string that includes xml stuffs
        
        Returns:
            text ->
        
    """
    
    def clean_dosya( data):
        try:
            return re.sub(r"\[\[Dosya.*\]\]","",data)
        except:
            return data
        
    def clean_pipes_in_double_square_brackets( data):
        try:
            return re.sub(r"\[\[[^\[\{]*\|","",data).replace('[','').replace(']','')
        except:
            return data.replace(']','').replace('[','')
        
    def clean_tags_regex(data):
        try:
            data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))","",data)
        except:
            pass
        try:
            return re.sub(r"<.*?>.*</.*?>|<.*?</.*?>|<.*?/>","",data)
        except:
            return data
        
    def clean_double_curly_brackets(data):
        try:
            # This comment is just for backup
            # old version of regex \(({{.*?(.|\s).*?}})\)|({{.*?(.|\s).*?}})
            return re.sub(r"\(({{.*?(.|\s).*?}},|{{.*?(.|\s).*?}};|{{.*?(.|\s).*?}})\)|({{.*?(.|\s).*?}},|{{.*?(.|\s).*?}};|{{.*?(.|\s).*?}})","",data) 
        except:
            return data
    
    def clean_triple_quoates(data):
        try:
            return data.replace("'''",'').replace("''",'').replace('"','')
        except:
            return data
    
    def clean_stars(data):
        try:
            return data.replace("*","")
        except:
            return data

    text = clean_dosya(text) # delete '[[Dosya.*]]'
    text = clean_tags_regex(text) # delete <.*?>.*?</.*?> TAGS
    text = clean_pipes_in_double_square_brackets(text) # [[ <remove this> | <hold this one> ]] 
    text = clean_double_curly_brackets(text) # delete {{...}} double curly brackets
    # clean_round_brackets_except_with_birth_and_death
    text = clean_triple_quoates(text) # remove ' """ ' and  " ''' " in sentence
    text = clean_stars(text) # delete '*' stars in text
    
    if text == '':
        return None
    
    return text

def clean_bulk_text(text):
    if text == None:
        return None    
    elif len(text) < 3 :
        return None
    cleaned_text = process_bulk_text(text).encode('utf-8').decode('utf-8').encode('utf-8')
    if cleaned_text == None:
        return None
    elif len(cleaned_text) < 3:
        return None
    return cleaned_text

def clean_paragraphs(article):
    tmp = []
    if len(article) > 0:
        for paragraph in article:
            try:
                cleanedParagraph = process_bulk_text(paragraph).encode('utf-8').decode('utf-8').encode('utf-8')
            except Exception as e:
                continue
            if cleanedParagraph == None:
                continue
            elif len(cleanedParagraph) < 3:
                continue
            else:
                tmp.append(cleanedParagraph)
                
    return tmp