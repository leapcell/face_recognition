#/bin/sh
pip install --upgrade pip cmake
apt-get -y update
apt-get update
apt-get install -y --fix-missing git gcc build-essential cmake && apt-get clean && rm -rf /tmp/* /var/tmp/*
git clone https://github.com/davisking/dlib.git && cd dlib && mkdir build; cd build; cmake ..; cmake --build . && cd .. && python3 setup.py install && cd ..
pip install -r requirements.txt