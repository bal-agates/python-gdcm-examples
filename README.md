# python-gdcm-examples

Examples with python-gdcm.  The starting point was extracting the Python source
from [GDCM
3.0.24](https://github.com/malaterre/GDCM/tree/v3.0.24/Examples/Python).  These
were updated for Python 3 and run against a small number of test cases.  The main
Python 2 -> 3 change was **print()** statements which I have updated.  Another
was Python 3 changes to differentiate between type **str** and **bytes**.  This
is still causing some problems that need to be fixed in the library.

The other change I made was running "ruff format" on all of the "*.py".  Mostly
this was to make the files more consistent.  The main change here was indent spacing
which varied between files.  In a few places this removed unneeded "()" or did
line folding on long lines.

The most useful examples for me were ConvertNumpy.py, ConvertPIL.py and ConvertMPL.py which
I enhanced some to handle multi-frame datasets.  This still has the problem that
palette images cannot be decoded because of SWIG type errors.

Many of the other programs I do not understand what they are trying to do an
often do not have an appropriate dataset to test.  They have been converted but may
or may not be working properly.

## Main python-gdcm Library Issues

1. Functions returning raw data, like `image.GetBuffer()`, should be returning Python type **bytes**
and not **str**.  OK to still return **str** for C null terminated strings.
2. Type checking errors preventing access in Python to some methods or functions.  This usually
is due to:
    1. C++ function parameters with parameter types of pointer * and refence &.
    2. C++ types that have no direct equivalent in Python (like uint16).

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

The scripts CreateRAWStorage.py, DecompressImage.py, DumbAnonymizer.py and ExtractImageRegion.py
reference dataset "gdcmData/012345.002.050.dcm".

The following came from [gdcmdata](https://sourceforge.net/p/gdcm/gdcmdata/ci/master/tree/).

* DICOMDIR
* 012345.002.050.dcm
* D_CLUNIE_CT1_J2KI.dcm

## Updated Source

The following have been updated for Python 3.  I have run "ruff format" on these to make the
formatting consistent.

* ConvertNumpy.py.  Notes: 1
* ConvertPIL.py.  Notes: 1
* ConvertMPL.py.  Notes: 1, 2
* HelloWorld.py.  Notes: 3
* FindAllPatientName.py.  Notes: 4
* MergeFile.py.  Notes: 5
* ScanDirectory.py.  Notes: 11
* RemovePrivateTags.py.  Notes: 6
* DumbAnonymizer.py.  Notes: 7
* ExtractImageRegion.py.  Notes: 8
* FixCommaBug.py.  Notes: 9
* PrivateDict.py.  Notes: 10
* ReadAndDumpDICOMDIR.py.  Notes: 3
* SortImage.py.  Notes: 11
* WriteBuffer.py.  Notes: 12
* AddPrivateAttribute.py.  Notes: 13
* CreateRawStorage.py.  Notes: 13, 14
* DecompressImage.py.  Notes: 13
* ManipulateSequence.py.  Notes: 18
* NewSequence.py.  Notes: 13
* GetPortionCSAHeader.py.  Notes: 15, 17
* ManipulateFile.py.  Notes: 10
* PhilipsPrivateRescaleInterceptSlope.py.  Notes 10, 15
* PlaySound.py.  Notes 15
* ReWriteSCAsMR.py.  Notes 16

The following all use SetByteStringValue() which is currently uncallable due to type errors:

* AddPrivateAttribute.py
* CreateRAWStorage.py
* DecompressImage.py
* FindAllPatientName.py
* ManipulateSequence.py
* NewSequence.py

I do not have good test case datasets for the following:

* GetPortionCSAHeader.py
* ManipulateFile.py
* ManipulateSequence.py
* PhilipsPrivateRescaleInterceptSlope.py
* PlaySound.py
* ReWriteSCAsMR.py

Notes

1) Does not decode palette.  Python type problems with gdcm LookupTable.decode().
2) By redesign only displays the first couple of image frames in multi-frame
   sequence.
3) Many tests failed on "print(dataset)" with `UnicodeEncodeError: 'utf-8' codec
   can't encode character '\udcf0' in position 1165: surrogates not allowed`.  I
   suspect this is another 'str' vs 'bytes' problem but not sure where.
   Uncommenting the (3) trace commands provided no more info.
4) Runtime error on `de.SetByteStringValue("F*")`. Changing to b"F*" causes
   crash.
