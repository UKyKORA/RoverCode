# Rover Code
## Code hosted on the rover. Includes control and sensor IO as well as server. 

### Sensors: 
* Camera
  * ran by image_poster.py
  * serves an image to image_serv.py every second
* Currents
  * all motors and actuators have current readers in their control code
  * these currents are fed through the MessageHub when OpenMCT subscribes to them 
### Control: 
* RoboClaw
  * all motors and actuators are controlled through roboclaw motor controls
  * roboclaw3.py is the corresponding package for this
### Server:
* MessageHub
  * MessageHub is where the code recieves encoded messages via websocket connections, and turns them into their corresponding controls and or sensor subscriptions.
  * It also posts to the OpenMCT connection based on what sensors are currently subscribed to. 
* TimeProvider
    * MessageHub is event-driven, and therefore will post sensor data on a consistent time interval. TimeProvider pings the messageHub socket at set intervals to ensure the sensor data refreshes. 
* Dictionary
    * OpenMCT uses a json 'dictionary' to package and recieve its messages and therefore MessageHub must abide by these conventions. 
    * See more info in the OpenMCT directory

## TODO
* Restructure to function as more of an API 
* Integrate a sensor posting thread similar to TimeProvider into MessageHub.py
* Implement code in ROS


