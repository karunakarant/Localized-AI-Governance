FROM nvidia/cuda:11.5.2-devel-ubuntu20.04

# Set up system
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (fixed line continuation)
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*
	
# Copy project
WORKDIR /workspace
COPY . /workspace
# Downgrade pip to <24.1 (critical fix)
####RUN python3 -m pip install --upgrade "pip<24.1"

# Avoid openGL errors in PyBullet
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so.1.13

# Upgrade pip and setuptools (critical for gym==0.21.0)
###RUN python3 -m pip install --upgrade pip setuptools==65.5.0


# Install PyTorch (now using CUDA 11.1 wheels)
#RUN pip3 install torch==1.8.0+cu111 torchvision==0.9.0+cu111 \
#    -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install  torch-1.8.0+cu111-cp38-cp38-linux_x86_64.whl
# Install stable-baselines3 and other packages WITH VERSION CONSTRAINTS
RUN pip install gym==0.21.0
RUN pip3 install \
    stable-baselines3==1.6.2 \
    pybullet==3.2.5 \
    pynvml==8.0.4 \
    numpy==1.21.6 \
    matplotlib==3.5.3 

# For headless PyBullet
ENV DISPLAY=:99



#CMD ["python3", "benchmark_930mx.py"]
ENTRYPOINT ["tail", "-f", "/dev/null"]