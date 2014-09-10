#!/usr/bin/env python
from __future__ import print_function
from string import Template
from cStringIO import StringIO
from contextlib import closing
import os
import sys
import shutil
import codecs
import glob
import random
import zipfile, zlib
import datetime
import ConfigParser
import argparse
import subprocess, shlex

def warning(*objs):
	print("WARNING: ", *objs, file=sys.stderr)

def error(*objs):
	print("ERROR: ", *objs, file=sys.stderr)
	sys.exit(1)

def main(argv):
	base_dir = os.path.dirname(argv[0])

	# Parse command line arguments
	parser = argparse.ArgumentParser(description='Assigns a set of volumes to different workers for tagging')
	parser.add_argument('--tsv', required=True, type=file, help='The master TSV file')
	parser.add_argument('--vols', required=True, type=file, help='The ZIP file containing the volumes referenced by the TSV file')
	args = parser.parse_args(argv[1:])

	# Parse configuration
	config = ConfigParser.ConfigParser({ 'batch_size': 0, 'reliability_factor': 3 })
	config.read([ os.path.join(base_dir, 'config.ini'), os.path.expanduser('~/.genreproject.ini') ])
	try:
		raters = [ rater.strip() for rater in config.get('config', 'raters').split(',') ]
		batch_size = config.getint('config', 'batch_size')
		reliability_factor = config.getint('config', 'reliability_factor')
		deploy_addr = config.get('remote', 'deploy_addr')
		deploy_path = config.get('remote', 'deploy_path')
		auth_key = os.path.expanduser(config.get('remote', 'auth_key'))
		dashboard_url = config.get('remote', 'dashboard_url')
	except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
		error('Configuration error:', e)

	if not os.path.exists(auth_key):
		error('Missing remote authentication key file', auth_key)

	zip_volume_dir = 'volumes/'
	arfftemplate_name = os.path.join(base_dir, 'arff.template')

	# Get arguments from command line
	tsvfile_name = args.tsv.name
	volumesfile_name = args.vols.name

	# Create an output folder with the same name as the TSV file name, in the current directory
	outputfolder_name = os.path.splitext(os.path.basename(tsvfile_name))[0]
	if os.path.exists(outputfolder_name):
		error('Output folder {} already exists - not overwriting!'.format(outputfolder_name))

	today = datetime.date.today().strftime('%Y%m%d')

	# Sanity check
	if reliability_factor > len(raters):
		error('Cannot have a reliability_factor of {} with {} raters'.format(reliability_factor, len(raters)))

	# Make sure the ARFF template exists
	if not os.path.exists(arfftemplate_name):
		error('Missing ARFF template file', arfftemplate_name)

	print('Creating output folder:', outputfolder_name)
	try:
		os.makedirs(outputfolder_name)
	except Exception as e:
		error('Cannot create output folder {} (Reason: {})'.format(outputfolder_name, e))

	with open(arfftemplate_name, 'r') as arfffile:
		arff_template = Template(arfffile.read())

	assignments = { rater: [] for rater in raters }
	batches = {}

	with codecs.open(tsvfile_name, 'rb', 'utf-8') as tsvfile, zipfile.ZipFile(volumesfile_name, 'r') as volumesfile:
		line_idx = 0
		rater_idx = random.randint(1, len(raters)) - 1   # start with a random rater for fairness :)

		zip_contents = volumesfile.namelist()
		
		for line in tsvfile:
			line_idx += 1

			# Skip header
			if line_idx == 1:
				continue

			try:
				htid, date, genre, author, title = line.split('\t')
			except ValueError as e:
				warning('Error parsing line {} (Reason: {}) -- ignoring line'.format(line_idx, e))
				continue

			# Check that the volume exists in the supplied ZIP file
			if not '{}{}'.format(zip_volume_dir, htid) in zip_contents:
				warning('Missing volume {} in {} -- ignoring volume', htid, volumesfile.filename)
				continue

			for i in range(reliability_factor):
				assignments[raters[rater_idx]].append(htid)
				rater_idx = (rater_idx + 1) % len(raters)

		del zip_contents

		for rater in raters:
			rater_assignment = assignments[rater]
			total_size = len(rater_assignment)
			if batch_size == 0: 
				batch_size = total_size   # if we don't want to batch, assign the entire workload in one batch
			batches[rater] = [ rater_assignment[i : i + batch_size] for i in range(0, total_size, batch_size)]
			
			# Create output folder for rater
			rater_dir = os.path.join(outputfolder_name, rater, 'assigned')
			try:
				os.makedirs(rater_dir)
			except Exception as e:
				error('Cannot create output folder {} (Reason: {})'.format(rater_dir, e))

			for i in range(len(batches[rater])):
				batch = batches[rater][i]
				batchzipfile_name = os.path.join(rater_dir, '{}-{}.zip'.format(today, i+1))
				batch_name = '{}-{}'.format(outputfolder_name, i+1)

				print("Creating:", batchzipfile_name)

				with zipfile.ZipFile(batchzipfile_name, 'w', zipfile.ZIP_DEFLATED) as batchfile, closing(StringIO()) as arff_volumes:
					# Write the batch volumes to the ZIP file
					for volume in batch:
						volume_id = os.path.splitext(volume)[0]
						arff_volumes.write('{},0,0,0,0,0\n'.format(volume_id))

						volumedata = volumesfile.read('{}{}'.format(zip_volume_dir, volume))
						batchfile.writestr('{}/{}'.format(batch_name, volume), volumedata)

					# Generate the ARFF file based on the template and write it to the batch ZIP file
					arffdata = arff_template.safe_substitute(batch_name = batch_name, volumes = arff_volumes.getvalue())
					batchfile.writestr('{}/{}.arff'.format(batch_name, batch_name), arffdata)

		# Print a report
		print('\nWork assignments: (batch size is {})'.format(batch_size))
		for rater in raters:
			print('   {}: \t{} volumes in {} batches'.format(rater, len(assignments[rater]), len(batches[rater])))

		# Copying assigned work to remote server
		print('\nTransfering work to remote server:')
		scp_cmd = 'scp -r -i {} {} {}:{}'.format(auth_key, ' '.join(glob.glob(os.path.join(outputfolder_name, '*'))), deploy_addr, deploy_path)
		try:
			subprocess.check_call(shlex.split(scp_cmd))
		except subprocess.CalledProcessError as e:
			error('Tranfer to remote server failed (Reason: {}) -- output folder NOT removed!'.format(e))

		print('Transfer successful -- removing output folder:', outputfolder_name)
		shutil.rmtree(outputfolder_name)
		print('To see the work dashboard, point your web browser to: {}'.format(dashboard_url))

if __name__ == "__main__":
	main(sys.argv)
