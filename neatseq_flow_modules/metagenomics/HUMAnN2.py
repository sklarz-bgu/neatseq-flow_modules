# -*- coding: UTF-8 -*-
""" 
``HUMAnN2``
--------------------------------

:Authors: Menachem Sklarz
:Affiliation: Bioinformatics core facility
:Organization: National Institute of Biotechnology in the Negev, Ben Gurion University.

.. Note:: This module was developed as part of a study led by Dr. Jacob Moran Gilad

A module for running ``HUMAnN2``:


Requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* fastq files, either forward or single:

    * ``sample_data[<sample>]["fastq.F"]``
    * ``sample_data[<sample>]["fastq.S"]``
    
    

Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Puts the ``HUMAnN2`` output files in:  

    * ``self.sample_data[sample]["HUMAnN2.genefamilies"]`` (Also in ``HUMAnN2.genefamilies.RPK``)
    * ``self.sample_data[sample]["HUMAnN2.pathabundance"]`` (Also in ``HUMAnN2.pathabundance.RPK``)
    * ``self.sample_data[sample]["HUMAnN2.pathcoverage"]``


* If ``humann2_renorm_table`` block is set in params, puts the normalized tables in:

    * ``self.sample_data[sample]["HUMAnN2.genefamilies"]`` (Also in ``HUMAnN2.genefamilies.<units>``, where ``<units>`` is the value passed to ``--units``)
    * ``self.sample_data[sample]["HUMAnN2.pathabundance"]`` (Also in ``HUMAnN2.pathabundance.<units>``, where ``<units>`` is the value passed to ``--units``)

* If ``humann2_join_tables`` block is set in params, puts the joined tables in:
    
    * ``self.sample_data["project_data"]["HUMAnN2.genefamilies"]``
    * ``self.sample_data["project_data"]["HUMAnN2.pathabundance"]``
    * ``self.sample_data["project_data"]["HUMAnN2.pathcoverage"]``

.. Note:: If both ``humann2_renorm_table`` and ``humann2_join_tables`` blocks exist in params, ``humann2_join_tables`` will work on the normalized tables produced by ``humann2_renorm_table``! To join the non-normalized tables, do not normalize the tables by not including a ``humann2_renorm_table`` block.

Parameters that can be set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: 
    :header: "Parameter", "Values", "Comments"
    :widths: 15, 10, 10

    "humann2_join_tables", "", "Block containing ``path`` to ``humann2_join_tables``, and a ``redirects`` block if necessary."
    "humann2_renorm_table", "", "Block containing ``path`` to ``humann2_renorm_table``, and a ``redirects`` block if necessary."
    "protein-database", "uniref50|uniref90", "Protein database used for analysis."

.. Warning:: The ``protein-database`` parameter records the protein database being used: *uniref50* or *uniref90*. It is not used by this module but is required by the downstream module, ``HUMAnN2_further_processing``. If you do not include it, you will not be able to add a ``HUMAnN2_further_processing`` instance for downstream analysis.

Lines for parameter file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::


    HUMAnN2_uniref50_hardtrimmed_reads:
        module: HUMAnN2
        base: Trim_Galore
        script_path: '{Vars.Programs_path.humann2}'
        setenv: PERL5LIB="" mpa_dir=$CONDA_PREFIX/bin
        qsub_params:
            -pe: shared 30
        protein-database:   uniref50
        redirects:
            --gap-fill: 'on'
            --input-format: fastq
            --minpath: 'on'
            --nucleotide-database: '{Vars.databases.humann2.chocophlan}'
            --protein-database: '{Vars.databases.humann2.uniref50}'
            --threads: '30'
        humann2_join_tables:
            path: humann2_join_tables
        humann2_renorm_table:
            path: humann2_renorm_table
            redirects:
                --units: cpm
            
References
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`HUMAnN2 home page <http://huttenhower.sph.harvard.edu/humann2>`_


"""

import os
import sys
import re
from neatseq_flow.PLC_step import Step,AssertionExcept


__author__ = "Menachem Sklarz"
__version__ = "1.6.0"


