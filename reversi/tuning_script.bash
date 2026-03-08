#!/bin/bash

SECONDS=0

if [ -z "$1" ]; then
echo "Usage: $0 <number_of_iterations> <player_name> <tuning_param_idx> <tun_param_val>"
exit 1
fi

foo=${1:-10} # not used
iterations=10
depth=3
declare -A counts
#logfile="results.log"
logfile="tuning/$2_tun_param_$3_$(date +%m-%d_%H-%M-%S).log"
log_interval=5

current_value=$4
step=1
last_result=0 # number of wins in last iteration

echo "Run started at $(date) | Tuning param with idx $3, value: $4" > "$logfile"
echo "STARTED"

# set baseLine
for ((i=1; i<=iterations; i++))
do

python3 tuning_reversi_creator.py $2 $3 $current_value benchmark_player
status=$?
echo "result $status"

# increase counter for this exit code
((counts[$status]++))

remaining=$((runs-i)) 
percent=$((100*i/runs)) 
printf "\rProgress: %d/%d (%d%%) | Remaining: %d\n" "$i" "$runs" "$percent" "$remaining" 
done

last_result=((last_result+counts[100]))
counts[100]=0
counts[101]=0
counts[90]=0
counts[91]=0
counts[99]=0

((current_value=current_value+step))
# first iteration with changed parameter
for ((i=1; i<=iterations; i++))
do

python3 tuning_reversi_creator.py $2 $3 $current_value benchmark_player
status=$?
echo "result $status"

# increase counter for this exit code
((counts[$status]++))

remaining=$((runs-i)) 
percent=$((100*i/runs)) 
printf "\rProgress: %d/%d (%d%%) | Remaining: %d\n" "$i" "$runs" "$percent" "$remaining" 
done

# iterate to selected precision
for((i=1; i<=depth;i++ ))
do
if(())

done


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
