## FileUtils

## a utility
## that reads my standard tab-separated metadata table,
## and returns three data objects: 1) a list of row indexes
## stored in the first column (e.g. volume ids).
## 2) a list of column names, and
## 3) a dictionary-of-dictionaries called table where
## table[columnname][rowindex] = the value of that cell.

def readtsv(filepath):
    with open(filepath, encoding='utf-8') as file:
        filelines = file.readlines()

    header = filelines[0].rstrip()
    fieldnames = header.split('\t')
    numcolumns = len(fieldnames)
    indexfieldname = fieldnames[0]

    table = dict()
    indices = list()
    
    for i in range(1, numcolumns):
        table[fieldnames[i]] = dict()

    for line in filelines[1:]:
        line = line.rstrip()
        fields = line.split('\t')
        rowindex = fields[0]
        indices.append(rowindex)
        for thisfield in range(1, numcolumns):
            thiscolumn = fieldnames[thisfield]
            thisentry = fields[thisfield]
            table[thiscolumn][rowindex] = thisentry

    return indices, fieldnames, table

## REVISED utility
## that reads my standard tab-separated metadata table,
## and returns three data objects: 1) a list of row indexes
## stored in the first column (e.g. volume ids).
## 2) a list of column names, and
## 3) a dictionary-of-dictionaries called table where
## table[columnname][rowindex] = the value of that cell.
## the difference here is thatthe first column, containing
## row indexes, is also returned as a column of the table.
## In the original version, it stupidly wasn't.

def readtsv2(filepath):
    with open(filepath, encoding='utf-8') as file:
        filelines = file.readlines()

    header = filelines[0].rstrip()
    fieldnames = header.split('\t')
    numcolumns = len(fieldnames)
    indexfieldname = fieldnames[0]

    table = dict()
    indices = list()
    
    for i in range(0, numcolumns):
        table[fieldnames[i]] = dict()

    for line in filelines[1:]:
        line = line.rstrip()
        fields = line.split('\t')
        rowindex = fields[0]
        indices.append(rowindex)
        for thisfield in range(0, numcolumns):
            thiscolumn = fieldnames[thisfield]
            thisentry = fields[thisfield]
            table[thiscolumn][rowindex] = thisentry

    return indices, fieldnames, table           

def writetsv(columns, rowindices, table, filepath):

    import os

    headerstring = ""
    numcols = len(columns)
    filebuffer = list()

    ## Only create a header if the file does not yet exist.
    
    if not os.path.exists(filepath):

        headerstring = ""
        for index, column in enumerate(columns):
            headerstring = headerstring + column
            if index < (numcols -1):
                headerstring += '\t'
            else:
                headerstring += '\n'

        filebuffer.append(headerstring)

    for rowindex in rowindices:
        rowstring = ""
        for idx, column in enumerate(columns):
            rowstring += table[column][rowindex]
            if idx < (numcols -1):
                rowstring += '\t'
            else:
                rowstring += '\n'

        filebuffer.append(rowstring)

    with open(filepath, mode='a', encoding = 'utf-8') as file:
        for line in filebuffer:
            file.write(line)

    return len(filebuffer)

def easywritetsv(columns, rowindices, table, filepath):
    '''This version does not assume the table contains a dict for rowindices'''
    firstcolumn = columns[0]
    table[firstcolumn] = dict()
    for idx in rowindices:
        table[firstcolumn][idx] = idx
        
    import os

    headerstring = ""
    numcols = len(columns)
    filebuffer = list()

    ## Only create a header if the file does not yet exist.
    
    if not os.path.exists(filepath):

        headerstring = ""
        for index, column in enumerate(columns):
            headerstring = headerstring + column
            if index < (numcols -1):
                headerstring += '\t'
            else:
                headerstring += '\n'

        filebuffer.append(headerstring)

    for rowindex in rowindices:
        rowstring = ""
        for idx, column in enumerate(columns):
            rowstring += table[column][rowindex]
            if idx < (numcols -1):
                rowstring += '\t'
            else:
                rowstring += '\n'

        filebuffer.append(rowstring)

    with open(filepath, mode='a', encoding = 'utf-8') as file:
        for line in filebuffer:
            file.write(line)

    return len(filebuffer)
       
def pairtreefile(htid):
    ''' Given a dirty htid, returns a clean one that can be used
    as a filename.'''
    
    if ':' in htid or '/' in htid:
        htid = htid.replace(':','+')
        htid = htid.replace('/','=')

    return htid

def pairtreelabel(htid):
    ''' Given a clean htid, returns a dirty one that will match
    the metadata table.'''
    
    if '+' in htid or '=' in htid:
        htid = htid.replace('+',':')
        htid = htid.replace('=','/')

    return htid  
