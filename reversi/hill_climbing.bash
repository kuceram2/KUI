#!/bin/bash

# put parameter index, step size and initial param value as arguments

index=$1
# Step size for hill climbing
step=$2
# Initial parameter value
param=$3
# Max iterations
max_iter=15
# Number of trials per parameter
trials=100

logfile="tuning/par_${index}_val_${param}___$(date +%m-%d_%H-%M-%S).log"


echo "tuning param number: $index | initial value: $param | step size: $step" 
echo "tuning param number: $index | initial value: $param | step size: $step" > "$logfile"
# Function to evaluate a parameter
evaluate() {
    local p=$1
    local wins=0
    for ((i=0; i<trials; i++)); do
    python3 tuning_reversi_creator.py tuning_player "$index" "$p" benchmark_player
        result=$?
        #echo "result: $result"
        if (( result == 100 )); then
            wins=$((wins + 1))
        fi

        # if ((result == 99)); then
        #      wins=$((wins + 1))
        # fi
    done
    # Return win count
    echo $wins
}

echo "Setting baseline. "

# Current best
best_param=$param
best_score=$(evaluate $param)

echo "Starting hill climbing: initial param=$param, score=$best_score"
echo "Starting hill climbing: initial param=$param, score=$best_score" > "$logfile"

for ((i=0; i<max_iter; i++)); do
    # Try increasing
    inc_param=$((best_param + step))
    inc_score=$(evaluate $inc_param)
    
    # Try decreasing
    dec_param=$((best_param - step))
    dec_score=$(evaluate $dec_param)

    echo "dec_score $dec_score, inc_score $inc_score"
    # Compare scores
    if (( inc_score > best_score )); then
        best_param=$inc_param
        best_score=$inc_score
        echo "Iteration $i: Improved with +step -> param=$best_param, score=$best_score"
        echo "Iteration $i: Improved with +step -> param=$best_param, score=$best_score" > "$logfile"

    elif (( dec_score > best_score )); then
        best_param=$dec_param
        best_score=$dec_score
        echo "Iteration $i: Improved with -step -> param=$best_param, score=$best_score"
        echo "Iteration $i: Improved with -step -> param=$best_param, score=$best_score" > "$logfile"

    else
        echo "Iteration $i: No improvement, stopping."
        echo "Iteration $i: No improvement, stopping." > "$logfile"
        echo "Best parameter found: $best_param with score $best_score"
        echo "Best parameter found: $best_param with score $best_score" > "$logfile"
        echo -e "\a"
        break
    fi
done

echo "Best parameter found: $best_param with score $best_score"
echo "Best parameter found: $best_param with score $best_score" > "$logfile"
echo -e "\a"