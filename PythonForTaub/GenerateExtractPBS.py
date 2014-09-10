for i in range (0, 53):
    filepath = '/Users/tunder/Dropbox/PythonScripts/requests/pbs/fic' + str(i) + '.pbs'
    with open(filepath, mode='w', encoding = 'utf-8') as file:
        file.write('#!/bin/bash\n')
        file.write('#PBS -l walltime=10:00:00\n')
        file.write('#PBS -l nodes=1:ppn=12\n')
        file.write('#PBS -N Fiction' + str(i) + '\n')
        file.write('#PBS -q ichass\n')
        file.write('#PBS -m be\n')
        file.write('cd $PBS_O_WORKDIR\n')
        file.write('python3 extract.py -idfile /projects/ichass/usesofscale/hathimeta/pre20cslices/slice' + str(i) + '.txt -g fic -v -sub -rh' + '\n')

