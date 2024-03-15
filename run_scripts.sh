DATA_RATES=("1" "2" "3" "4" "5")
TIKTOK_VIDEO_LENGTH=("15" "60")
BASE_DIR="tiktok_data"

mkdir -p "$BASE_DIR"

for RUN_LABEL in {1..5}
do
    INITIAL_DIR="$BASE_DIR/$RUN_LABEL"
    mkdir -p "$INITIAL_DIR"
    echo "Starting Run: $RUN_LABEL"
    for LENGTH in "${TIKTOK_VIDEO_LENGTH[@]}"
    do
        echo "Current Length: $LENGTH Seconds"
        CURRENT_DIR="$INITIAL_DIR/$LENGTH"
        mkdir -p "$CURRENT_DIR"
        for RATE in "${DATA_RATES[@]}"
        do
            TRACE_FILE="traces/${RATE}Mbps_trace"
            RATE_DIR="$CURRENT_DIR/${RATE}Mbps"
            mkdir -p "$RATE_DIR"
            mkdir -p "$RATE_DIR/QoS"
            mkdir -p "$RATE_DIR/QoE"
            mkdir -p "$RATE_DIR/HAR"
            mm-link $TRACE_FILE $TRACE_FILE -- python3 tokgrab.py $RATE_DIR $LENGTH $RUN_LABEL $RATE
            pkill java
        done
    done
    echo "Run: $RUN_LABEL Complete"
done





