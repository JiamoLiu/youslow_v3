DATA_RATES=("3" "5")
BASE_DIR="database"
LOCATION="campus"
mkdir -p "$BASE_DIR"
LOC_DIR="$BASE_DIR/$LOCATION"
mkdir -p "$LOC_DIR"
for RATE in "${DATA_RATES[@]}"
do
    RATE_DIR="$LOC_DIR/${RATE}Mbps"
    mkdir -p "$RATE_DIR"
    for RUN_LABEL in {1..10}
    do
        TRACE_FILE="traces/${RATE}Mbps_trace"
        CURRENT_DIR="$RATE_DIR/$RUN_LABEL"
        mkdir -p "$CURRENT_DIR"
        PCAP_FILE="${CURRENT_DIR}/${LOCATION}_${RATE}Mbps_run_${RUN_LABEL}.pcap"
        pkill -f "tcpdump -w $PCAP_FILE"
        sudo tcpdump -w $PCAP_FILE -i any > /dev/null 2>&1 &
        TCPDUMP_PID=$!
        if [ "$LOCATION" = "campus" ]; then
            echo "Running campus test at rate $RATE Mbps, run $RUN_LABEL"
            mm-link $TRACE_FILE $TRACE_FILE -- python3 tokbase.py $BASE_DIR $LOCATION $RATE $RUN_LABEL $CURRENT_DIR
        else
            echo "Running satellite test at rate $RATE Mbps, run $RUN_LABEL"
            python3 tokbase.py $BASE_DIR $LOCATION $RATE $RUN_LABEL $CURRENT_DIR
        fi

        pkill java
        kill $TCPDUMP_PID
        echo "Packet capture for $LOCATION at rate $RATE Mbps, run $RUN_LABEL complete."
        sleep 5
    done
done
echo "WE DONE"