from lxml import html
import requests
from tabulate import tabulate
import csv
import time

def query(url):
    '''
    input: url (string)
    returns: tuple with ra, dec from site
    Meant for use with STSci coordinate lookup page only (aka not useful outside of this doc)
    '''
    page = requests.get(url)
    tree = html.fromstring(page.text)
    ra = tree.xpath('//input[@name="r"]/@value')
    dec = tree.xpath('//input[@name="d"]/@value')
    return (ra,dec)

def ra_to_deg(sexa):
    '''
    input: sexagesimal string, format 'hh mm ss.sss...'
    output: return decimal degree value (as float)
    '''
    h = float(sexa[0:2])
    m = float(sexa[3:5])
    s = float(sexa[6:])
    hours = h + (m + (s/60))/60
    return hours * 15

def dec_to_deg(sexa):
    '''
    input: declination as string, format 'dd mm ss.ss...'
    output: return decimal degree value (as float)
    '''
    if sexa[0] == '+' or sexa[0] == '-':
        sexa = sexa[1:]
    dd = float(sexa[0:2])
    m = float(sexa[3:5])
    s = float(sexa[6:])
    return dd + (m + (s/60))/60

def coordinate_search(target_list,n=True,not_null=False,degrees=True,NED=True,pretty=True,csv_name='',delay=False):
    '''
    target_list: list of star IDs
    n: boolean, include ID in table if True
    not_null: boolean, do not include IDs without ra and dec if True
    NED: boolean, tries query again with NED database for SIMBAD failures if True
    degrees: give values for ra,dec in decimal degrees
    pretty: boolean, format table for human viewing in console if True and returns
    csv_name: string specifies name of csv file to save table to, does not save if name not changed from ''
    delay: boolean, implements .6s delay between requests to be courteous to the server (results in ~1s per request)
    '''
    
    url = "https://archive.stsci.edu/cgi-bin/dss_form?target="
    end = '&resolver=SIMBAD'
    table = []
    head = ['ra','dec']
    if n:
        head.append('host_id')
        
    #start_time = time.time()
    for target in target_list:
        fix = target.replace('+','%2B')
        spec = fix.replace(' ','+')
        ra,dec = query(url+spec+end)

        #if SIMBAD returns an empty string, try again with NED
        if NED:
            if ra == [''] or dec == ['']:
                ra,dec = query(url+spec+'&resolver=NED')

        if not_null:
            if ra==[''] or dec==['']:
                continue

        #creates a list of lists, with or without target name as specified in args
        if n and degrees:
            table.append([ra_to_deg(ra[0]),dec_to_deg(dec[0]),target])
        elif n:
            table.append([ra[0],dec[0],target])
        elif degrees:
            table.append([ra_to_deg(ra[0]),dec_to_deg(dec[0])])
        else:
            table.append([ra[0],dec[0]])

        #delays for 1 second between requests to be considerate
        if delay:
            time.sleep(0.56)

    #print('--- %s seconds ---' % (time.time() - start_time))

    #outputs location data to csv file
    if csv_name != '':
        filename = csv_name+'.csv'
        whole = [head]
        whole.extend(table)
        with open(filename,'wb') as f:
            writer = csv.writer(f)
            writer.writerows(whole)

    #use tabulate module to output a nice, human-readable table 
    if pretty:
        return tabulate(table,headers=head,tablefmt='orgtbl')
    return
    

def coordinate_prompt(target_list):
    '''
    prompted version of coordinate search for a given target list
    input: target_list, a list of object IDs as strings
    output: return coordinate_search results with given params (returns a tabulate table and/or outputs a csv file)
    '''
    names = raw_input('Include names? Y/n: ')
    if names.lower() == 'n':
        n = False
    else:
        n = True
    nulls = raw_input('Allow null values in rows? Y/n: ')
    if nulls.lower() == 'n':
        not_null = True
    else:
        not_null = False
    deg = raw_input('Output position in degrees? Y/n: ')
    if deg.lower() == 'n':
        degrees = False
    else:
        degrees = True
    again = raw_input('Re-search with NED if SIMBAD does not return results? Y/n: ')
    if again.lower() == 'n':
        ned = False
    else:
        ned = True
    p = raw_input('Return a printable, human-formatted table? Y/n: ')
    if p.lower() == 'n':
        pretty = False
    else:
        pretty = True
    c = raw_input('Output table to a csv file? Y/n: ')
    if c.lower() == 'y':
        csv = raw_input('Pick a name for destination file: ')
    else:
        csv = ''
    d = raw_input('Delay requests to once per second? Y/n: ')
    if d.lower() == 'y':
        delay = True
    else:
        delay = False
    return coordinate_search(target_list,n,not_null,degrees,ned,pretty,csv,delay)
            
