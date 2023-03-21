apt update
apt upgrade
apt install build-essential
apt install pkg-config
apt install libnet-dev python-yaml libaio-dev
apt install libprotobuf-dev libprotobuf-c0-dev protobuf-c-compiler protobuf-compiler python-protobuf libnl-3-dev libcap-dev python-future
curl -O -sSL http://download.openvz.org/criu/criu-version.tar.bz2 #我装的3.16
tar xjf criu-version.tar.bz2 
cd criu-3.10
make
cp ./criu/criu /usr/local/bin
echo "{\"experimental\": true}" >> /etc/docker/daemon.json
systemctl restart docker
