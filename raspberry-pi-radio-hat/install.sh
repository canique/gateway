#!/bin/sh


release="$(lsb_release -cs)"

if ! [ "$release" = "bullseye" ]; then
  echo "Only Debian Bullseye is supported as of now."
  exit 1
fi

#prepare CANIQUE REPO
SetupCaniqueRepository() {
  if ! [ -f /etc/apt/sources.list.d/canique.list ]; then
  	echo "Setting up Canique repository"
  	wget -qO- https://packages.canique.com/canique.key | sudo tee /usr/share/keyrings/canique.key
  	echo "deb [signed-by=/usr/share/keyrings/canique.key] https://packages.canique.com/ $(lsb_release -cs) raspberry" | sudo tee /etc/apt/sources.list.d/canique.list
  fi

  sudo tee /etc/apt/preferences.d/canique.pref > /dev/null <<EOT
Package: mosquitto* libmosquitto*
Pin: origin Canique
Pin-Priority: 1001
EOT

}

SetupInfluxRepository() {
  [ -f /etc/apt/sources.list.d/influxdb.list ] && return

  echo "Setting up InfluxDB repository"
  wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /usr/share/keyrings/influxdb.key
  echo "deb [signed-by=/usr/share/keyrings/influxdb.key] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
}

SetupInfluxRepository
SetupCaniqueRepository

sudo apt-get update

echo "Installing InfluxDB..."
sudo apt-get -y install influxdb

echo "Starting InfluxDB..."
sudo systemctl start influxdb


echo "Installing Mosquitto from Canique Repository..."
sudo apt-get -y install libmosquitto1 mosquitto

echo "Installing Nginx + PHP7.4 ..."
sudo apt-get -y install nginx php7.4-fpm

echo "Installing Canique Packages..."
sudo apt-get -y canique-radio-bridge canique-mqtt-tools canique-web-conf canique-local-cockpit

echo "Status for nginx, mosquitto, influxdb, php7.4 - you should see 4x active:"
systemctl is-active nginx mosquitto influxdb php7.4-fpm

echo "Finished."
echo "Please shutdown Raspberry now, then disconnect power, then plugin Canique Hat + antenna, and finally reconnect power to Raspberry again."


#setup connection between your mosquitto and Canique Cloud with your own user and password
#canique-setup-mosquitto-bridge MQTT_USER MQTT_PASSWD

#setup sensor radio password for every sensor you have
#runuser -u cnq canique-setup-sensor-encryption

#to read new passwords
#sudo systemctl restart canique-radio-bridge
