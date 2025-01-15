#!/usr/bin/env zsh

# Should capture stdout on good run.

apps=("ConvertNumpy.py" "ConvertPIL.py" "ConvertMPL.py")
# apps=("ConvertNumpy.py")
# Subset of files in test_data.
test_images=("MR_small_padded.dcm" "examples_jpeg2k.dcm" "examples_palette.dcm" "examples_palette_8.dcm" "examples_rgb_color.dcm" "examples_ybr_color.dcm")
for app in $apps
do
    for test_file in ${test_images}
    do
        echo "$ python $app test_data/$test_file"
        python $app test_data/$test_file
    done
    echo
done

# exit 1

setopt verbose

python HelloWorld.py test_data/examples_rgb_color.dcm

python FindAllPatientName.py test_data/examples_rgb_color.dcm

python MergeFile.py test_data/MR_small_padded.dcm test_data/examples_rgb_color.dcm
gdcmdiff test_data/MR_small_padded.dcm merge.dcm

python ScanDirectory.py test_data

python RemovePrivateTags.py test_data/examples_ybr_color.dcm rem_pvt.dcm
gdcmdiff test_data/examples_ybr_color.dcm rem_pvt.dcm

python DumbAnonymizer.py test_data/MR_small_padded.dcm anon.dcm
gdcmdiff test_data/MR_small_padded.dcm anon.dcm

python ExtractImageRegion.py test_data/012345.002.050.dcm
md5 frame.raw

python FixCommaBug.py test_data/012345.002.050.dcm fix.dcm
gdcmdiff test_data/012345.002.050.dcm fix.dcm

python PrivateDict.py

python ReadAndDumpDICOMDIR.py test_data/DICOMDIR

python SortImage.py test_data

python WriteBuffer.py test_data/examples_rgb_color.dcm wbuf

python AddPrivateAttribute.py test_data/examples_rgb_color.dcm addattr.dcm

python DecompressImage.py test_data/examples_ybr_color.dcm j.dcm

python ManipulateSequence.py test_data/examples_ybr_color.dcm manip_sq.dcm
gdcmdiff test_data/examples_ybr_color.dcm manip_sq.dcm

python NewSequence.py test_data/examples_ybr_color.dcm new_sq.dcm
gdcmdiff test_data/examples_ybr_color.dcm new_sq.dcm

python ManipulateFile.py test_data/examples_ybr_color.dcm manip_file.dcm
gdcmdiff test_data/examples_ybr_color.dcm manip_file.dcm

python GetPortionCSAHeader.py test_data/examples_rgb_color.dcm

python ManipulateFile.py test_data/examples_ybr_color.dcm manip_file.dcm
gdcmdiff test_data/examples_ybr_color.dcm manip_file.dcm

python PhilipsPrivateRescaleInterceptSlope.py test_data/examples_ybr_color.dcm
gdcmdiff test_data/examples_ybr_color.dcm philips_rescaled.dcm

python PlaySound.py test_data/examples_ybr_color.dcm

python ReWriteSCAsMR.py test_data/MR_small_padded.dcm rewrite.dcm

unsetopt verbose
