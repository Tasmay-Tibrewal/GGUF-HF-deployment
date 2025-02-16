#!/bin/bash
# Checking for the file
# Check if a directory named "llama.cpp" exists in the current folder
echo "Checking if current directory contains llama.cpp folder"
if [ -d "llama.cpp" ]; then
    if [ -d "llama.cpp/build" ]; then
        echo "Changing directory to llama.cpp/build/"
        cd llama.cpp/build
        # Launch llama-server in the background
        echo "Starting llama-server in the background..."
        # cd build
        # & to run process in background, nohup and disown to isolate it from the terminal
        nohup ./bin/llama-server \
            -m ../models/sarvam_entity_normalisation_llama_3.1_8b_unsloth.Q4_K_M.gguf \
            -n 256 -c 1024 -t 2 -b 1 \
            --temp 0.1 --repeat-penalty 1.1 --top-k 20 \
            --port 8081 --mlock --numa numactl &
        disown
        echo "llama-server launched. Waiting for the server to initialize..."
        # (Optional) Wait a few seconds for the server to start before launching Streamlit
        sleep 5
        echo "Initialization complete. Proceeding with Streamlit app startup..."
    else
        echo "Directory 'build' not found inside 'llama.cpp'"
    fi

# Else, check if the current directory itself is named "llama.cpp"
elif [ "$(basename "$PWD")" = "llama.cpp" ]; then
    echo "First condition is not met, checking if current directory is llama.cpp"
    echo "Current directory is llama.cpp"
    if [ -d "build" ]; then
        echo "Changing directory to build/"
        cd build
        # Launch llama-server in the background
        echo "Starting llama-server in the background..."
        # cd build
        # & to run process in background, nohup and disown to isolate it from the terminal
        nohup ./bin/llama-server \
            -m ../models/sarvam_entity_normalisation_llama_3.1_8b_unsloth.Q4_K_M.gguf \
            -n 256 -c 1024 -t 2 -b 1 \
            --temp 0.1 --repeat-penalty 1.1 --top-k 20 \
            --port 8081 --mlock --numa numactl &
        disown
        echo "llama-server launched. Waiting for the server to initialize..."
        # (Optional) Wait a few seconds for the server to start before launching Streamlit
        sleep 5
        echo "Initialization complete. Proceeding with Streamlit app startup..."
    else
        echo "Directory 'build' not found in the current 'llama.cpp' folder"
    fi

# If neither condition is met, echo an appropriate message along with the current working directory
else
    echo "'llama.cpp' was not found in the current folder, and the current directory is not 'llama.cpp'."
    echo "Current working directory: $(pwd)"
fi