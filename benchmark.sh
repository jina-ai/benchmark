#!/usr/bin/python3

mkdir -p outputs

for file in src/*.py; do
    output_json=$(echo $file | sed -r 's/.py/.json/g' | sed -r "s/src/outputs/g")
    output_plot=$(echo $file | sed -r 's/.py/.png/g' | sed -r "s/src/outputs/g")
    cmdbench --save-json=${output_json} --save-plot=${output_plot} python3 ${file}
done
