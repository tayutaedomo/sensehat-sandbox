# Reference: https://note.com/agw/n/nc052420f3c37

from sense_hat import SenseHat


sense = SenseHat()

print( "Humidity: ", round( sense.get_humidity(),2 ) )
print( "Temperature: ", round( sense.get_temperature(),2 ) )
print( "Air pressure: ", round( sense.get_pressure(),2 ) )

