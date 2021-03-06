# -*- coding: UTF-8 -*-
""" 
``parse_blast``
-----------------------

:Authors: Menachem Sklarz
:Affiliation: Bioinformatics core facility
:Organization: National Institute of Biotechnology in the Negev, Ben Gurion University.


A module for running ``parse_blast.R``:

The ``parse_blast.R`` script is `available on github <https://github.com/bioinfo-core-BGU/parse_blast>`_.

The program performs the following tasks:

1. It adds annotation to raw tabular BLAST output files,
2. filters the BLAST results by several possible fields,
3. selects the best hit for a group when passed a grouping field and
4. extracts the sequences equivalent to the alignments.



Requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Tabular BLAST result files in the following slots:

    * ``sample_data[<sample>]["blast.nucl|blast.prot"]`` (if ``scope`` set to ``sample``)
    * ``sample_data["project_data"]["blast.nucl|blast.prot"]``           (if ``scope`` set to ``project``)

.. csv-table::
    :header: "File type", "Scope", "Comments"
    :widths: 15, 10, 10

    "``blast.nucl|blast.prot``", "sample/project", "A blast report for a ``nucl`` or ``prot`` query"

.. Attention:: If both ``blast.nucl`` and ``blast.prot`` exist, determine which to use by setting ``fasta2use``. See parameter table below.

Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Puts the parsed report in:

    * ``sample_data[<sample>]["blast.parsed"]``  if ``scope = sample``
    * ``sample_data["project_data"]["blast.parsed"]``            if ``scope = project``

.. csv-table::
    :header: "File type", "Scope", "Comments"
    :widths: 15, 10, 10

    "``blast.parsed``", "sample/project", "Results of parsed blast report"


Parameters that can be set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: 
    :header: "Parameter", "Values", "Comments"
    :widths: 15, 10, 10

    "fasta2use", "``nucl|prot``", "If both nucl and prot BLAST reports exist, you have to specify which one to use with this parameter."
    "blast_merge", "", "Block with ``path`` set to path of ``compare_blast_parsed_reports.R`` and ``redirects`` set to ``compare_blast_parsed_reports.R`` parameters."
    "extract_fasta", "", "Should the script extract a fasta of the hits?"

.. Note::
    ``path`` in ``blast_merge`` block can be left empty. The script will be taken from the same location as the main ``parse_blast.R`` script.
    ``redirects``  in ``blast_merge`` block can be either in string format or the regular block format.

Lines for parameter file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    parse_blast_table:
        module: parse_blast
        base: blst_table
        script_path: {Vars.paths.parse_blast}
        scope: sample
        redirects:
            --columns2keep: '"group name accession qseqid sallseqid evalue bitscore score pident coverage align_len"'
            --dbtable: {Vars.databases.gene_list.table}
            --group_dif_name: # See parse_blast.R documentation for how this is to be specified
            --max_evalue: 1e-7
            --merge_blast: qseqid
            --merge_metadata: # See parse_blast.R documentation for how this is to be specified
            --min_align_len: 30
            --min_coverage: 60
            --names: '"qseqid sallseqid qlen slen qstart qend sstart send length evalue bitscore score pident qframe"'
            --num_hits: 1
        extract_fasta:
        blast_merge:
            path: '{Vars.paths.compare_blast_parsed_reports}'
            redirects:
                --variable:     evalue
                --full_txt_output:


"""



import os
import sys
import re
from neatseq_flow.PLC_step import Step,AssertionExcept


__author__ = "Menachem Sklarz"
__version__ = "1.1.0"

