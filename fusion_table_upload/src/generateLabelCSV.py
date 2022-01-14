

from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL
import ftclient
from fileimport.fileimporter import CSVImporter

import json
import math
import urllib2
import pprint

import csv

csv_filename = 'labelimport.csv'

# json file containing database (write loading file later)

labeldb = 'labels.json'

if __name__ == "__main__":
	import sys, getpass

	f = open(csv_filename, 'wt')

	writer = csv.writer(f)
	writer.writerow( ('ref', 't', 'det', 'nl', 'sd', 'latlong') )

    # default values
	x = 0
	y = 0

	dbjson = open(labeldb, 'r')
	combined_db = json.load(dbjson)
	jdbkeys = combined_db.keys()

	min_lat = 100
	max_lat = -100
	min_long = 1000
	max_long = -1000
	min_x = 1000
	max_x = -1000
	min_y = 1000
	max_y = -1000


	top_bound = 85.1
	left_bound = -179.99
	bottom_bound = 73.83
	right_bound = -89.50

	for key in combined_db.keys():
		tref = combined_db[key]

		width = 5400
		height = 4050

		lat_dif = top_bound - bottom_bound
		long_dif = left_bound - right_bound

		lat_dif_per_px = float(lat_dif) / float(height)
		long_dif_per_px = float(long_dif) / float(width)
		
		temp_x = float(tref['cx'])
		temp_y = height - float(tref['cy'])

		_r = 6378.1
		goog_x = temp_x
		goog_y = (temp_y * 1.874) + 12430

		sin_g = math.sinh(goog_y / _r)
		temp_lat = 180*math.atan(sin_g)/ math.pi
		temp_long = (left_bound - (temp_x * long_dif_per_px))
		latlong = '%f, %f' % (temp_lat, temp_long)
		
		print tref

		detail = tref['detail'].encode('utf-8')

		# if len(detail) > 200:
		# 	detail = detail[:200] + ' ...'

		shortdetail = tref['shortdetail']
		neurolex = tref['neurolex']
		title = tref['title']
		# _id = tref['id']

		
		writer.writerow((str(key) , title, detail, neurolex, shortdetail, latlong))
	
	f.close()	
			# 
			# writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
			# ('ref', 'title', 'authors', 'l_authors', 'abstract', 'species', 'latlong', 'iconName', 'year', 'type', 'secondary', 'keywords', 'l_key', 'circuit') )
		# writer.writerow((str(key), str(title), str(authors), str(authors).lower(), str(abstract), str(species), latlong, iconName, str(year), str(reftype), str(secondary), str(keywords), lowerkeywords,  str(circuit)))

			# rowid = int(ft_client.query(SQL().insert(tableid, {'ref':str(key), 'title': str(title), 'authors':str(authors), 'l_authors': str(authors).lower(), 'l_key':lowerkeywords, 'abstract':str(abstract), 'species':str(species), 'latlong':latlong, 'iconName':iconName, 'year':str(year), 'type':str(reftype), 'secondary':str(secondary), 'keywords':str(keywords), 'circuit':str(circuit)})).split("\n")[1])
		# except urllib2.HTTPError, error:
		# 	# pprint.pprint(tref)
		# 	contents = error.read()
		# 	print contents

		# finally:


	# labelsjson = open(labeldb,'r')
	# label_db = json.load(labelsjson)
	# labelkeys = label_db.keys()
		
	

	# toupload = 'upload.tsv'
	# foutput = open(toupload,'w')

	# foutput.write('ref\t')
	# foutput.write('longdesc\t')
	# foutput.write('label\t')
	# foutput.write('shortname\t')
	# foutput.write('shortdesc\t')
	# foutput.write('neurolex\t')
	# foutput.write('latLng\t')
	# foutput.write('circuit\n')

	# table = {'label':{'ref':'NUMBER', 'longdesc':'STRING', 'label': 'STRING', 'shortname': 'STRING', 'shortdesc':'STRING', 'nif':'STRING', 'neurolex':'STRING', 'neuroname':'STRING','latlong':'LOCATION', 'circuit':'STRING'}}
	# tableid = int(ft_client.query(SQL().createTable(table)).split("\n")[1])
	# print 'Label Table: %s' % (tableid)

	# for key in labelkeys:
	# 	tref = label_db[key]

	# 	width = 5400
	# 	height = 4050
	# 	lat_dif = top_bound - bottom_bound
	# 	long_dif = left_bound - right_bound
	# 	lat_dif_per_px = float(lat_dif) / float(height)
	# 	long_dif_per_px = float(long_dif) / float(width)
	# 	temp_x = float(tref['cx'])
	# 	temp_y = height - float(tref['cy'])
	# 	_r = 6378.1
	# 	goog_x = temp_x
	# 	goog_y = (temp_y * 1.874) + 12430

	# 	sin_g = math.sinh(goog_y / _r)
	# 	temp_lat = 180*math.atan(sin_g)/ math.pi
	# 	temp_long = (left_bound - (temp_x * long_dif_per_px))
	# 	latlong = '%f, %f' % (temp_lat, temp_long)

	# 	print latlong

	# 	label = tref['label'].encode('utf-8')
	# 	circuit = tref['circuit'].encode('utf-8')
	# 	neurolex = tref['neurolex'].encode('utf-8')
	# 	nif = tref['neurolex'].encode('utf-8')
	# 	neuroname = tref['neuronames'].encode('utf-8')
	# 	shortdesc = tref['shortdesc'].encode('utf-8')
	# 	shortname = tref['shortname'].encode('utf-8')
	# 	longdesc = tref['longdesc'].encode('utf-8')

		
	# 	foutput.write('%s\t' % (str(key)))
	# 	foutput.write('%s\t' % longdesc)
	# 	foutput.write('%s\t' % label)
	# 	foutput.write('%s\t' % shortname)
	# 	foutput.write('%s\t' % shortdesc)
	# 	foutput.write('%s\t' % neurolex)
	# 	foutput.write('%s\t' % latlong)
	# 	foutput.write('%s\t' % circuit)
	# 	foutput.write('\n')

	# 	longdesc = ''

	# 	try:
	# 		rowid = int(ft_client.query(SQL().insert(tableid, {'ref':str(key), 'longdesc':longdesc, 'label': str(label), 'shortname':str(shortname), 'shortdesc':str(shortdesc), 'nif':str(nif), 'neurolex':str(neurolex), 'neuroname':str(neuroname), 'latlong':latlong, 'circuit':str(circuit)})).split("\n")[1])
	# 	except urllib2.HTTPError, error:
	# 		contents = error.read()
	# 		print contents
	
	# foutput.close()


