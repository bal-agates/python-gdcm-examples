#!/usr/bin/env zsh

apps=("ConvertNumpy.py" "ConvertPIL.py" "ConvertMPL.py" "HelloWorld.py" "FindAllPatientName.py")
# apps=("HelloWorld.py")
test_files=`ls test_data/*.dcm`
for app in $apps
do
    for test_file in ${=test_files}
    do
        echo "$ python $app $test_file"
        python $app $test_file
    done
    echo
done