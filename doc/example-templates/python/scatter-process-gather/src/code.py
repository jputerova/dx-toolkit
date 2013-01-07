#!/usr/bin/env python
# coding: utf-8
# DX_APP_WIZARD_NAME DX_APP_WIZARD_VERSION
# Generated by dx-app-wizard.
#
# Scatter-process-gather execution pattern: Your app will split its
# input into multiple pieces, each of which will be processed in
# parallel, after which they are gathered together in some final
# output.
#
# This pattern is very similar to the "parallelized" template.  What
# it does differently is that it formally breaks out the "scatter"
# phase as a separate black-box entry point in the app.  (As a side
# effect, this requires a "map" entry point to call "process" on each
# of the results from the "scatter" phase.)
#
# Note that you can also replace any entry point in this execution
# pattern with an API call to run a separate app or applet.
#
# The following is a Unicode art picture of the flow of execution.
# Each box is an entry point, and vertical lines indicate that the
# entry point connected at the top of the line calls the entry point
# connected at the bottom of the line.  The letters represent the
# different stages in which the input is transformed, e.g. the output
# of the "scatter" entry point ("array:B") is given to the "map" entry
# point as input.  The "map" entry point calls as many "process" entry
# points as there are elements in its array input and gathers the
# results in its array output.
#
#          ┌──────┐
#       A->│ main │->D (output from "postprocess")
#          └┬─┬─┬─┘
#           │ │ │
#          ┌┴──────┐
#       A->│scatter│->array:B
#          └───────┘
#             │ │
#            ┌┴──────────────┐
#   array:B->│      map      │->array:C
#            └─────────┬─┬─┬─┘
#               │      │ . .
#               │     ┌┴──────┐
#               │  B->│process│->C
#               │     └───────┘
#            ┌──┴────────┐
#   array:C->│postprocess│->D
#            └───────────┘
#
# A = original app input, split up by "scatter" into pieces of type B
# B = an input that will be provided to a "process" entry point
# C = the output of a "process" entry point
# D = app output aggregated from the outputs of the "process" entry points
#
# See http://wiki.dnanexus.com/Developer-Portal for documentation and
# tutorials on how to modify this file.
#
# DNAnexus Python Bindings (dxpy) documentation:
#   http://autodoc.dnanexus.com/bindings/python/current/

import os
import dxpy

@dxpy.entry_point("postprocess")
def postprocess(process_outputs, additional_input):
    # This is the "gather" phase which aggregates and performs any
    # additional computation after the "map" (and therefore after all
    # the "process") jobs are done.

    for item in process_outputs:
        print item

    return { "final_output": "postprocess placeholder output" }

@dxpy.entry_point("process")
def process(scattered_input, additional_input):
    # Fill in code here to process the input and create output.

    # As always, you can choose not to return output if the
    # "postprocess" stage does not require any input, e.g. rows have
    # been added to a GTable that has been created in advance.  Just
    # make sure that the "postprocess" job does not run until all
    # "process" jobs have finished by making it wait for "map" to
    # finish using the depends_on argument (this is already done for
    # you in the invocation of the "postprocess" job in "main").

    return { "process_output": "process placeholder output" }

@dxpy.entry_point("map")
def map_entry_point(array_of_scattered_input, process_input):
    # The following calls "process" for each of the items in
    # *array_of_scattered_input*, using as input the item in the
    # array, as well as the rest of the fields in *process_input*.
    process_jobs = []
    for item in array_of_scattered_input:
        process_input["scattered_input"] = item
        process_jobs.append(dxpy.new_dxjob(fn_input=process_input, fn_name="process"))
    return { "process_outputs": [subjob.get_output_ref("process_output") for subjob in process_jobs] }

@dxpy.entry_point("scatter")
def scatter(input_to_scatter):
    # Fill in code here to do whatever is necessary to scatter the
    # input.
    array_of_scattered_input = []

    return { "array_of_scattered_input": array_of_scattered_input }

@dxpy.entry_point("main")
def main(DX_APP_WIZARD_INPUT_SIGNATURE):
DX_APP_WIZARD_INITIALIZE_INPUTDX_APP_WIZARD_DOWNLOAD_ANY_FILES
    # We first create the "scatter" job which will scatter some input
    # (replace with your own input as necessary).
    input_to_scatter = "placeholder value"
    scatter_job = dxpy.new_dxjob(fn_input={ "input_to_scatter": input_to_scatter },
                                 fn_name="scatter")

    # We will want to call "process" on each output of "scatter", so
    # we call the "map" entry point to do so.  We can also provide
    # here additional input that we want each "process" entry point to
    # receive, e.g. a GTable ID to which the "process" function should
    # add rows of data.
    map_input = {
        "array_of_scattered_input": scatter_job.get_output_ref("array_of_scattered_input"),
        "process_input": { "additional_input": "gtable ID, for example" }
        }
    map_job = dxpy.new_dxjob(fn_input=map_input, fn_name="map")

    # Finally, we want the "postprocess" job to run after "map" is
    # done calling "process" on each of its inputs.  Note that a job
    # is marked as "done" only after all of its child jobs are also
    # marked "done".
    postprocess_input = {
        "process_outputs": map_job.get_output_ref("process_outputs"),
        "additional_input": "gtable ID, for example"
        }
    postprocess_job = dxpy.new_dxjob(fn_input=postprocess_input,
                                     fn_name="postprocess",
                                     depends_on=[map_job])

    # If you would like to include any of the output fields from the
    # postprocess_job as the output of your app, you should return it
    # here using a job-based object reference.  If the output field in
    # the postprocess function is called "answer", you can pass that
    # on here as follows:
    #
    # return { "app_output_field": postprocess_job.get_output_ref("final_output"), ...}
    #
    # Tip: you can include in your output at this point any open
    # objects (such as gtables) which will be closed by a job that
    # finishes later.  The system will check to make sure that the
    # output object is closed and will attempt to clone it out as
    # output into the parent container only after all subjobs have
    # finished.

    output = {}
DX_APP_WIZARD_OUTPUT
    return output

dxpy.run()