class Step_parse_blast(Step):
    """ A class that defines a pipeline step name (=instance).
    """
    
    
    def step_specific_init(self):
        """ Called on intiation
            Good place for parameter testing.
            Wrong place for sample data testing
        """
        self.shell = "bash"      # Can be set to "bash" by inheriting instances
        self.file_tag = ".blast.parsed"

        if "blast_merge_path" in self.params:
            raise AssertionExcept("Please convert 'blast_merge_path' into the new path/redirects format!")

        if "blast_merge" in self.params:
            try:
                # Testing existence of "path" and, if empty, extracting from main script_path
                if self.params["blast_merge"]["path"] is None:
                    self.params["blast_merge"]["path"] = re.sub(pattern="parse_blast",
                                                                repl="compare_blast_parsed_reports",
                                                                string=self.params["script_path"])
                # Testing existence and stringifying redirects
                if not isinstance(self.params["blast_merge"]["redirects"], str):
                    self.params["blast_merge"]["redirects"] = " \\\n\t".join(
                        [key + " " + (val if val else "")
                         for key, val
                         in self.params["blast_merge"]["redirects"].items()])
                self.params["blast_merge"]["redirects"] = "\n\t{redirs} \\".format(redirs=self.params["blast_merge"]["redirects"])
            except KeyError:
                raise AssertionExcept("Please add path and redirects to `blast_merge` block")

    def step_sample_initiation(self):
        """ A place to do initiation stages following setting of sample_data
        """

        if "scope" in self.params:
          
            if self.params["scope"]=="project":
                if not "blast.nucl" in self.sample_data["project_data"] and not "blast.prot" in self.sample_data["project_data"]:
                    raise AssertionExcept("There are no project BLAST results.\n")
            elif self.params["scope"]=="sample":
                # Checking all samples have a 'blast' file-type in sample_data
                for sample in self.sample_data["samples"]:      # Getting list of samples out of samples_hash
                    if not "blast.nucl" in self.sample_data[sample] and not "blast.prot" in self.sample_data[sample]:
                        raise AssertionExcept("There are no BLAST results.\n" , sample)
            else:
                raise AssertionExcept("'scope' must be either 'sample' or 'project'")
        else:
            raise AssertionExcept("No 'scope' specified.")
                
            
        
    def create_spec_wrapping_up_script(self):
        """ Add stuff to check and agglomerate the output data
        """

        if self.params["scope"] == "sample":

            self.make_sample_file_index()   # see definition below


            if "blast_merge" in self.params:
                # self.params["blast_merge_path"]
                self.script = """\
{path} \\{redirs}
\t--blastind {ind} \\
\t--output {output}
            """.format(path=self.params["blast_merge"]["path"],
                       redirs=self.params["blast_merge"]["redirects"],
                       ind=self.sample_data["project_data"]["BLAST_files_index"],
                       output=self.base_dir + "merged_parsed_blast.tsv")
            else:
                self.write_warning("You did not supply a blast_merge_path parameter. Will not merge blast reports...\n")
                self.script = ""

    
    def build_scripts(self):

        if self.params["scope"] == "project":
            sample_list = ["project_data"]
        elif self.params["scope"] == "sample":
            sample_list = self.sample_data["samples"]
        else:
            raise AssertionExcept("'scope' must be either 'sample' or 'project'")

        for sample in sample_list:      # Getting list of samples out of samples_hash

            # Make a dir for the current sample:
            sample_dir = self.make_folder_for_sample(sample)

            # Name of specific script:
            self.spec_script_name = self.set_spec_script_name(sample)
            self.script = ""

            # This line should be left before every new script. It sees to local issues.
            # Use the dir it returns as the base_dir for this step.
            use_dir = self.local_start(sample_dir)

            # Define output filename
            output_filename = "".join([self.sample_data["Title"] if sample=="project_data" else sample,
                                       self.file_tag])

            # Define query and db files:
            # If db is defined by user, set the query to the correct 'fasta2use'
            # If both nucl and prot appear in blast results
            if "blast.nucl" in self.sample_data[sample] and "blast.prot" in self.sample_data[sample]:
                if "fasta2use" in list(self.params.keys()) and self.params["fasta2use"] in ("nucl","prot"):
                    fasta2use = self.params["fasta2use"]
                    # self.script += "--blast %s \\\n\t" % self.sample_data[sample]["blast"][fasta2use]
                else:
                    raise AssertionExcept("Both 'nucl' and 'prot' blast results were found. Select one by specifying "
                                          "the 'fasta2use' parameter.", sample)
            elif "blast.nucl" in self.sample_data[sample]:
                fasta2use = "nucl"
            elif "blast.prot" in self.sample_data[sample]:
                fasta2use = "prot"
            else:
                raise AssertionExcept("No BLAST Results defined\n")

            self.script += self.get_script_const()
            self.script += "--blast %s \\\n\t" % self.sample_data[sample]["blast." + fasta2use]
            
            # FASTA Extraction
            if "extract_fasta" in self.params:
                try:
                    self.script += "--fasta2extract %s \\\n\t" % self.sample_data[sample]["fasta." + fasta2use]
                except keyError:
                    raise AssertionExcept("In order to extract the fasta sequences, you need to have a fasta file "
                                          "defined with the same type and scope as the blast type.", sample)

            self.script += "--output %s\n\n" % os.sep.join([use_dir,output_filename])

            # Store BLAST result file:
            self.sample_data[sample]["blast.parsed"] = "".join([sample_dir, output_filename])
            self.sample_data[sample]["blast.parsed." + fasta2use] = self.sample_data[sample]["blast.parsed"]
            self.stamp_file(self.sample_data[sample]["blast.parsed"])

            # Wrapping up function. Leave these lines at the end of every iteration:
            self.local_finish(use_dir,self.base_dir)

            self.create_low_level_script()

    def make_sample_file_index(self):
        """ Make file containing samples and target file names for use by kraken analysis R script
        """
        
        if self.params["scope"]=="sample":
            with open(self.base_dir + "parsed_BLAST_files_index.txt", "w") as index_fh:
                index_fh.write("#Sample\tBLAST_report\n")
                for sample in self.sample_data["samples"]:      # Getting list of samples out of samples_hash
                    index_fh.write("%s\t%s\n" % (sample,self.sample_data[sample]["blast.parsed"]))
        else:
            with open(self.base_dir + "parsed_BLAST_files_index.txt", "w") as index_fh:
                index_fh.write("""\
#Sample\tBLAST_report
{project}\t{file}""".format(project=self.sample_data["Title"], file=self.sample_data["project_data"]["blast.parsed"]))
        
        self.sample_data["project_data"]["BLAST_files_index"] = self.base_dir + "parsed_BLAST_files_index.txt"
        
  