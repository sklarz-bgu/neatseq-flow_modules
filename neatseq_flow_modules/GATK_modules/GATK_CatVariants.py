#!/fastspace/bioinfo_apps/python-2.7_SL6/bin/python


import os
import sys
from neatseq_flow.PLC_step import Step,AssertionExcept


__author__ = "Michal Gordon"

class Step_GATK_CatVariants(Step):
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

        
       
        # Each iteration must define the following class variables:
        # spec_qsub_name
        # spec_script_name
        # script
######################################################## SNP

        for sample in self.sample_data["samples"]:
            output_file = self.base_dir + sample + "_CatVariants.vcf"
            my_CatVariants_string = """
                    
                    
                    
    echo '\\n---------- Create SNP VariantRecalibrator file -------------\\n'
    %(GATK_path)s \\
        -R %(genome_reference)s \\
    """ % { 
                        "GATK_path" : self.params["script_path"],
                        "genome_reference" : self.params["genome_reference"]
                }      
            for chr in self.params["chrom_list"].split(','):
                chr = chr.strip()

                # Name of specific script:
                my_CatVariants_string = my_CatVariants_string + "    -V " + self.sample_data[sample][chr]["GATK_vcf"] + " \\\n"
            my_CatVariants_string = my_CatVariants_string + "    -out " + output_file + " \n"
            self.script = my_CatVariants_string
    #        print self.script
            self.spec_script_name = self.jid_name_sep.join([self.step,self.name,sample])
            # self.spec_script_name = set_spec_script_name()
            # self.jid_name_sep instead of "_"
            use_dir = self.local_start(self.base_dir)
            self.sample_data[sample]["vcf"] = output_file
            self.stamp_file(self.sample_data[sample]["vcf"])
                
            self.local_finish(use_dir,self.base_dir)

            self.create_low_level_script()
    '''
     java -cp GenomeAnalysisTK.jar org.broadinstitute.gatk.tools.CatVariants \
        -R reference.fasta \
        -V input1.vcf \
        -V input2.vcf \
        -out output.vcf \
        -assumeSorted'''
