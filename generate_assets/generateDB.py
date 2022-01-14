#!/usr/bin/python
from xml.dom.minidom import parse, parseString

from Bio import Entrez
import pprint
import json
import sqlite3
import sys

# ONLY RUN THIS DURING non-business hours EST
# it will use more than 100 queries to the API, to do the look up

# email needed to pubmed api
Entrez.email = 'rstoner@ucsd.edu'

# reference xml from endnote
xmlfilename = 'Frontiers_Paper_v4.xml'

# sqlite database to be put in iphone app
sqlitedb = 'references.sqlite'

# svg saved from illustrator
anatomysvg = 'cc-refs-final.svg'
labelsvg = 'labels.svg'

# svg generated from python
outputsvg = 'cc-refs-final_out.svg'

# base pubmed query string (needed for sqlite db)
pubmedbasestr = 'http://www.ncbi.nlm.nih.gov/pubmed/'

# file containing all of the style infromation for the abstracts
abstract_head = 'header.html'

# json file containing database (write loading file later)
jsondb = 'combined.json'

# csv file name
csv_file_name = 'combined.csv'


################################################################################
# this builds the reference DB from the endnote xml file
################################################################################
def buildReferenceDB(xmlfilename):
    _referenceDB = {}
    dom1 = parse(xmlfilename) # parse an XML file by name
    
    def handleReferenceXML(ref_xml):    
        records = ref_xml.getElementsByTagName("record")
        #print len(records)
        handleRecords(records)
        
    def handleSingleValue(node, tagname):
        val = []
        nodes = node.getElementsByTagName(tagname)
        for single_node in nodes:
            node_val = single_node.getElementsByTagName("style")
            for vals in node_val:
                val.append(getText(vals.childNodes))
                
        return val
    
    def handleRecords(records):
        ref_count = 0
        
        for ref in records:
            
            rec_number = ref.getElementsByTagName("rec-number")[0]
            
            refset = {}
            #refset['recnumber'] = rec_number
            refset['title'] = handleSingleValue(ref, 'title')
            refset['authors'] = handleSingleValue(ref, 'author')
            refset['acc'] = handleSingleValue(ref, 'accession-num')
            refset['xml_position'] = ref_count
            refset['keywords'] = handleSingleValue(ref,'keyword')
            refset['secondary'] = handleSingleValue(ref, 'secondary-title')
            refset['pages'] = handleSingleValue(ref, 'pages')
            refset['number'] = handleSingleValue(ref, 'number')
            refset['abstract'] = handleSingleValue(ref, 'abstract')
            refset['year'] = handleSingleValue(ref, 'year')

            ref_type_node = ref.getElementsByTagName("ref-type")
            refset['type'] = ref_type_node[0].attributes['name'].value
            # print refset
            ref_count += 1
            #if refset['acc'] != []:
            
            
            _referenceDB[int(getText(rec_number.childNodes))] = refset
            
    handleReferenceXML(dom1)
    
    return _referenceDB

################################################################################
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)#
            
            return ''.join(rc)
            
################################################################################
# parses svg, updates colors, extracts previous value and records location
################################################################################s
def extractReferences(layer):
                    
    svg_refs = {}
    ref_count = 0
    
    subgroups = layer.getElementsByTagName("g")
    
    for subgroup in subgroups:
        
        keys = subgroup.attributes.keys()
        
        for key in keys:
        
            atr = subgroup.attributes[key]
            
            if 'Ref-' in atr.value:
                

                single_ref = {}
                
                # print subgroup.parentNode.parentNode.attributes['id'].value
                circuit_layer = subgroup.parentNode.attributes['id'].value
                print circuit_layer

                # we have a reference group
                subtext = subgroup.getElementsByTagName("text")
                subrect = subgroup.getElementsByTagName("rect")
                
                base_rect = subrect[0]
                species_rect = subrect[1]
                target_rect = subrect[2]
                
                text_box = subtext[0]
                
                try:
                    single_ref['rec_num'] = int(str(text_box.firstChild.data))
                except:
                    # print 'error for key: %s' % (key)
                    single_ref['rec_num'] = -1


                                
                single_ref['cx'] = float(base_rect.attributes['x'].value)
                single_ref['cy'] = float(base_rect.attributes['y'].value)
                
                single_ref['circuit'] = circuit_layer

                single_ref['layer'] = atr.value

                if 'Human' in atr.value:
                    species_rect.attributes['fill'] = '#ff0000'
                    single_ref['species'] = 'human'
                elif 'Primate' in atr.value:
                    species_rect.attributes['fill'] = '#00ff00'
                    single_ref['species'] = 'primate'
                elif 'Mammal' in atr.value:
                    species_rect.attributes['fill'] = '#0000ff'
                    single_ref['species'] = 'mammal'
                else:
                    species_rect.attributes['fill'] = '#ffcc00'
                    single_ref['species'] = 'unknown'
                
                svg_refs[ref_count] = single_ref
       
                ref_count += 1
                
    #pprint.pprint(svg_refs)
    return svg_refs

