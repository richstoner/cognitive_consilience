

from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL
import ftclient
from fileimport.fileimporter import CSVImporter

import json
import math
import urllib2


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
    
 