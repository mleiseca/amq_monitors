
date_for_file=`date +%Y_%m_%d_%H%M_%S`
while true
do
    python scalability.py "$@" 2>&1 >> run_${date_for_file}.log
    rc=$?
    if [[ $rc != 0 ]] ; then
        exit $rc
    fi
done