def relabelSVG(svgfile, combined_db):

    svg_refs = {}
    ref_count = 0
    subgroups = svgfile.getElementsByTagName("g")
    for subgroup in subgroups:
        keys = subgroup.attributes.keys()
        for key in keys:
            atr = subgroup.attributes[key]
            
            if 'Ref-' in atr.value:

                # if '459' in atr.value:
                #     print 'found 459 occurence'


                single_ref = {}
                # print subgroup.parentNode.parentNode.attributes['id'].value
                circuit_layer = subgroup.parentNode.attributes['id'].value
                # print circuit_layer

                # we have a reference group
                subtext = subgroup.getElementsByTagName("text")
                subrect = subgroup.getElementsByTagName("rect")
                
                base_rect = subrect[0]
                species_rect = subrect[1]
                target_rect = subrect[2]
                
                text_box = subtext[0]

                # print combined_db[str(ref_count)]['en_authors'][0][0]
                # print combined_db[str(ref_count)]['en_year'][0][2:]
                # print int(str(text_box.firstChild.data))

                newstring = combined_db[str(ref_count)]['en_authors'][0][0] + combined_db[str(ref_count)]['en_year'][0][2:]
                # print newstring

                text_box.firstChild.data = newstring

                ref_count += 1




def extractLabels(layer):
                    
    svg_refs = {}
    ref_count = 0

    subgroups = layer.getElementsByTagName("circle")
    for subgroup in subgroups:

        single_ref = {}
        single_ref['cx'] = float(subgroup.attributes['cx'].value)
        single_ref['cy'] = float(subgroup.attributes['cy'].value)
        single_ref['id'] = (subgroup.attributes['id'].value)
        single_ref['detail'] = 'description for left view'
        single_ref['shortdetail'] = 'description for window'
        single_ref['title'] = 'title for window'
        single_ref['neurolex'] = 'neurolex link'

        # print subgroup.attributes.keys()


        # single_ref['circuit'] = circuit_layer
        # single_ref['label'] = atr.value
        # single_ref['shortname'] = 'Info window title'
        # single_ref['shortdesc'] = 'Short description of the item selected. Should be approximately 2-3 sentences in length.'
        # single_ref['neurolex'] = '<a href="http://www.neurolex.org">Find in Neurolex</a>'
        # single_ref['neuronames'] = '<a href="http://www.neurolex.org">Find in Neuronames</a>'
        # single_ref['nif'] = '<a href="http://www.neurolex.org">Find in NIF</a>'


        svg_refs[ref_count] = single_ref
       
        ref_count += 1


        # keys = subgroup.attributes.keys()
        # for key in keys:

        #     single_ref = {}



        #     print key
        #     atr = subgroup.attributes[key]
        #     if 'Ref-' in atr.value:
                
                
                
        #         # print subgroup.parentNode.attributes['id'].value
        #         circuit_layer = subgroup.attributes['id'].value
        #         print circuit_layer

        #         # we have a reference group
        #         # subtext = subgroup.getElementsByTagName("text")
        #         # subrect = subgroup.getElementsByTagName("rect")
        # # <circle id="Label-unknown-L4" opacity="0.5" fill="#FFFFFF" stroke="#231F20" cx="298.59" cy="972.693" r="13.329"/>
                
        #         # base_rect = subrect[0]
        #         # species_rect = subrect[1]
        #         # target_rect = subrect[2]
                
        #         # text_box = subtext[0]
                
        #         # try:
        #         #     single_ref['rec_num'] = int(str(text_box.firstChild.data))
        #         # except:
        #         #     # print 'error for key: %s' % (key)
        #         #     single_ref['rec_num'] = -1




                
    #pprint.pprint(svg_refs)
    return svg_refs    



