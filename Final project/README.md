![Third](https://github.com/RamonGilabert/Python/blob/master/Resources/final.png)

The final project consists basically in an app, a web service and what was the third project of basically an NFC sensor together with a DHT11 sensor that go together.

#### Parts of it

- NFC and Temperature sensors that have their own class.
- Notifications, fully configurable to add more if needed.
- Web service to provide users and sensors.
- Web app to display and edit those.

#### Considerations

- When running the main file `final.py` it needs to run in `sudo` for the Adafruit_DHT library to work.
- The Adafruit_DHT library needs to be installed in order to work.
- The pyttsx library needs to be installed in order to work.
- There is a library added that touches the NFC code and all the copyright goes to `ondryaso` even though there has been a small modification in order for the Raspberry Pi to not complain.
- Everything else uses custom code.

##### Notifications

From the configuration file you'll be able to add which outputs you want, using the library pyttsx we are going to output the voice. Note that there are some problems using the library in OS X Yosemite and El Capitan, that's why initially, the configuration file adds a False in the initialization of the voice.

##### Database

The database is only in the web service and it provides a hub for **Users** and for **Sensors**, those last ones will be temperature sensors. Everything to manipulate it comes from a manipulator class in the connection file.

##### Sensors

- NFC sensor.
- DHT11 sensor.

##### Source

There's a website (with an image above) that represents the temperatures when any. It has also an empty state. It lets you edit, add or display more sensors and users, with a login page and custom messages when needed.
