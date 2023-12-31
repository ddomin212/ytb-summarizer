first_time=$1
kernel_name=$2
if [ $first_time == "yes" ]; then
    kaggle datasets create -p generated/dataset
elif [ $first_time == "no" ]; then
    kaggle datasets version -p generated/dataset -m '"new"'
else
    echo "Moving on without creating dataset"
fi

sleep 10

kaggle k push -p generated/kernel

kernel_status="running"
while [[ $kernel_status != "complete" ]]; do
    kernel_status=$(kaggle kernels status $kernel_name | grep -oP 'status "\K\w+')
    if [ $kernel_status == "error" ]; then
        echo "Kernel failed"
        break
    fi
    printf "Kernel status: $kernel_status"
    sleep 10
done

kaggle kernels output $kernel_name -p generated/output