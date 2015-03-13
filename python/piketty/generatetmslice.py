with open('/Users/tunder/Dropbox/GenreProject/metadata/topicmodelingsample.tsv', encoding = 'utf-8') as f:
	filelines = f.readlines()

with open('/Users/tunder/Dropbox/GenreProject/metadata/tmslice.txt', mode = 'w', encoding = 'utf-8') as f:
	for line in filelines[1:]:
		label = line.split('\t')[0]
		f.write(label + '\n')