################################################################################
# compares the endnote db against the svg db
# for every svg item, finds corresponding endnote RECORD NUMBER
# if it has na accession #, queries pubmed for abstract, keywords, etc
################################################################################
def crossReference(endnoteDB, svgDB):
    
    summary_stats = {}

    combined_db = {}
    combined_count = 0
    
    svgkeys = svgDB.keys()
    
    for key in svgkeys:
        key_to_find_in_endnote = svgDB[key]['rec_num']
        
        if key_to_find_in_endnote > 0:
            
            # print key
            svg_item = svgDB[key]
            
            try:
                endnote_item = endnoteDB[key_to_find_in_endnote]

            except:

                print '\tError: rec_num from SVG not found in endnoteDB: %d , %s' % (key, svgDB[key]['layer'])
                print svgDB[key]['rec_num']
                print svgDB[key]
                print key_to_find_in_endnote

                endnote_item = {}
                endnote_item['title'] = 'Not Found'
                endnote_item['authors'] = 'Not Found'
                endnote_item['xml_position'] = 'Not Found'


            combined = {}
            combined['species'] = svg_item['species']
            combined['cx'] = svg_item['cx']
            combined['cy'] = svg_item['cy']
            combined['circuit'] = svg_item['circuit']
            combined['svg_key'] = key
            
            
            # try to look it up on pubmed

            combined['pm_authors'] = ''
            combined['pm_abstract'] = ''

            combined['en_title'] = endnote_item['title']
            combined['en_authors'] = endnote_item['authors']
            combined['en_acc'] = endnote_item['acc']
            combined['en_xml_position'] = endnote_item['xml_position']
            combined['en_keywords'] = endnote_item['keywords']
            combined['en_secondary'] = endnote_item['secondary']
            combined['en_pages'] = endnote_item['pages']
            combined['en_volume'] = endnote_item['number']
            combined['en_abstract'] = endnote_item['abstract']
            combined['en_type'] = endnote_item['type']
            combined['en_year'] = endnote_item['year']

            searchid = combined['en_acc']
            # print searchid

            if len(searchid) > 0 and len( combined['en_abstract']) < 10:
                searchid = combined['en_acc']
                
                handle = Entrez.efetch(db="pubmed", id=searchid, rettype="citation", retmode="xml")
                pmstr = handle.read()

                entrezxml = parseString(pmstr)
                author_list = entrezxml.getElementsByTagName('Author')
                authors = []
                
                # for author in author_list:
                    
                #     if len(author.getElementsByTagName('LastName')) > 0:
                #         lastname = author.getElementsByTagName('LastName')[0]
                #     else:
                #         lastname = ''

                #     if len(author.getElementsByTagName('Initials')) > 0:
                #         initial = author.getElementsByTagName('Initials')[0]
                #     else:
                #         initial = ''
                    
                #     if len(author.getElementsByTagName('ForeName')) > 0:
                #         forename = author.getElementsByTagName('ForeName')[0]
                #     else:
                #         forename = ''
                
                #     auth_name =  getText(lastname.childNodes) + ', ' + getText(initial.childNodes)
                #     authors.append(auth_name.encode('utf-8'))

                combined['pm_authors'] = authors

                abstract_list  = entrezxml.getElementsByTagName('AbstractText')
                if len(abstract_list) > 0:
                    abstract = abstract_list[0]
                    abstract_text = getText(abstract.childNodes)

                    # print authors
                    combined['pm_abstract'] = abstract_text
                else:
                    combined['pm_abstract'] = ''
                
            else:
                # print 'error for %s %s' % (combined['svg_key'], searchid)

                if 'Journal' in combined['en_type']:
                    # pprint.pprint(combined)
                    print combined['en_title'][0]
                    print combined['en_authors'][0]
                    print combined['en_year'][0] + '\n'

                combined['en_acc'] = ''
                combined['pm_authors'] = ''
                combined['pm_abstract'] = ''
                
                
            combined['en_key'] = key_to_find_in_endnote
            
            combined_db[combined_count] = combined
            combined_count += 1
            
    return combined_db


