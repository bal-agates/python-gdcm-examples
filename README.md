# python-gdcm-examples

Examples with python-gdcm.  The starting point was extracting the Python source from [GDCM 3.0.24](https://github.com/malaterre/GDCM/tree/v3.0.24/Examples/Python).  These were updated for Python 3 and run against a
small number of test cases copied from the pydicom project.

## Test Data

The following test data came from the [pydicom test files](https://github.com/pydicom/pydicom/tree/main/src/pydicom/data/test_files)

* MR_small_padded.dcm: 64x64x1, 16-bit, MONOCHROME2 (black square)
* examples_jpeg2k.dcm: 640x480x3, 8-bit, YBR_RCT
* examples_palette.dcm: 800x350x1, 8-bit, PALETTE (16-bit RGB)
* examples_rgb_color.dcm: 320x240x3, 8-bit, RGB
* examples_ybr_color.dcm: 50*(320x240x3), 8-bit, YBR_FULL_422

The following test is a modified version of *examples_palette.dcm* where the lookup table
has been changed to 8-bit index to 8-bit RGB.

* examples_palette_8.dcm: 800x350x1, 8-bit, PALETTE (8-bit RGB)

## Update source

The following have been updated.

* ConvertNumpy.py.  Notes: 1
* ConvertPIL.py.  Notes: 1
* ConvertMPL.py.  Notes: 1, 2

Notes

1) Does not decode palette.  Type problems with gdcm python.
2) Only displays first image in multi-frame sequence.

## System Info

Testing was done with:

* macOS 14.7.2 arm64
* Python 3.12.8 (MacPorts)
* python-gdcm 3.0.24. (Pip)
* numpy 1.26.4_3 (MacPorts)
* matplotlib 3.10.0
