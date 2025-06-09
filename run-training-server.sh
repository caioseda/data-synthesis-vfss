#!/bin/bash
# Load env variables
set -a
source .env
set +a

# Logging setup
mkdir -p logs
LOG_FILE="logs/train.log"
exec > >(tee -a "$LOG_FILE") 2>&1

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log_step() {
    echo
    echo "========== $1 =========="
    echo
}

error_exit() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_FILE" >&2
    exit 1
}

log_step "[1/7] SSH into remote and set up environment..."
ssh "$REMOTE_HOST" << 'EOF' || error_exit "SSH or setup failed"
    set -e
    apt update
    apt upgrade -y rsync
    cd /workspace
    git clone https://github.com/caioseda/data-synthesis-vfss.git || echo "Repo exists"
    git clone https://github.com/NVlabs/stylegan3 || echo "Repo exists"
    pip install click requests tqdm pyspng ninja imageio-ffmpeg==0.4.3 scipy
EOF

log_step "[2/7] Copy data to remote..."
rsync -avz \
    "$LOCAL_REPO_PATH/$REPO_DATA_PATH/$TAR_FILE" \
    "$REMOTE_HOST:$REMOTE_WORKDIR/data-synthesis-vfss/$REPO_DATA_PATH/" \
    --progress || error_exit "Failed to copy data"

rsync -avz \
    "$LOCAL_REPO_PATH/$REPO_MODEL_PATH/$MODEL_FILE" \
    "$REMOTE_HOST:$REMOTE_WORKDIR/data-synthesis-vfss/data/" \
    --progress || error_exit "Failed to copy model"

log_step "[3/7] Prepare data on remote..."
ssh "$REMOTE_HOST" << EOF || error_exit "Data extraction or dataset tool failed"
    set -e
    
    mkdir -p $REMOTE_WORKDIR/data-synthesis-vfss/data/images/00000-all-frames-512

    tar \
        -xzf $REMOTE_WORKDIR/data-synthesis-vfss/data/images/$TAR_FILE  \
        -C $REMOTE_WORKDIR/data-synthesis-vfss/data/images/00000-all-frames-512

    python $REMOTE_WORKDIR/stylegan3/dataset_tool.py \
        --source=$REMOTE_REPO_PATH/data/images/00000-all-frames-512 \
        --dest=$REMOTE_REPO_PATH/data/images/00000-all-frames-512.zip
EOF

log_step "[4/7] Train model..."
ssh "$REMOTE_HOST" << EOF || error_exit "Training failed"
    set -e
    SESSION_NAME="train-session"
    
    # Mata a sessão antiga, se existir
    tmux kill-session -t \$SESSION_NAME 2>/dev/null || true

    # Cria nova sessão desanexada
    tmux new-session -d -s \$SESSION_NAME

    # Conecta o output do tmux diretamente ao cat (stdout)
    tmux pipe-pane -o -t \$SESSION_NAME 'cat'

    # Envia o comando de treino para a sessão
    tmux send-keys -t \$SESSION_NAME "
        cd $REMOTE_WORKDIR &&
        python stylegan3/train.py \\
        --data=data-synthesis-vfss/data/images/00000-all-frames-512.zip \\
        --outdir=data-synthesis-vfss/$REPO_MODEL_PATH \\
        --resume=data-synthesis-vfss/data/$MODEL_FILE \\
        --cfg=stylegan2 \\
        --kimg=5000 \\
        --snap=25 \\
        --gpus=2 \\
        --batch=32 \\
        --gamma=1.6384 \\
        --map-depth=2 \\
        --glr=0.0025 \\
        --dlr=0.0025 \\
        --metrics=none
        " C-m
EOF

log_step "[5/7] Determine next training run ID on remote..."

# Set run id based on local date and time
NEXT_RUN_ID=$(date +'%Y-%m-%d--%H-%M-%S')

REMOTE_TRAIN_RUN="data-synthesis-vfss/data/training-runs/00000-stylegan2-00000-all-frames-512-gpus2-batch32-gamma1.6384"
LOCAL_TRAIN_DIR="$LOCAL_TRAIN_PATH/${NEXT_RUN_ID}-stylegan2-00000-all-frames-512-gpus2-batch32-gamma1.6384"

log "Next training run will be: $NEXT_RUN_ID"

log_step "[6/7] Copy training results back to local..."
rsync -avz \
    "$REMOTE_HOST:$REMOTE_WORKDIR/$REMOTE_TRAIN_RUN" \
    "$LOCAL_TRAIN_DIR" \
    --progress || error_exit "Failed to fetch training results from remote"

log_step "[✔] All steps completed. Training run: $NEXT_RUN_ID"