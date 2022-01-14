
import glob
import os
import shutil

directory_list = glob.glob('*')

for each_dir in directory_list:

    if os.path.isdir(each_dir):

        filelist = glob.glob(each_dir + '*')

        target_dir = each_dir + '/tiles_app/'

        print target_dir

        # if os.path.exists(target_dir):
        #     cmdstr = 'rm -rvf %s' % (target_dir)
        #     pipe = os.popen(cmdstr, 'r')
        #     for e in pipe:
        #         print e

        # cmdstr = 'mkdir %s' % (target_dir)
        # pipe = os.popen(cmdstr, 'r')
        # for e in pipe:
        #     print e

        # for zoomifyDir in filelist:
            
        #     to_search = zoomifyDir + '/*'
        #     print to_search

        #     for each_file in glob.glob(to_search):
        #         print each_file
        #         if 'TileGroup' in each_file:
                    
        #             sublist = glob.glob(each_file + '/*.jpg')
                    
        #             for each_subfile in sublist:
                        
        #                 basename = each_file.split('Tile')[0]
        #                 target = basename + 'c_all/' + each_subfile.split('/')[-1]

        #                 tile_params = each_subfile.split('/')[-1].split('-')
                        
        #                 if int(tile_params[0]) < 7:

        #                     scaled = '%d-%d-%d.jpg' % (int(tile_params[0]), int(tile_params[1]), int(tile_params[2].split('.jpg')[0]))

        #                     target = target_dir + scaled

        #                     cmdstr = 'convert %s -quality 50 -extent 256x256 %s' % (each_subfile, target)
        #                     print cmdstr
        #                     pipe = os.popen(cmdstr)
        #                     for e in pipe:
        #                     	print e

        if os.path.exists(target_dir):
            cmdstr = 'zip ./' + each_dir + '.zip' + ' -9 -r ./' + target_dir
            print cmdstr
            pipe = os.popen(cmdstr)
            for e in pipe:
                print e

        
    