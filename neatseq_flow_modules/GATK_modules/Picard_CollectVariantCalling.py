# -*- coding: UTF-8 -*-

import os
import sys
from neatseq_flow.PLC_step import Step,AssertionExcept


__author__ = "Michal Gordon"
__version__ = "1.6.0"

class Step_Picard_CollectVariantCalling(Step):
    """ A class that defines a pipeline step name (=instance).
    """


    def step_specific_init(self):
        self.shell = "bash"      # Can be set to "bash" by inheriting instances

    def step_sample_initiation(self):
        """ A place to do initiation stages following setting of sample_data
        """
        pass
        
    def create_spec_wrapping_up_script(self):
        """ Add stuff to check and agglomerate the output data
        """
        
        pass
            
            
    
    def build_scripts(self):
        """ This is the actual script building function
            Most, if not all, editing should be done here 
            HOWEVER, DON'T FORGET TO CHANGE THE CLASS NAME AND THE FILENAME!
        """
        
        # Prepare a list to store the qsub names of this steps scripts (will then be put in pipe_data and returned somehow)
        self.qsub_names=[]
        
       
        # Each iteration must define the following class variables:
            # spec_qsub_name
            # spec_script_name
            # script
        use_dir = self.local_start(self.base_dir)

        for chr in self.params["chrom_list"].split(','):
            self.script = ""
            chr = chr.strip()
            self.spec_script_name = self.jid_name_sep.join([self.step,self.name,self.sample_data["Title"],chr])

            input_file = self.sample_data[chr]["vcf"]

        
            DBSNP = self.params["DBSNP"]
            output_CollectVariantCallingMetrics =  use_dir + self.sample_data["Title"] + "CollectVariantCallingMetrics_" + chr + ".txt" 
            my_string = """
                    cd %(dir)s
                    echo '\\n---------- CollectVariantCallingMetrics -------------\\n'
                    %(picard_path)s CollectVariantCallingMetrics \\
                    INPUT=%(input_file)s \\
                    DBSNP=%(DBSNP)s \\
                    OUTPUT=%(dir)s%(output_file)s

                """ % { 
                        "picard_path" : self.params["script_path"],
                        "input_file" : input_file,
                        "DBSNP" : DBSNP,
                        "dir" : use_dir,
                        "output_file" : output_CollectVariantCallingMetrics
                }
                
                
                
            self.script += my_string
            #self.get_script_env_path()
                
                                       
            self.local_finish(use_dir,self.base_dir)

            self.create_low_level_script()