5) Ran without errors but I do not understand what this should be doing so have
no idea how to check.  gdcmdiff shows some differences including in the Pixel
Data but the image exported from the merge appears to be the same as file1.
6) No runtimes errors.  gdcmdiff showed at least some private tags removed.
7) Seemed to work.  Reported "Problem with:" on KeepIfExist, GetNumberOfFrames,
   GetPatientOrientation.
8) Ran without problems.  Found test case noted in comments and it produced the
expected output.
9) Ran without problems.  I do not have a test case with comma problem.
Comparing my test case input and output gdcmdiff reported no differences.
10) Ran without errors.  I am not sure if the output is correct.
11) Ran without errors.  I am not sure if the output is correct.  No stdout
after "Sorter:" which seems like a problem?
12) Ran without errors.  I do not have dataset with the specific tag
(0x2005, 0x1132) so no output and not thoroughly tested.  I am not sure what
this is supposed to be doing.  Link in comments was broken.
13) Runtime error with `SetByteStringValue()`
14) Attribute `Testing` in `gdcm.Testing.GetDataRoot()` does not exists.  I
commented out that line and replaced with local testing directory.
15) Need appropriate input dataset.
16) Programmatic error.  The var image used before being set.
17) Line 68, bv is None with my dataset.
18) Fails with `'DataElement' object has no attribute 'GetSequenceOfItems'`

### Typical Error Outputs

``` text
python HelloWorld.py test_data/examples_palette.dcm
Traceback (most recent call last):
  File "/Users/brett/GitHub/python-gdcm-examples/HelloWorld.py", line 48, in <module>
    print(dataset)
UnicodeEncodeError: 'utf-8' codec can't encode characters in position 1742-1744: surrogates not allowed
```

``` text
Traceback (most recent call last):
  File "/Users/brett/GitHub/python-gdcm-examples/FindAllPatientName.py", line 33, in <module>
    de.SetByteStringValue("F*")
  File "/Users/brett/Library/Python/3.12/lib/python/site-packages/_gdcm/gdcmswig.py", line 2902, in SetByteStringValue
    return _gdcmswig.DataElement_SetByteStringValue(self, array)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: in method 'DataElement_SetByteStringValue', argument 2 expected byte string.
```

``` text
Help on method SetByteStringValue in module _gdcm.gdcmswig:

SetByteStringValue(array) method of _gdcm.gdcmswig.DataElement instance
```

``` text
$ python DumbAnonymizer.py test_data/MR_small_padded.dcm anon.dcm
(18, 16) ('Value', 'MySponsorName')
(18, 32) ('Value', 'MyProtocolID')
(18, 33) ('Value', 'MyProtocolName')
(18, 98) ('Value', 'YES')
(18, 99) ('Value', 'MyDeidentificationMethod')
(8, 24) ('Method', 'GenerateMSOPId')
(16, 16) ('Method', 'GetSponsorInitials')
(16, 32) ('Method', 'GetSponsorId')
(18, 48) ('Method', 'GetSiteId')
(18, 49) ('Method', 'GetSiteName')
(18, 64) ('Method', 'GetSponsorId')
(18, 80) ('Method', 'GetTPId')
(24, 34) ('Method', 'KeepIfExist')
Problem with:  KeepIfExist
(24, 4885) ('Method', 'KeepIfExist')
Problem with:  KeepIfExist
(32, 13) ('Method', 'GenerateStudyId')
(32, 14) ('Method', 'GenerateSeriesId')
(32, 4098) ('Method', 'GetNumberOfFrames')
Problem with:  GetNumberOfFrames
(32, 32) ('Method', 'GetPatientOrientation')
Problem with:  GetPatientOrientation
```

``` text
python ManipulateSequence.py test_data/D_CLUNIE_CT1_J2KI.dcm manip_sq.dcm
Traceback (most recent call last):
  File "/Users/brett/GitHub/python-gdcm-examples/ManipulateSequence.py", line 57, in <module>
    sqprcs = prcs.GetSequenceOfItems()
             ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'DataElement' object has no attribute 'GetSequenceOfItems'. Did you mean: 'GetSequenceOfFragments'?
```

## System Info

Testing was done with:

* macOS 14.7.2 arm64
* Python 3.12.8 (MacPorts)
* python-gdcm 3.0.24. (Pip)
* numpy 1.26.4_3 (MacPorts)
* matplotlib 3.10.0
