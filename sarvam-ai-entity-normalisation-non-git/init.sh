#!/bin/bash
set -e  # Exit immediately if a command fails

echo "Starting initialization of llama.cpp environment..."

# Clone llama.cpp repository if not already present
if [ ! -d "llama.cpp" ]; then
    echo "Cloning llama.cpp repository..."
    git clone https://github.com/ggml-org/llama.cpp
else
    echo "llama.cpp repository already exists. Skipping clone."
fi

cd llama.cpp

# Build llama-server
echo "Configuring build with cmake..."
cmake -B build
echo "Building llama-server..."
cmake --build build --config Release -t llama-server

# Download the model if not already present
if [ ! -f "models/sarvam_entity_normalisation_llama_3.1_8b_unsloth.Q4_K_M.gguf" ]; then
    echo "Model not found. Downloading the model..."
    cd models
    wget https://huggingface.co/Tasmay-Tib/sarvam-entity-normalisation-llama-3.1-8b-gguf/resolve/main/sarvam_entity_normalisation_llama_3.1_8b_unsloth.Q4_K_M.gguf
    cd ..
else
    echo "Model already exists. Skipping download."
fi

# Launch llama-server in the background
echo "Starting llama-server in the background..."
cd build
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