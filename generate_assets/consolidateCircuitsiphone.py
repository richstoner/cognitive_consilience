
import glob
import os
import shutil

filelist = glob.glob('./*')

for each_file in filelist:
    if 'TileGroup' in each_file:
        
        sublist = glob.glob(each_file + '/*.jpg')
        
        for each_subfile in sublist:
            
            basename = each_file.split('Tile')[0]
            # target = basename + 'c_all/' + each_subfile.split('/')[-1]

            tile_params = each_subfile.split('/')[-1].split('-')
            
            scaled = '%d-%d-%d.jpg' % (int(tile_params[0])+3, int(tile_params[1])+2, int(tile_params[2].split('.jpg')[0])+2)
            target = basename + 'c_all/' + scaled

            # cmdstr = 'convert %s -gravity NorthWest -background black -extent 256x256 %s' % (each_subfile, target)
            cmdstr = 'convert %s %s' % (each_subfile, target)
            print cmdstr
            pipe = os.popen(cmdstr)
            for e in pipe:
            	print e


            #
        
        
    