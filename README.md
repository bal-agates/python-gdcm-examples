# python-gdcm-examples

Examples with python-gdcm.  The original examples came from the [gdcm-3.0.24 examples](https://github.com/malaterre/GDCM/tree/v3.0.24/Examples/Python).  These were updated for Python 3 and run against a
small number of test cases copied from the pydicom project.

## ConvertMPL.py

Display a DICOM image using numpy and matplotlib.  Works with 2D images with
8, 16 and 32 bit data.

Tested with:

``` shell
python ConvertMPL.py pydicom_test_data/examples_jpeg2k.dcm
python ConvertMPL.py pydicom_test_data/examples_palette.dcm
python ConvertMPL.py pydicom_test_data/examples_palette_8.dcm
python ConvertMPL.py pydicom_test_data/examples_rgb_color.dcm
python ConvertMPL.py pydicom_test_data/examples_ybr_color.dcm
python ConvertMPL.py pydicom_test_data/MR_small_padded.dcm
```

Problems with:

* examples_palette.dcm -> palette not decoded   (index -> 8-bit RGB)
* examples_palette_8.dcm -> palette not decoded (index -> 16-bit RGB)

Fails with:

* pydicom_test_data/examples_ybr_color.dcm -> Multi-frame sequence

## System Info

Testing was done with:

* macOS 14.7.2 arm64
* Python 3.12.8 (MacPorts)
* python-gdcm 3.0.24. (Pip)
* numpy 1.26.4_3 (MacPorts)
* matplotlib 3.10.0
