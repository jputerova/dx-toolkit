#!/usr/bin/env python
# DX_APP_WIZARD_NAME DX_APP_WIZARD_VERSION
# Generated by dx-app-wizard.
#
# Basic execution pattern: Your app will run on a single machine from
# beginning to end.
#
# See http://wiki.dnanexus.com/Building-Your-First-DNAnexus-App for
# instructions on how to modify this file.
#
# DNAnexus Python Bindings (dxpy) documentation:
#   http://autodoc.dnanexus.com/bindings/python/current/

import os
import dxpy

@dxpy.entry_point('main')
def main(DX_APP_WIZARD_INPUT_SIGNATURE):
DX_APP_WIZARD_INITIALIZE_INPUT
DX_APP_WIZARD_DOWNLOAD_ANY_FILES
    # Fill in your application code here.  Dummy output provided
    # below.

    return DX_APP_WIZARD_OUTPUT

dxpy.run()