################################################################################
# writes combined db to a sqlite database, adding additional style information
# to abstract text
################################################################################
def writeDB(combined_db):
    
    conn = sqlite3.connect(sqlitedb)
    c = conn.cursor()
    
    # default values
    x = 0
    y = 0
    #descript = 'description'
    url = 'http://'
    
    descript = ''
    fhead = open(abstract_head, 'r')
    for line in fhead:
        descript += line
    fhead.close()
    
    try:
        c.execute('''drop table zoom0''')
        c.execute('''create table zoom0 (id INTEGER PRIMARY KEY ASC, journal TEXT, x FLOAT, y FLOAT, ref INTEGER, descript TEXT, url TEXT, species TEXT, authorstring TEXT, title TEXT)''')
    except:
        c.execute('''create table zoom0 (id INTEGER PRIMARY KEY ASC, journal TEXT, x FLOAT, y FLOAT, ref INTEGER, descript TEXT, url TEXT, species TEXT, authorstring TEXT, title TEXT)''')
    
    for key in combined_db.keys():
        
        tref = combined_db[key]
        
        temp_descript = descript
        temp_descript += '<h1>%s</h1>\n' % (str(tref['en_title'][0]))
        
        temp_descript += '<h2>'
        for a in tref['en_authors']:
            temp_descript += '%s, ' % (str(a))
        
        temp_descript += '</h2>'
        # temp_descript += '<br><h2>'

        if len(tref['en_secondary']) > 0:
            # temp_descript += tref['en_secondary'][0] + ',' + tref['en_year'][0]
            journalstr = tref['en_secondary'][0] + ',' + tref['en_year'][0]
        else:
            # temp_descript += tref['en_year'][0]
            journalstr = tref['en_year'][0]
        
        # temp_descript += '</h2>'
        #EN: %s</h2>\n' % (str(tref['en_authors'][0]))
        # temp_descript += '<h2>PM: %s</h2>\n' % (str(tref['pm_authors']))
        temp_descript += '<p>%s</p>\n' % (tref['pm_abstract'])
        
        temp_descript = temp_descript.replace('"', "'")

        title = tref['en_title'][0].replace('"', "'")
        
        if len(tref['en_acc']) > 0:
            temp_url = pubmedbasestr + tref['en_acc'][0]

        else:
            temp_url = pubmedbasestr + tref['en_title'][0]


        keywords = ''
        for a in tref['en_keywords']:
            keywords += '%s, ' % (str(a))
        
        temp_descript += '<p><b>Keywords</b> '
        temp_descript += keywords
        temp_descript += '</p>'


        # temp_url = pubmedbasestr.encode('utf-8')
        temp_species = str(tref['species'])
        authors = ''
        for a in tref['en_authors']:
            authors += '%s ' % (str(a))

        authors = authors
        temp_x = (tref['cx'] / 5400)*16500
        temp_y = (tref['cy'] / 4050)*12375
        temp_ref = key

        # width is 66 pix in native, 202 in ipad space
        # height is 23 pix in native, 70.3 in ipad space

        insert_str = '''insert into zoom0 values (null, "%s", %f,%f,%s,"%s","%s", "%s", "%s", "%s")''' % (journalstr, temp_x, temp_y, temp_ref, temp_descript, temp_url, temp_species, authors.lower(), title)
        
        # print insert_str
        c.execute(insert_str)
    
    conn.commit()
    c.close()

