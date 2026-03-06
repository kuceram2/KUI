#!/bin/bash

SECONDS=0

if [ -z "$1" ]; then
echo "Usage: $0 <number_of_runs>"
exit 1
fi

runs=${1:-10}
declare -A counts
#logfile="results.log"
logfile="overnight/$2_vs_$3_$(date +%m-%d_%H-%M-%S).log"
log_interval=5

echo "Run started at $(date)" > "$logfile"
echo "STARTED"
for ((i=1; i<=runs; i++))
do

python3 headless_reversi_creator.py $2 $3
status=$?
echo "result $status"


# increase counter for this exit code
((counts[$status]++))

remaining=$((runs-i)) 
percent=$((100*i/runs)) 
printf "\rProgress: %d/%d (%d%%) | Remaining: %d\n" "$i" "$runs" "$percent" "$remaining" 
# periodic logging
if (( i % log_interval == 0 )) 
then
 { 
    echo ""
    echo "Checkpoint at run $i ($(date))" 
    for code in "${!counts[@]}" 
    do 
    echo "Exit code $code : ${counts[$code]}" 
    done 
    echo "100: $2 win | 101: $3 win | 99: draw | 90: $2 overtime | 91: $3 overtime"
    echo "-------------------------" 
    } >> "$logfile"
fi
done

echo "Exit status statistics after $runs runs:"
echo "--------------------------------------"
echo "Players: $2 vs $3"
for code in "${!counts[@]}"
do
echo "Exit code $code : ${counts[$code]} times"
done
echo "100: $2 win | 101: $3 win | 99: draw | 90: $2 overtime | 91: $3 overtime"

runtime=$SECONDS
printf "Total runtime: %02d:%02d \n" $((runtime/60)) $((runtime%60))
echo -e "\a \a"
