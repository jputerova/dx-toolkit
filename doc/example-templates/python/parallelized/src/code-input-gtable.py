#!/usr/bin/env python
# DX_APP_WIZARD_NAME DX_APP_WIZARD_VERSION
# Generated by dx-app-wizard.
#
# Parallelized execution pattern (gtable input): Your app will
# subdivide a large chunk of work (in the form of an existing
# GenomicTable) into multiple pieces that can be processed in parallel
# and independently of each other, followed by a final "postprocess"
# stage that will perform any additional computations as necessary.
#
# See http://wiki.dnanexus.com/Building-Your-First-DNAnexus-App for
# instructions on how to modify this file.
#
# DNAnexus Python Bindings (dxpy) documentation:
#   http://autodoc.dnanexus.com/bindings/python/current/

import os
import dxpy

# This example will break an input GenomicTable into chunks of 10000
# rows each.
row_chunk_size = 10000

@dxpy.entry_point('postprocess')
def postprocess(process_outputs):
    for output in process_outputs:
        pass

    return {}

@dxpy.entry_point('process')
def process(gtable_id, start_row, end_row):
    DX_APP_WIZARD_PARALLELIZED_INPUT = dxpy.DXGTable(gtable_id)

    for row in DX_APP_WIZARD_PARALLELIZED_INPUT.iterate_rows(start_row, end_row):
        # Fill in code here to perform whatever computation is
        # necessary to process the row.
        pass

    # If your subproblem is to compute some value over the rows it was
    # given, you can return it here:
    return {"output": None}

@dxpy.entry_point('main')
def main(DX_APP_WIZARD_INPUT_SIGNATURE):
DX_APP_WIZARD_INITIALIZE_INPUT
DX_APP_WIZARD_DOWNLOAD_ANY_FILES
    # Split your input to be solved by the next stage of your app.
    # The following assumes you are splitting the input by giving,
    # 10000 rows of a GenomicTable per subjob running the
    # "process" entry point.

    # To make this example work, fill in "gtable-xxxx" with the actual
    # ID of the GenomicTable you would like to use as input.  This
    # could either be from an input variable to this function, or
    # perhaps the result of importing data into a gtable you've just
    # created.

    num_rows = DX_APP_WIZARD_PARALLELIZED_INPUT.describe()["length"]

    subjobs = []
    for i in range(num_rows / row_chunk_size + (0 if num_rows % row_chunk_size == 0 else 1)):
        subjob_input = { "gtable_id": DX_APP_WIZARD_PARALLELIZED_INPUT.get_id(),
                         "start_row": row_chunk_size * i,
                         "end_row": min(row_chunk_size * (i + 1), num_rows)}
        subjobs.append(new_dxjob(subjob_input, 'process'))

    # The following line creates the job that will perform the
    # "postprocess" step of your app.  If you give it any inputs that
    # use outputs from the "process" jobs, then it will automatically
    # wait for those jobs to finish before it starts running.  If you
    # do not need to give it any such inputs, you can explicitly state
    # the dependencies to wait for those jobs to finish by setting the
    # "depends_on" field to the list of subjobs to wait for (it
    # accepts either DXJob objects are string job IDs in the list).

    postprocess_job = new_dxjob(fn_input={"process_outputs": [subjob.get_output_ref("output") for subjob in subjobs]},
                                fn_name='postprocess',
                                depends_on=subjobs)

    # If you would like to include any of the output fields from the
    # postprocess_job as the output of your app, you should return it
    # here using a reference.  If the output field is called "answer",
    # you can pass that on here as follows:
    #
    # return {"app_output_field": postprocess_job.get_output_ref("answer"), ...}

    return DX_APP_WIZARD_OUTPUT

dxpy.run()
