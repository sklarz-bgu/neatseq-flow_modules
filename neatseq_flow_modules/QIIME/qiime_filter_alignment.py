# -*- coding: UTF-8 -*-
""" 
``qiime_filter_alignment``
------------------------------------


:Authors: Menachem Sklarz
:Affiliation: Bioinformatics core facility
:Organization: National Institute of Biotechnology in the Negev, Ben Gurion University.

.. Note:: This module was developed as part of a study led by Dr. Jacob Moran Gilad

A module for running QIIME's ``filter_alignment.py``


Requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* A fasta file in:

    * ``sample_data["fasta.nucl"]``
    

Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Puts the resulting aligned fasta file in: 

    * ``self.sample_data["fasta.nucl"]``
    
* Saves the original unaligned fasta file in: 

    * ``self.sample_data["fasta.aligned_unfiltered"]``
    
    
Parameters that can be set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: 
    :header: "Parameter", "Values", "Comments"
    :widths: 15, 10, 10

    
Lines for parameter file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    q_filt_align_1:
        module: qiime_filter_alignment
        base: q_align_1
        script_path: '{Vars.qiime_path}/filter_alignment.py'
        setenv: {Vars.qiime_env}
    

References
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Caporaso, J.G., Kuczynski, J., Stombaugh, J., Bittinger, K., Bushman, F.D., Costello, E.K., Fierer, N., Peña, A.G., Goodrich, J.K., Gordon, J.I. and Huttley, G.A., 2010. "QIIME allows analysis of high-throughput community sequencing data". *Nature methods*, 7(5), pp.335-336.




"""



import os
import sys
import re
from neatseq_flow.PLC_step import Step,AssertionExcept


__author__ = "Menachem Sklarz"
__version__ = "0.2.0"
class Step_qiime_filter_alignment(Step):
    """ A class that defines a pipeline step name (=instance).
        Most of the class functions are in the super class "Step"
    """
    
    def step_specific_init(self):
        self.shell = "bash"      # Can be set to "bash" by inheriting instances
        self.file_tag = "qiime_filter_alignment"
        
        
    def step_sample_initiation(self):
        """ A place to do initiation stages following setting of sample_data
            Here you should do testing for dependency output. These will NOT exist at initiation of this instance. They are set only following sample_data updating
        """
        
        # # If does not exist 
        # try:
            # self.sample_data["qiime"]
        # except KeyError:
            # raise AssertionExcept("It seems like qiime_demult is the first qiime step. At the moment, it must come after qiime_prep...\n" )

        try:
            self.sample_data["fasta.nucl"]
        except KeyError:
            raise AssertionExcept("fasta dir does not exist.")

        # try:
            # self.links_dir = self.sample_data["otu_table"]
        # except KeyError:
            # raise AssertionExcept("otu table does not exist.\n")

            
     

        
    def create_spec_wrapping_up_script(self):
        """ Add stuff to check and agglomerate the output data
        """
        
        pass
      

    def build_scripts(self):
        

        
        # Name of specific script:
        self.spec_script_name = "_".join([self.step,self.name,self.sample_data["Title"]])

        self.script = ""


    
        # This line should be left before every new script. It sees to local issues.
        # Use the dir it returns as the base_dir for this step.
        use_dir = self.local_start(self.base_dir)

        ####################################################################################################
        ## 
        ## Step 1: build fasta filtering script:

        # if "env" in self.params.keys():         # Add optional environmental variables.
            # self.script += "env %s \\\n\t" % self.params["env"]
        # self.script += self.params["script_path"] + " \\\n\t"
        self.script += self.get_script_env_path()
        for key in self.params["redir_params"].keys():
            self.script += "%s %s \\\n\t" % (key,self.params["redir_params"][key] if self.params["redir_params"][key] else "")
        self.script += "-i %s \\\n\t" % self.sample_data["fasta.nucl"]
        self.script += "-o %s  \n\n" % use_dir

        outfile = os.path.basename(self.sample_data["fasta.nucl"])
        outfile = re.sub("\.(fas|fasta|fna|fa)$","",outfile) + "_pfiltered.fasta"

        self.sample_data["fasta.aligned_unfiltered"] = self.sample_data["fasta.nucl"]
        # self.sample_data["fasta.aligned"] = self.base_dir + outfile
        self.sample_data["fasta.nucl"] = self.base_dir + outfile


        # Move all files from temporary local dir to permanent base_dir
        self.local_finish(use_dir,self.base_dir)       # Sees to copying local files to final destination (and other stuff)
            
        # self.stamp_dir_files(self.base_dir)
   
        
        self.create_low_level_script()
                    
            
            
     