#		width = 16094
#		height = 10649
#		5400 4050
# nw (top left)			ne (top, right)
# 85.055, -179.99 			85.055, -89.5
# sw (bottom left)		se (bottom right)
# 73.88, - 179.99			73.88, -89.5

		


# 		# conversion: 1.85771

# 	for i in range(0,11):
# 		for j in range(0,11):
# 			temp_x = width * float(i) / 10
# 			temp_y = (height  * float(j) / 10)
# 			#print '%f %f' % (temp_x, temp_y)

# 			_r = 6378.1
# 			goog_x = temp_x
# 			goog_y = (temp_y * 1.85771) + 12441.78
# 			#print goog_y

# 			sin_g = math.sinh(goog_y / _r)
# #			print sin_g

# 			temp_lat = 180*math.atan(sin_g)/ math.pi


# #			temp_lat = (top_bound - (temp_x * lat_dif_per_px))
# 			temp_long = (left_bound - (temp_x * long_dif_per_px))
# 			# latlong = '%f %f %f' % (temp_y, temp_lat, goog_y)
# 			latlong = '%f, %f' % (temp_lat, temp_long)
# 			print latlong
# 			rowid = int(ft_client.query(SQL().insert(tableid, {'ref': '%d %d' % (i,j) , 'abstract': str(tref['pm_authors']), 'latlong': latlong})).split("\n")[1])
# 	print i
# 	print j







# 		#in google maps -> origin is lat / long = 85, -179
# 		# 				-> size is lat / long = 10, 



# #g(75, -179.0), new google.maps.LatLng(85.00, -90));

# 		temp_y = tref['cy'] / height
# 		temp_x = tref['cx'] / width

# 		if temp_y < min_y:
# 			min_y = temp_y
# 		if temp_y > max_y:
# 			max_y = temp_y

# 		if temp_x < min_x:
# 			min_x =temp_x
# 		if temp_x > max_x:
# 			max_x = temp_x



# 		temp_lat = (top_bound - (tref['cy'] * lat_dif_per_px))
# 		temp_long = (left_bound + (tref['cx'] * long_dif_per_px))


# 		if temp_lat < min_lat:
# 			min_lat = temp_lat
# 		if temp_lat > max_lat:
# 			max_lat = temp_lat

# 		if temp_long < min_long:
# 			min_long = temp_long
# 		if temp_long > max_long:
# 			max_long = temp_long			

# 		latlong = '%f, %f' % (temp_lat, temp_long)
# 		#print latlong


# 		if '4' == key:
# 			print latlong
		
# 		#rowid = int(ft_client.query(SQL().insert(tableid, {'ref': int(key), 'abstract': str(tref['pm_authors']), 'latlong': latlong})).split("\n")[1])


# 	print 'lat %f %f' % (min_lat, max_lat)
# 	print 'long %f %f' % (min_long, max_long)

# 	print 'x %f %f' % (min_x, max_x)
# 	print 'y %f %f' % (min_y, max_y)

	


			#rowid = int(ft_client.query(SQL().insert(tableid, {'ref': int(key), 'abstract': str(tref['pm_authors']), 'latlong': latlong})).split("\n")[1])




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


