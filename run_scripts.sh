DATA_RATES=("5")
TIKTOK_VIDEO_LENGTH=("test")
# BASE_DIR="satellite_data"
# BASE_DIR="tiktok_data_2"
ewrewqrewqre
BASE_DIR="dataset"
LOCATION="campus"

mkdir -p "$BASE_DIR"

for LENGTH in "${TIKTOK_VIDEO_LENGTH[@]}"
do
    TIME_DIR="$BASE_DIR/$LENGTH"
    mkdir -p "$TIME_DIR"
    LOC_DIR="$TIME_DIR/$LOCATION"
    mkdir -p "$LOC_DIR"
    for RATE in "${DATA_RATES[@]}"
    do
        TRACE_FILE="traces/${RATE}Mbps_trace"
        RATE_DIR="$LOC_DIR/${RATE}Mbps"
        mkdir -p "$RATE_DIR"
        for RUN_LABEL in {1..5}
        do
            for FIX in {1..2}
            do
                echo "Starting Run: $RUN_LABEL Part $FIX"
                echo "Current Length: $LENGTH Seconds"
                CURRENT_DIR="$RATE_DIR/$RUN_LABEL"
                # PCAP_FILE="${CURRENT_DIR}/PCAP/pcap_run_${RUN_LABEL}_type_${LENGTH}_${FIX}.pcap"
                # sudo tcpdump -w $PCAP_FILE -i any & 
                # TCPDUMP_PID=$!
                mkdir -p "$CURRENT_DIR"
                mkdir -p "$CURRENT_DIR/QoS"
                mkdir -p "$CURRENT_DIR/QoE"
                mkdir -p "$CURRENT_DIR/HAR"
                mkdir -p "$CURRENT_DIR/PCAP"
                # mm-link $TRACE_FILE $TRACE_FILE -- python3 tokgrab.py $CURRENT_DIR $LENGTH $RUN_LABEL $RATE $BASE_DIR $LOCATION
                
                python3 tokgrab.py $CURRENT_DIR $LENGTH $RUN_LABEL $RATE $BASE_DIR $LOCATION
                pkill java
                # kill $TCPDUMP_PID
            done
        done
        echo "RUN FINISHED FOR $RATE at $LENGTH seconds"
    done
    echo "ALL RUNS DONE FOR ALL RATES AT $LENGTH seconds"
done
echo "WE DONE"