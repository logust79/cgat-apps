################################################################################
#
#   MRC FGU Computational Genomics Group
#
#   $Id$
#
#   Copyright (C) 2009 Andreas Heger
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#################################################################################
'''
extract_clade_data.py - 
======================================================

:Author: Andreas Heger
:Release: $Id$
:Date: |today|
:Tags: Python

Purpose
-------

.. todo::
   
   describe purpose of the script.

Usage
-----

Example::

   python extract_clade_data.py --help

Type::

   python extract_clade_data.py --help

for command line help.

Documentation
-------------

Code
----

'''
import os, sys, string, re, getopt, tempfile, time, optparse, math

import Experiment
import Genomics
import IndexedFasta
import IOTools
import pgdb
import Regions

USAGE="""python %s [OPTIONS] 

Version: $Id: extract_clade_data.py 2781 2009-09-10 11:33:14Z andreas $

extract data from clades.

""" % sys.argv[0]

def getMembersOfGroups( dbhandle, groups, options ):

    statement = """
SELECT malis.schema, malis.gene_id, malis.alignment 
FROM 
%(schema)s.%(malis)s AS malis,
%(schema)s.%(members)s AS members
WHERE 
malis.cluster_id = members.cluster_id AND 
malis.gene_id = members.gene_id AND
malis.schema = members.schema AND
members.group_id = '%(group_id)s'""" 

    result = []
    params = {
        'malis': options.table_name_malis,
        'members': options.table_name_members }
    for schema, group_id in groups:
        params["schema"] = schema
        params["group_id"] = str(group_id)
        cc = dbhandle.cursor()
        cc.execute(statement % params )
        result += cc.fetchall()
        cc.close()
        
    return result

if __name__ == "__main__":

    parser = optparse.OptionParser( version = "%prog version: $Id: extract_clade_data.py 2781 2009-09-10 11:33:14Z andreas $", usage = globals()["__doc__"])

    parser.add_option("-g", "--filename-groups", dest="filename_groups", type="string",
                      help="filename with orthologous groups to extract."  )

    parser.set_defaults(
        table_name_malis = "malis_genes_aa",
        table_name_members = "groups_members",
        mode = "sequences",
        filename_groups = None,
        output_format = "fasta",
        separator = "|",
        )

    (options, args) = Experiment.Start( parser, add_psql_options = True )

    ## database handle for connecting to postgres
    dbhandle = pgdb.connect( options.psql_connection )

    if options.filename_groups:
        data, errors = IOTools.ReadList( open(options.filename_groups, "r" ) )
        groups = map( lambda x: x.split( options.separator)[:2], data )
        
        result = getMembersOfGroups( dbhandle, groups, options )
        
        
    if options.output_format == "fasta":
        for schema, gene_id, sequence in result:
            options.stdlog.write(">%s%s%s\n%s\n" % (schema, options.separator,
                                                    gene_id, re.sub("-", "", sequence) ) )


    Experiment.Stop()