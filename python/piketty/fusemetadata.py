# fusemetadata.py

file19 = "/Volumes/TARDIS/work/metadata/19cmetadata.tsv"
with open(file19, encoding='utf-8') as f:
	firstdata = f.readlines()

file20 = "/Volumes/TARDIS/work/metadata/20cMonographMetadata.tsv"
with open(file20, encoding='utf-8') as f:
	seconddata = f.readlines()

merged = "/Volumes/TARDIS/work/metadata/MergedMonographs.tsv"
with open(merged, mode = 'w', encoding = 'utf-8') as f:
	for line in firstdata:
		f.write(line)
	# In the second set, skip header.
	for line in seconddata[1:]:
		f.write(line)

print('Done.')


