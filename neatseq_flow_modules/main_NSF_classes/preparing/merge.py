# -*- coding: UTF-8 -*-
"""
``merge`` :sup:`*`
-------------------

"""

import os
import sys
import re
from neatseq_flow.PLC_step import Step,AssertionExcept

import yaml

from pprint import pprint as pp

__author__ = "Menachem Sklarz"
__version__ = "1.6.0"


class Step_merge(Step):
    
    def step_specific_init(self):
        raise AssertionExcept("Module 'merge' has been renamed to 'Import'")
        # self.shell = "bash"      # Can be set to "bash" by inheriting instances
        # self.file_tag = "merge"

        # # TODO: Find a better way for doing this
        # self.conserved_sample_types = ["type","..grouping.."]

        # # Load YAML of file type stored in merge_file_types.yml
        # with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"merge_file_types.yml"),"r") as fileh:
            # try:
                # self.default_src_trg_map = yaml.load("".join(fileh.readlines()),  Loader=yaml.SafeLoader)
            # except yaml.YAMLError as exc:
                # if hasattr(exc, 'problem_mark'):
                    # mark = exc.problem_mark
                    # print("Error position: (%s:%s)" % (mark.line+1, mark.column+1))
                    # print(mark.get_snippet())
                # raise AssertionExcept("Error loading file types index 'merge_file_types.yml'")
            # except:
                # raise AssertionExcept("Error loading file types index 'merge_file_types.yml'")
            
        # # Load YAML of script_paths stored in merge_script_path_types.yml
        # with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"merge_script_path_types.yml"),"r") as fileh:
            # try:
                # self.script_path_map = yaml.load("".join(fileh.readlines()),  Loader=yaml.SafeLoader)
            # except yaml.YAMLError as exc:
                # if hasattr(exc, 'problem_mark'):
                    # mark = exc.problem_mark
                    # print("Error position: (%s:%s)" % (mark.line+1, mark.column+1))
                    # print(mark.get_snippet())
                # raise AssertionExcept("Error loading script_path index 'merge_script_path_types.yml'")
            # except:
                # raise AssertionExcept("Error loading script_path index 'merge_script_path_types.yml'")

    
    # def step_sample_initiation(self):
        # """ Two operations are performed in this function:
            # 1. Creating good lists for both Basic and Advanced modes.
            # 2. Testing the values passed by the user and guessing values where necessary.
        # """

        # # Getting list of possible src values.
        # # This is done for sample and project scope separately.
        # # Used for creating src or testing src list passed by user
        # src = []
        # scope = []
        # # Get list of existing file types in samples file:
        # for sample in self.sample_data["samples"]:
            # sample_src = list(set(self.sample_data[sample].keys()))
            # # if "type" in sample_src:
            # #     sample_src.remove("type")   # 'type' is the type of sample (PE, etc.)
            # # Remove keywords from sample. These are not 'src's.
            # # At the moment, "type" and "..grouping..". Add more when required!
            # sample_src = [src1
                          # for src1
                          # in sample_src
                          # if src1 not in self.conserved_sample_types]
            # sample_scope = ["sample"] * len(sample_src)
            # # If sample data exists, store in 'src' and 'scope'
            # # Do this only if one of the following:
                # # 1. 'scope' is not defined, or 
                # # 2. 'scope' is a None or
                # # 3. 'scope' is a string equal to 'sample' or
                # # 4. 'scope' is a list containing 'sample'.
            # if "scope" not in self.params \
                # or not self.params["scope"] \
                # or (isinstance(self.params["scope"],str) and self.params["scope"] == "sample") \
                # or (isinstance(self.params["scope"],list) and "sample" in self.params["scope"]):
                # src += sample_src
                # scope += sample_scope
        # if "project_data" in self.sample_data:
            # project_src = list(set(self.sample_data["project_data"].keys()))
            # project_scope = ["project"] * len(project_src)
            # # If project data exists, add to 'src' and 'scope'
            # # Do this only if one of the following:
                # # 1. 'scope' is not defined, or
                # # 2. 'scope' is None, or
                # # 2. 'scope' is a string equal to 'project' or
                # # 3. 'scope' is a list containing 'project'.
            # if "scope" not in self.params \
                    # or not self.params["scope"] \
                    # or (isinstance(self.params["scope"],str) and self.params["scope"] == "project") \
                    # or (isinstance(self.params["scope"],list) and "project" in self.params["scope"]):
                # src = src + project_src
                # scope = scope + project_scope

        # # Getting unique pairs of src and scope:
        # uniq_src_scope = list(set(zip(src,scope)))
        # src, scope = list(zip(*uniq_src_scope))
        # src = list(src)
        # scope = list(scope)
        # # src = sample_src + project_src
        # # scope = sample_scope + project_scope

        # # Removing types not in src/scope from sample_data
        # for sample in self.sample_data["samples"]:
            # for src_p in list(self.sample_data[sample].keys()):
                # if src_p in self.conserved_sample_types:  # Not removing 'type'!
                    # continue
                # if (src_p, "sample") not in uniq_src_scope:
                    # del(self.sample_data[sample][src_p])
        # if "project_data" in self.sample_data:
            # sample = "project_data"
            # for src_p in list(self.sample_data[sample].keys()):
                # if src_p in self.conserved_sample_types:   # Not removing 'type'!
                    # continue
                # if (src_p, "project") not in uniq_src_scope:
                    # del(self.sample_data[sample][src_p])

        # # If 'src' is NOT user-defined: (Basic mode)
        # if "src" not in self.params or not self.params["src"]:
            # self.params["src"] = src
            # # For each of the other required lists
            # for param in ["trg","script_path","ext","pipe","scope"]:
                # if param in self.params and self.params[param]:  # list is defined!
                    # if param in ['trg','ext']:
                        # raise AssertionExcept("'src' not specified. Please do not specify '%s'." %param)
                    # else:  # Param is script_path or pipe or scope
                        # if isinstance(self.params[param], str):
                            # # If param is a str, convert it into a list:
                            # self.params[param] = re.split(pattern="\s*,\s*", string=self.params[param])
                            
                        # if isinstance(self.params[param], list):
                            # if len(self.params[param])>1:
                                # raise AssertionExcept("'src' not specified. Please do not specify '%s' as list "
                                                      # "(only string values are accepted)." %param)
                            # else:
                                # self.params[param] = self.params[param] * len(self.params["src"])
                        # else:
                            # raise AssertionExcept("Unrecognized value for '%s'" % param)
                           
                # else:
                    # # 4. If not passed by user, creating list with None. This is so that pipe can be populated by
                    # # automatic file extension recognition
                    # self.params[param] = [None] * len(self.params["src"])
            # # Defining 'scope' (basic mode. user should not pass this. Setting it here)
            # self.params["scope"] = scope

        # else: # 'src' is user-defined (Advanced mode)
            # # Converting 'src' into list
            # if isinstance(self.params['src'], str):
                # self.params['src'] = re.split(pattern="\s*,\s*", string=self.params['src'])
            # if isinstance(self.params['src'], list):
                # pass
            # else:  # src is not a string or a list. What is it???
                # raise AssertionExcept("Unrecognized format in 'src'")
            # for param in ["trg","script_path","ext","pipe","scope"]:
                # if param in self.params and self.params[param]:  # list is defined!

                    # if isinstance(self.params[param], str):
                        # self.params[param] = re.split(pattern="\s*,\s*", string=self.params[param])
                    # if isinstance(self.params[param], list):
                        # if len(self.params[param]) == 1:
                            # self.params[param] = self.params[param] * len(self.params["src"])
                        # elif len(self.params[param]) == len(self.params["src"]):
                            # pass
                        # else:
                            # raise AssertionExcept("Parameter '{param}' must be a single value or a list the length of "
                                                  # "'src'. Put '..guess..' in places to be determined automatically."
                                                  # .format(param=param))
                    # else: # param is not a string or a list. What is it???
                        # raise AssertionExcept("Unrecognized format in '%s'" % param)
                # else:
                    # self.params[param] = [None] * len(self.params["src"])

        # # #---------------------------------------
        # # print(self.get_step_name())
        # # for param in ["script_path","src","trg","ext","pipe","scope"]:
        # #     print(param)
        # #     pp(self.params[param])
        # # #---------------------------------------
        # # sys.exit()
        # # For each src in the list of sources:
        # for src_ind in range(len(self.params["src"])):
            # src = self.params["src"][src_ind]
            # scope = self.params["scope"][src_ind]
            # script_path = self.params["script_path"][src_ind]
            # ext = self.params["ext"][src_ind]
            # # A list of srcs to remove. These are sources that do not exist in samples or projects
            # bad_srcs = []
            # # If 'trg' is not user-defined, guess it from default_src_trg_map.
            # # Sets list in params. Will be done only for first 'src'
            # if not self.params["trg"][src_ind]:
                # if src not in list(self.default_src_trg_map.keys()):
                    # self.write_warning("The following 'src' is  not recognized: {src}. "
                                       # "Setting 'trg' to {trg}".format(src=src,trg=src))
                    # self.params["trg"][src_ind] = src
                # else:
                    # self.params["trg"][src_ind] = self.default_src_trg_map[src][0]
            # # Get the relevant 'trg' from the 'trg' list
            # trg = self.params["trg"][src_ind]
            # # If it is set by user to ..guess.., try guessing it.
            # if trg == "..guess..":
                # try:
                    # self.params["trg"][src_ind] = self.default_src_trg_map[src][0]
                # except KeyError:
                    # raise AssertionExcept("src '{src}' is not recognized. Can't guess 'trg'.".format(src=src))

            # # Guessing 'ext'
            # if self.params["ext"][src_ind] is None:
                # if src not in list(self.default_src_trg_map.keys()):
                    # self.write_warning("The following 'src' is  not recognized: {src}. "
                                       # "Setting 'ext' to {ext}".format(src=src,ext=src.lower()))
                    # self.params["ext"][src_ind] = None  #src.lower()
                # else:
                    # self.params["ext"][src_ind] = self.default_src_trg_map[src][1]
            # # Get the relevant 'ext' from the 'ext' list
            # ext = self.params["ext"][src_ind]
            # # # If it is set by user to ..guess.., try guessing it.
            # # if ext == "..guess..":
            # #     try:
            # #         self.params["ext"][src_ind] = self.default_src_trg_map[src][1]
            # #     except KeyError:
            # #         raise AssertionExcept("src '{src}' is not recognized. Can't guess 'ext'.".format(src=src))

            # # Guessing scope if None
            # if not scope:
                # if all([src in list(self.sample_data[x].keys()) for x in self.sample_data["samples"]]):
                    # self.params["scope"][src_ind] = "sample"
                # elif src in self.sample_data["project_data"]:
                    # self.params["scope"][src_ind] = "project"
                # else:
                    # raise AssertionExcept("{src} does not exist in all samples or in project. Make sure sample "
                                          # "file is correct, or pass 'scope' explicitly.".format(src=src))
            # scope = self.params["scope"][src_ind]

            # # Testing scope and guessing 'script_path':
            # if scope=="sample":
                # for sample in self.sample_data["samples"]:
                    # if src not in self.sample_data[sample]:
                        # self.write_warning("Type '{src}' does not exist for sample '{smp}'!".format(src=src,smp=sample))
                        # bad_srcs += [src_ind]  # Adding bad source to bad_srcs
                # # print "==>", bad_srcs
                # # Guessing script_path:
                # # Get file extensions:
                # if not script_path or script_path == "..guess..":
                    # # Is none or ..guess.. - try guessing
                    # # src_exts is defined as follows: For each sample in samples list,
                    # # get the list of file extensions. Creates a list of lists.
                    # src_exts = [[os.path.splitext(filename)[1]
                                 # for filename
                                 # in self.sample_data[sample][src]]
                                # for sample
                                # in self.sample_data["samples"]
                                # if src in self.sample_data[sample]]

                    # # TODO: src_exts can be empty if assuming sample scope but no files exist!

                    # if src_exts:

                        # # Flatten the list of lists, and uniqify:
                        # src_exts = list(set([item for sublist in src_exts for item in sublist]))
                        # if len(src_exts)>1:
                            # # Will be determined in the script building stage
                            # pass
                        # else:
                            # # Convert set to string:
                            # src_exts = src_exts[0]
                            # if src_exts not in list(self.script_path_map.keys()):
                                # raise AssertionExcept("Unidentified extension in source '{src}' ({ext}). Can't guess "
                                                      # "'script_path'".format(src=src, ext=src_exts))
                            # else:
                                # if isinstance(self.script_path_map[src_exts],list):
                                    # self.params["script_path"][src_ind] = self.script_path_map[src_exts][0]
                                    # self.params["pipe"][src_ind] = self.script_path_map[src_exts][1]
                                # else:
                                    # self.params["script_path"][src_ind] = self.script_path_map[src_exts]

            # elif scope=="project":
                # if src not in self.sample_data["project_data"]:
                    # self.write_warning("Type '{src}' does not exist in project data!".format(src=src))
                    # bad_srcs += [src_ind]  # Adding bad source to bad_srcs

                # # Guessing script_path:
                # # Get file extensions:
                # if not script_path or script_path == "..guess..":
                    # # Is none or ..guess.. - try guessing
                    # src_exts = list(set([os.path.splitext(filename)[1] for filename in self.sample_data["project_data"][src]]))
                    # if len(src_exts)>1:
                        # raise AssertionExcept("More than one file extension in source '{src}' for project ({ext}). "
                                              # "Can't guess 'script_path'".format(src=src, ext=", ".join(src_exts)))
                    # # Convert set to string:
                    # src_exts = src_exts[0]
                    # if src_exts not in list(self.script_path_map.keys()):
                        # raise AssertionExcept("Unidentified extension in source '{src}' for project ({ext}). "
                                              # "Can't guess 'script_path'".format(src=src, ext=src_exts))
                    # else:
                        # if isinstance(self.script_path_map[src_exts],list):
                            # self.params["script_path"][src_ind] = self.script_path_map[src_exts][0]
                            # self.params["pipe"][src_ind] = self.script_path_map[src_exts][1]
                        # else:
                            # self.params["script_path"][src_ind] = self.script_path_map[src_exts]
                                    
            # else:
                # raise AssertionExcept("'scope' must be either 'sample' or 'project'")

        # # # ---------------------------------------
        # # for param in ["script_path","src","trg","ext","pipe","scope"]:
        # #     print(param)
        # #     # self.params[param] = [i for j, i in enumerate(self.params[param]) if j not in bad_srcs]
        # #     self.params[param] = [i for j, i in enumerate(self.params[param]) ]
        # #     pp(self.params[param])
        # # print(bad_srcs)
        # # # ---------------------------------------
        # # sys.exit()

    # def create_spec_wrapping_up_script(self):
        # """ Add stuff to check and agglomerate the output data
        # """
        
        # pass
    
    # def build_scripts(self):

        # for scope_ind in range(len(self.params["scope"])):
            # src = self.params["src"][scope_ind]
            # scope = self.params["scope"][scope_ind]
            # trg = self.params["trg"][scope_ind]
            # ext = self.params["ext"][scope_ind]
            # script_path = self.params["script_path"][scope_ind]
            # pipe = self.params["pipe"][scope_ind]

            # for temparam in "src scope".split(" "):
                # if self.params[temparam][scope_ind] == "..guess..":
                    # raise AssertionExcept("..guess.. in '{param}' not yet supported".format(param=temparam))

                # # Set list of samples to go over. Either self.sample_data["samples"] for sample scope
            # # or ["project_data"] for project scope
            # if scope == "project":
                # sample_list = ["project_data"]
            # elif scope == "sample":
                # sample_list = self.sample_data["samples"]
            # else:
                # raise AssertionExcept("'scope' must be either 'sample' or 'project'")

            # for sample in sample_list:
                # # General comment: If there is a parallel routine for each direction (forward, reverse), add this loop
                # # if  in self.sample_data[sample].keys():

                # sample_title = sample if sample != "project_data" else self.sample_data["Title"]

                # # The following two may be modified per sample. Therefore, reading them again for each sample
                # script_path = self.params["script_path"][scope_ind]
                # pipe = self.params["pipe"][scope_ind]

                # # src_type not defined for this sample. Move on.
                # if src not in self.sample_data[sample]:
                    # continue

                # if script_path == "..import..":
                    # # if src is a list of length one, import the element, converting into str (hopefully)
                    # if isinstance(self.sample_data[sample][src], list) and len(self.sample_data[sample][src]) == 1:
                        # self.sample_data[sample][trg] = self.sample_data[sample][src][0]
                    # elif isinstance(self.sample_data[sample][src], str):  # Not sure this can happen
                        # self.sample_data[sample][trg] = self.sample_data[sample][src]
                    # else:
                        # self.sample_data[sample][trg] = self.sample_data[sample][src]
                    # continue
                # if script_path == "..skip..":
                    # continue

                # self.spec_script_name = self.jid_name_sep.join([self.step,self.name,sample_title,src])

                # # This line should be left before every new script. It sees to local issues.
                # # Use the dir it returns as the base_dir for this step.
                # use_dir = self.local_start(self.base_dir)

                # if not script_path or script_path == "..guess..":
                    # # Not all samples have the same file types. Sample-specific guessing...

                    # src_exts = list(set([os.path.splitext(filename)[1]
                                         # for filename
                                         # in self.sample_data[sample][src]]))
                    # if len(src_exts)>1:
                        # raise AssertionExcept("More than one file extension in source '{src}' ({ext}). "
                                              # "Can't guess 'script_path'".format(src=src, ext=", ".join(src_exts)),
                                              # sample=sample)
                    # # Convert set to string:
                    # src_exts = src_exts[0]
                    # if src_exts not in list(self.script_path_map.keys()):
                        # raise AssertionExcept("Unidentified extension in source '{src}' ({ext}). "
                                              # "Can't guess 'script_path'".format(src=src, ext=src_exts),
                                              # sample=sample)
                    # else:
                        # if isinstance(self.script_path_map[src_exts],list):
                            # script_path = self.script_path_map[src_exts][0]
                            # pipe = self.script_path_map[src_exts][1]
                        # else:
                            # script_path = self.script_path_map[src_exts]

                # # Changing extension to value set in unzipped file in sample file, if the 'zip_ext' column is True
                # # in "merge_script_path_types"
                # first_file_ext = os.path.splitext(self.sample_data[sample][src][0])[1]
                # if not ext or ext == "..guess..":
                    # # If ext is a zipped type, finding the type to unzip to:
                    # # Testing that: (a) ext exists in script_path_map;
                    # # (b) it is a list in script_path_map
                    # # (c) it has at least 3 fields and
                    # # (d) the last field is True
                    # if first_file_ext in self.script_path_map and \
                            # isinstance(self.script_path_map[first_file_ext],list) and \
                            # len(self.script_path_map[first_file_ext])>=3 and \
                            # self.script_path_map[first_file_ext][2]:
                        # first_file = os.path.splitext(self.sample_data[sample][src][0])[0]
                        # if os.path.splitext(first_file)[1]:# and ext == src.lower():
                            # # Add other limits on ext, in case the filename has a "." in it., such as length < 5
                            # ext = os.path.splitext(first_file)[1].lstrip(".")
                    # else:
                        # # Guess based on src type:
                        # try:
                            # ext = self.default_src_trg_map[src][1]
                        # except KeyError:
                            # # Guess based on raw file types:
                            # ext = first_file_ext.lstrip(".")
                            # self.write_warning("src '{src}' is not recognized. Setting 'ext' to type of first file "
                                               # "({ext}).".format(src=src,ext=ext))

                # fq_fn = ".".join([sample_title, src, self.file_tag,ext])

                # # Composing script:
                # self.script = ""
                # self.script += script_path + " \\\n\t"
                # # The following line concatenates all the files in the direction separated by a " "
                # self.script += " ".join(self.sample_data[sample][src])
                # self.script += " \\\n\t"
                # if pipe:  # pipe is not 'None'
                    # self.script += "| {pipe} \\\n\t".format(pipe = pipe)
                # self.script += "> %s%s \n\n"  % (use_dir, fq_fn)

                # # Move all files from temporary local dir to permanent base_dir
                # self.local_finish(use_dir,self.base_dir)

                # # Store file in active file for sample:
                # self.sample_data[sample][trg] = self.base_dir + fq_fn
                # self.stamp_file(self.sample_data[sample][trg])

                # self.create_low_level_script()

