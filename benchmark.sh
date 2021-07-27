#!/usr/bin/python3

mkdir -p outputs

for file in benchmarks/*.py; do
    output_json=$(echo $file | sed -r 's/.py/.json/g' | sed -r "s/benchmarks/outputs/g")
    output_plot=$(echo $file | sed -r 's/.py/.png/g' | sed -r "s/benchmarks/outputs/g")
    cmdbench --save-json=${output_json} --save-plot=${output_plot} python3 ${file}
done