################################################################################
################################################################################

def countUniquesInCombined(combined_db):
    ref_list = []
    for key in combined_db.keys():
        tref = combined_db[key]
        key_to_compare = tref['en_key']
        if key_to_compare not in ref_list:
            ref_list.append(key_to_compare)
    return ref_list


def countUniquesInSVG(svgDB):
    ref_list = []
    ref_dict = {}

    region_list = []
    region_dict = {}

    errorcount = 0

    svgkeys = svgDB.keys()
    
    for key in svgkeys:

        key_to_compare = svgDB[key]['rec_num']
        reference_label = svgDB[key]['layer']


        if len(reference_label.split('-')) < 2:
            print '\tIncorrect split for Label: %s' % (reference_label)
        else:

            region = reference_label.split('-')[1]

            if region not in region_list:
                region_list.append(region)
                region_dict[region] = 1
            else:
                region_dict[region] += 1

        if key_to_compare == -1:
            errorcount += 1

        if key_to_compare not in ref_list:
            ref_list.append(key_to_compare)

            ref_dict[key_to_compare] = 1
        else:
            ref_dict[key_to_compare] += 1


        if str(key_to_compare) in reference_label:
            pass
        else:
            print '\tIncorrect label ref: %d %s' % (key_to_compare, reference_label)


    print 'Unique References in SVG DB: %d' % (len(ref_list))
    print 'Labels without a number: %d' % (errorcount)
    
    # print '\nRegion statistics'
    # pprint.pprint(region_dict)

    # print '\nRec Num statistics'
    # pprint.pprint(ref_dict)

    return ref_list


print "\nCC script"

# build the reference data base
# print "\nParsing Endnote XML"
# referenceDB = buildReferenceDB(xmlfilename)
# print '\tReferences in EndNote XML: %d' % (len(referenceDB))

# print "\nWriting Json Backup"
# dbjson = open('final_reference.json', 'w')
# dbjson.write(json.dumps(referenceDB, indent=4))
# dbjson.close()

# print "\nParsing SVG"
# svg = parse(anatomysvg)
# svg_refs = extractReferences(svg)
# print '\tReferences in Svg File: %d' % (len(svg_refs))

svg = parse(labelsvg)
svg_labels = extractLabels(svg)
pprint.pprint(  svg_labels )

print "\nWriting Json Backup"
dbjson = open('labels.json', 'w')
dbjson.write(json.dumps(svg_labels, indent=4))
dbjson.close()

# print "\nSVG Statistics"
# uniqueSVGRefs = countUniquesInSVG(svg_refs)



# print "\nCross Reference SVG with XML"
# combinedDB = crossReference(referenceDB, svg_refs)

# print "\nWriting Json Backup"
# dbjson = open(jsondb, 'w')
# dbjson.write(json.dumps(combinedDB, indent=4))
# dbjson.close()


dbjson = open(jsondb, 'r')
combined_db = json.load(dbjson)
# relabelSVG(svg, combined_db)

# print "\nWriting Updated SVG"
# outsvg = open(outputsvg, 'w')
# outsvg.write(svg.toxml('utf-8'))
# outsvg.close()

# print "\nWriting Sqlite Backup"
writeDB(combined_db)

# print "\nCombined Statistics"
# uniqueCombinedRefs = countUniquesInCombined(combined_db)
# uniqueCombinedSVG = countUniquesInSVG(svg_refs)

# print '\tUnique References in CrossRef DB: %d\n' % (len(uniqueCombinedRefs))


# remaining 
# print out any that don't have a pmid
# print out any that have an abbreviated abstract
# print out type from endnote





# Ordered (by number) list of unique references used: this is so I can make sure I have check that I haven't missed any
# Any references where the number in the "name" and the number in "text" do not correlate.  If this is the case, then I need to check the reference because the info may be wrong
# List of "area" names used.  The refs are named "Ref_area_species_number".  This is to correlate with color, I know I've put in some mixed names i.e. frontalParietal or All or None, so we want this list to fix the final names and then how to map to colors.
# List of "species" names used. same convention and issue as above.


















