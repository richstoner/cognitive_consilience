

from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL
import ftclient
from fileimport.fileimporter import CSVImporter

import json

abstract_head = 'header.html'

# json file containing database (write loading file later)
jsondb = 'combined.json'



if __name__ == "__main__":
	import sys, getpass
	username = sys.argv[1]
	password = getpass.getpass("Enter your password: ")

	token = ClientLogin().authorize(username, password)
	ft_client = ftclient.ClientLoginFTClient(token)

	results = ft_client.query(SQL().showTables())
	print results
    
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

	dbjson = open(jsondb, 'r')
	combined_db = json.load(dbjson)

	jdbkeys = combined_db.keys()


	# create a table
	table = {'testtable':{'ref':'NUMBER', 'abstract':'STRING', 'latlong':'LOCATION'}}
	tableid = int(ft_client.query(SQL().createTable(table)).split("\n")[1])
	print tableid


	min_lat = 0
	max_lat = 0

	min_long = 0
	max_long = 0

	max_x = 0
	max_y = 0

	for key in combined_db.keys():
		tref = combined_db[key]

		print int(key)

		if tref['cx'] > max_x:
			max_x = tref['cx']

		if tref['cy'] > max_y:
			max_y = tref['cy']			

	for key in combined_db.keys():
		tref = combined_db[key]

		print int(key)	



		temp_lat = (tref['cx'] / max_x ) * 170 - 85
		temp_long = (tref['cy'] / max_y ) * 360 - 180

		if temp_lat < min_lat:
			min_lat = temp_lat

		if temp_lat > max_lat:
			max_lat = temp_lat
		
		if temp_long < min_long:
			min_long = temp_long
 
		if temp_long > max_long:
			max_long = temp_long
	
		latlong = '%f, %f' % (temp_lat, temp_long)

		rowid = int(ft_client.query(SQL().insert(tableid, {'ref': int(key), 'abstract': 'testabstract', 'latlong': latlong})).split("\n")[1])


	print '%f %f' % (min_lat, max_lat)
	print '%f %f' % (min_long, max_long)

	





 #    fcsv = open(csv_file_name, 'w')
 #    fcsv.write('x_location\ty_location\ttemp_ref\ttemp_descript\ttemp_url\n')

 #    for key in combined_db.keys():
            
 #        tref = combined_db[key]
        
 #        temp_descript = descript
 #        temp_descript += '<h1>%s</h1>\n' % (str(tref['en_title'][0]))
        
 #        temp_descript += '<h2>EN: '
 #        for a in tref['en_authors']:
 #            temp_descript += '%s, ' % (str(a))
        
 #        temp_descript += '</h2>'
        
 #        #EN: %s</h2>\n' % (str(tref['en_authors'][0]))
 #        temp_descript += '<h2>PM: %s</h2>\n' % (str(tref['pm_authors']))
 #        temp_descript += '<p>%s</p>\n' % (tref['pm_abstract'])
        
 #        temp_url = pubmedbasestr + tref['en_acc']
        
 #        s_descript = temp_descript.encode('utf-8')

 #        temp_x = tref['cx']
 #        temp_y = tref['cy']
 #        temp_ref = key
 #        pprint.pprint(tref)
        
 #        fcsv.write('%f\t%f\t%s\t%s\t%s\n' % (temp_x, temp_y, str(temp_ref), s_descript, str(temp_url)))

 #    fcsv.close()



	# #insert row into table
	# rowid = int(ft_client.query(SQL().insert(tableid, {'strings':'mystring', 'numbers': 12, 'locations':'Palo Alto, CA'})).split("\n")[1])
	# print rowid


