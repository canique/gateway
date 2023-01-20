# Adjusting the local cockpit to your needs

The debian package canique-local-cockpit provides html, js, and css files and places them under /var/www/canique-gateway/  
All dynamic data (sensor data, sensor labels etc) is loaded by Javascript calls using WebSockets (talking directly to Mosquitto on port 9001). The chart data is loaded by requesting JSON formatted data from InfluxDB on port 8086.
You can change the index.html under this directory to fit your needs.   

If you change css or js files, please note that
1) they get cached by your browser, so either you need to change the file name (both in the css/js directory and in index.html) or do a full refresh in the browser
2) The gzipped version will be served to clients automatically if available (e.g. mqtt-4.2.8.min.js.gz) - so if you change mqtt-4.2.8.min.js this will have no effect because mqtt-4.2.8.min.js.gz is still the same.



## Protecting changes from being overwritten

Future updates of the Debian package canique-local-cockpit might overwrite your manual changes or restore files that you have manually deleted.   
Run `sudo apt-mark hold canique-local-cockpit` to prevent this package from being updated in the future. After running this /var/www/canique-gateway will stay as you've left it.
