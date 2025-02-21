# So, this is a coffea analysis framework.

## My general workflow is something like this:

### Write all tools in a python file (skims for particle objects in NanoAOD, plotting functions, caculations, etc.)

### Zoom out: Write Processors in a python file (the thing that runs over each slice of a root file, imports and uses the above mentioned tools). 

### Zoom out: Notebooks, where the processor is imported and the preprocessed file(s) (preprocessed file is what points to which NanoAOD files from CMS DAS).

After importing processor and preprocessed files the notebook is where the "analysis" is done. It will run the processor over the specified NanoAOD files (pulled from from CMS DAS), then the results will typically be available as a dictionary.

Results could be counts of objects, calculations of objects, plots of objects, or some other fourth thing I can't think of. Regardless, the bottom of the notebook is where you should access and play with these things, either displaying counts/plots or whatever.