class Step_HUMAnN2(Step):

    
    def step_specific_init(self):
        """ Called on intiation
            Good place for parameter testing.
            Wrong place for sample data testing
        """
        self.shell = "bash"      # Can be set to "bash" by inheriting instances
        self.file_tag = "HUMAnN2"

        if "--input-format" in list(self.params["redir_params"].keys()):
            self.write_warning("At the moment metaphlan supports only --input-format fastq. Ignoring the value you passed\n")
        
        self.params["redir_params"]["--input-format"] = "fastq"
        
        if "--o-log" in list(self.params["redir_params"].keys()):
            self.write_warning("Ignoring the value you passed for --o-log.\nWill store data in sample specific location\n")

        humann2_dir,main_script = os.path.split(self.params["script_path"])

        for prog_name in ["humann2_join_tables","humann2_renorm_table"]:

            if prog_name+"_path" not in self.params:  # Prog path was not passed. Guessing:
                # 1. humann2_dir is empty, i.e. it is in PATH. prog, therefore, is also in path,
                # hopefully (installed with conda?)
                if humann2_dir == "":
                    self.params[prog_name+"_path"] = prog_name
                    self.write_warning("%s_path not passed. Assuming it is in path"%prog_name)
                # 2. script_path is a path to humann2. Assume prog is installed in same location
                else:
                    self.params[prog_name+"_path"] = os.sep.join([humann2_dir,prog_name])
                    self.write_warning("{prog_name} not passed. Using '{path}' ".
                                       format(prog_name=prog_name,
                                              path=self.params[prog_name+"_path"]))
            else:  # prog path was passed explicitly. Keeping
                pass

        # For backwards compatibility
        if "renorm_table" in self.params:
            raise AssertionExcept("Please use the new 'humann2_renorm_table' method of requesting normalized tables. See docs")
        if "join_tables" in self.params:
            raise AssertionExcept("Please use the new 'humann2_join_tables' method. See docs")

        # # For backwards compatibility
        # if "humann2_renorm_table" not in self.params:
        #     # For backwards compatibility, converting 'renorm_table' string into 'humann2_renorm_table' dict
        #     if "renorm_table" in self.params:
        #         self.params["humann2_renorm_table"] = dict()
        #         # If path explicit. Use. Otherwise, extract from script_path
        #         if "humann2_renorm_table_path" in self.params:
        #             self.params["humann2_renorm_table"]["path"] = self.params["humann2_renorm_table_path"]
        #         else:
        #             humann2_dir, main_script = os.path.split(self.params["script_path"])
        #             self.params["humann2_renorm_table"]["path"] = humann2_dir + "humann2_renorm_table"
        #         # redirects can be either string or dict. Here, using string version
        #         self.params["humann2_renorm_table"]["redirects"] = self.params["renorm_table"]

        # Check renorm_table contains --units
        if "humann2_renorm_table" in self.params:
            if "redirects" not in self.params["humann2_renorm_table"]:
                raise AssertionExcept("Please pass --units parameter in humann2_renorm_table redirects!")
            if not isinstance(self.params["humann2_renorm_table"]["redirects"], dict):
                raise AssertionExcept("humann2_renorm_table redirects must be a dict including the --units parameter !")
            if "--input" in self.params["humann2_renorm_table"]["redirects"] or \
                    "--output" in self.params["humann2_renorm_table"]["redirects"]:
                raise AssertionExcept("Please do not pass --input and --output in humann2_renorm_table redirects!")
            if "--units" not in self.params["humann2_renorm_table"]["redirects"]:
                raise AssertionExcept("Please pass --units parameter in humann2_renorm_table redirects!")

            self.units = self.params["humann2_renorm_table"]["redirects"]["--units"]


        # if "humann2_join_tables" not in self.params:
        #     if "join_tables" in self.params:
        #         self.params["humann2_join_tables"] = dict()
        #         if "humann2_join_tables_path" in self.params:
        #             self.params["humann2_join_tables"]["path"] = self.params["humann2_join_tables_path"]
        #         else:
        #             humann2_dir, main_script = os.path.split(self.params["script_path"])
        #             self.params["humann2_join_tables"]["path"] = humann2_dir + "humann2_join_tables"
        #         self.params["humann2_join_tables"]["redirects"] = self.params["join_tables"]

        if "humann2_join_tables" in self.params:
            if "redirects" in self.params["humann2_join_tables"]:
                if not isinstance(self.params["humann2_join_tables"]["redirects"], dict):
                    raise AssertionExcept("humann2_join_tables redirects must be a dict!")
                if "--input" in self.params["humann2_join_tables"]["redirects"] or \
                        "--output" in self.params["humann2_join_tables"]["redirects"]:
                    raise AssertionExcept("Please do not pass --input and --output in humann2_join_tables redirects!")


    def step_sample_initiation(self):
        """ A place to do initiation stages following setting of sample_data
        """
        if "protein-database" in self.params:
            if self.params["protein-database"] not in ["uniref50","uniref90"]:
                raise AssertionExcept("'protein-database' should be either uniref50 or uniref90")
            self.sample_data["project_data"]["HUMAnN2.prot.db"] = self.params["protein-database"]



        
    def create_spec_wrapping_up_script(self):
        """ Add stuff to check and agglomerate the output data
        """
        
        if "humann2_join_tables" in self.params:

            if "redirects" in self.params["humann2_join_tables"]:
                redirects = " \\\n\t" + " \\\n\t".join(
                    [key + " " + (val if val else "")
                     for key, val
                     in self.params["humann2_join_tables"]["redirects"].items()])
            else:
                redirects = ""

            # Get location of humann2 scripts:
            # humann2_dir,main_script = os.path.split(self.params["script_path"])
            if "humann2_renorm_table" in self.params:
                gene_filename = "genefamilies."+self.units
                pw_filename = "pathabundance."+self.units
            else:
                gene_filename = "genefamilies"
                pw_filename = "pathabundance"

            self.script += """\
# Adding code for normalizing genefamilies and pathabundance tables\n\n
{path} \\
\t-i {dir} \\
\t--search-subdirectories \\
\t--file_name {gene}.tsv \\
\t-o {dir}merged.{gene}.tsv {redirs}

{path} \\
\t-i {dir} \\
\t--search-subdirectories \\
\t--file_name {pw}.tsv \\
\t-o {dir}merged.{pw}.tsv {redirs}

{path} \\
\t-i {dir} \\
\t--search-subdirectories \\
\t--file_name pathcoverage.tsv \\
\t-o {dir}merged.pathcoverage.tsv {redirs}


""".format(path=self.params["humann2_join_tables"]["path"],
           dir = self.base_dir,
           gene= gene_filename,
           pw=pw_filename,
           redirs=redirects)

            self.script += """
# HERE YOU CAN ADD NEW THINGS
            """.format()

            ## Storing in dict and stamping
            self.sample_data["project_data"]["HUMAnN2.genefamilies"] = "{dir}merged.{pw}.tsv".format(dir=self.base_dir,
                                                                                                       pw=gene_filename)
            self.sample_data["project_data"]["HUMAnN2.pathabundance"] = "{dir}merged.{pw}.tsv".format(dir=self.base_dir,
                                                                                                       pw=pw_filename)
            self.sample_data["project_data"]["HUMAnN2.pathcoverage"] = "{dir}merged.pathcoverage.tsv".format(dir=self.base_dir)

            self.stamp_file(self.sample_data["project_data"]["HUMAnN2.genefamilies"])
            self.stamp_file(self.sample_data["project_data"]["HUMAnN2.pathabundance"])
            self.stamp_file(self.sample_data["project_data"]["HUMAnN2.pathcoverage"])

            #
            #
            # # self.sample_data["project_data"]["HUMAnN2." + gene_filename] = "%smerged.%s.tsv" % (self.base_dir,  gene_filename)
            # self.stamp_file(self.sample_data["project_data"]["HUMAnN2." + gene_filename])
            #
            # ## Storing in dict and stamping
            # self.sample_data["project_data"]["HUMAnN2." + pw_filename] = "{dir}merged.{pw}.tsv".format(dir=self.base_dir,
            #                                                                                            pw=pw_filename)
            # self.stamp_file(self.sample_data["project_data"]["HUMAnN2." + pw_filename])
            #
            # ## Storing in dict and stamping
            # self.sample_data["project_data"]["HUMAnN2.pathcoverage"] = "%smerged.pathcoverage.tsv" % (self.base_dir)
            # self.stamp_file(self.sample_data["project_data"]["HUMAnN2.pathcoverage"])

    def build_scripts(self):
        """ This is the actual script building function
            Most, if not all, editing should be done here 
            HOWEVER, DON'T FORGET TO CHANGE THE CLASS NAME AND THE FILENAME!
        """
        
        for sample in self.sample_data["samples"]:      # Getting list of samples out of samples_hash
            
            # Name of specific script:
            self.spec_script_name = self.set_spec_script_name(sample)
            self.script = ""

            # Make a dir for the current sample:
            sample_dir = self.make_folder_for_sample(sample)
            
            # This line should be left before every new script. It sees to local issues.
            # Use the dir it returns as the base_dir for this step.
            use_dir = self.local_start(sample_dir)

            # Define output filename 
            output_filename = "%s_%s" % (sample , self.file_tag)

            # If user passed bowtie2out or biom, change the value to sample specific values:
            # These are then added with redirected params
            if "--o-log" in list(self.params["redir_params"].keys()):
                self.params["redir_params"]["--o-log"] = "%s.log" % output_filename

            # Input file
            if "fastq.F" in self.sample_data[sample] and "fastq.R" in self.sample_data[sample]:
                self.write_warning("PE not defined in HUMAnN2. Using only forward reads.\n")
            if "fastq.F" in self.sample_data[sample]:
                # self.script += "--input %s \\\n\t" % (self.sample_data[sample]["fastq.F"])
                inputf = self.sample_data[sample]["fastq.F"]
            elif "fastq.S" in self.sample_data[sample]:
                inputf = self.sample_data[sample]["fastq.S"]
                # self.script += "--input %s \n\n" % self.sample_data[sample]["fastq.S"]
            else:
                raise AssertionExcept("Are you sure you have fastq files in sample?",sample)

            self.script += """
{const} --output {dir} \\
\t--output-basename {basename} \\
\t--input {inputf}

 
""".format(const=self.get_script_const(),
           dir=use_dir,
           basename=output_filename,
           inputf=inputf)
            

            # self.script += "--output %s \\\n\t" % use_dir
            # self.script += "--output-basename %s\n\n" % output_filename

            
            self.sample_data[sample]["HUMAnN2.genefamilies"] = "%s_genefamilies.tsv" % (sample_dir + output_filename)
            self.sample_data[sample]["HUMAnN2.pathabundance"] = "%s_pathabundance.tsv" % (sample_dir + output_filename)
            self.sample_data[sample]["HUMAnN2.pathcoverage"] = "%s_pathcoverage.tsv" % (sample_dir + output_filename)

            # Storing also as RPK, because default may be overwritten with norm below
            self.sample_data[sample]["HUMAnN2.genefamilies.RPK"] = self.sample_data[sample]["HUMAnN2.genefamilies"]
            self.sample_data[sample]["HUMAnN2.pathabundance.RPK"] = self.sample_data[sample]["HUMAnN2.pathabundance"]

            self.stamp_file(self.sample_data[sample]["HUMAnN2.genefamilies"])
            self.stamp_file(self.sample_data[sample]["HUMAnN2.pathabundance"])
            self.stamp_file(self.sample_data[sample]["HUMAnN2.pathcoverage"])


            if "humann2_renorm_table" in self.params:
                # Adding code for normalization if required
                # Checking redirects exists although in init this was checked already
                if "redirects" in self.params["humann2_renorm_table"]:
                    redirects = " \\\n\t".join(
                        [key + " " + (val if val else "")
                         for key, val
                         in self.params["humann2_renorm_table"]["redirects"].items()])
                else:
                    redirects = ""

                self.script += """\
# Adding code for normalizing genefamilies and pathabundance tables\n\n
{path} \\
\t-i {in_gene} \\
\t-o {out_gene} \\
\t{redirs}

{path} \\
\t-i {in_pw} \\
\t-o {out_pw} \\
\t{redirs}

""".format(path=self.params["humann2_renorm_table"]["path"],
           in_gene="{basefn}_genefamilies.tsv".format(basefn=use_dir + output_filename),
           out_gene="{basefn}_genefamilies.{norm}.tsv".format(basefn=use_dir + output_filename,norm=self.units),
           in_pw="{basefn}_pathabundance.tsv".format(basefn=use_dir + output_filename),
           out_pw="{basefn}_pathabundance.{norm}.tsv".format(basefn=use_dir + output_filename,norm=self.units),
           redirs=redirects)

                # self.sample_data[sample]["HUMAnN2.genefamilies"] = "%s_genefamilies.norm.tsv" % (sample_dir + output_filename)
                # self.sample_data[sample]["HUMAnN2.pathabundance"] = "%s_pathabundance.norm.tsv" % (sample_dir + output_filename)

                self.sample_data[sample]["HUMAnN2.genefamilies"] = \
                    "{basefn}_genefamilies.{norm}.tsv".format(basefn=sample_dir + output_filename,
                                                              norm=self.units)
                self.sample_data[sample]["HUMAnN2.pathabundance"] = \
                    "{basefn}_pathabundance.{norm}.tsv".format(basefn=sample_dir + output_filename,
                                                               norm=self.units)

                self.sample_data[sample]["HUMAnN2.genefamilies."+self.units] = self.sample_data[sample]["HUMAnN2.genefamilies"]
                self.sample_data[sample]["HUMAnN2.pathabundance."+self.units] = self.sample_data[sample]["HUMAnN2.pathabundance"]

                self.stamp_file(self.sample_data[sample]["HUMAnN2.genefamilies"])
                self.stamp_file(self.sample_data[sample]["HUMAnN2.pathabundance"])

            # Move all files from temporary local dir to permanent base_dir
            self.local_finish(use_dir,self.base_dir)       # Sees to copying local files to final destination (and other stuff)
                        
            self.create_low_level_script()

    def make_sample_file_index(self):
        """ Make file containing samples and target file names for use by kraken analysis R script
        """
        
        with open(self.base_dir + "HUMAnN2_files_index.txt", "w") as index_fh:
            index_fh.write("Sample\tHUMAnN2_report\n")
            for sample in self.sample_data["samples"]:      # Getting list of samples out of samples_hash
                index_fh.write("%s\t%s\n" % (sample,self.sample_data[sample]["classification"]))
                
        self.sample_data["project_data"]["HUMAnN2.files_index"] = self.base_dir + "HUMAnN2_files_index.txt"