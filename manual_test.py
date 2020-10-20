import time
import sys
import logging
import click
from pyhomematic import HMConnection
from pyhomematic.devicetypes.actors import GenericSwitch, IPWKeyBlindMulti, KeyBlind
from pyhomematic.devicetypes.helper import HelperLowBat, HelperSabotage, HelperWorking, HelperBatteryState, HelperValveState
from pyhomematic.devicetypes.sensors import WeatherSensor, IPWeatherSensor, AreaThermostat, ShutterContact, IPShutterContact, Smoke, Motion, Remote
from pyhomematic.devicetypes.thermostats import HMThermostat, IPThermostat


def systemcallback(src, *args):
    print("##### SYSTEMCALLBACK #######")
    print(src)
    for arg in args:
        print(arg)
    print("############################")

def eventcallback(address, interface_id, key, value):
    print("## CALLBACK: %s, %s, %s, %s ##" % (address, interface_id, key, value))


@click.command()
@click.option("--local", "-l", default="0.0.0.0", help="Local address for server")
@click.option("--localPort", "-lp", default=0, help="Local Port for server")
@click.option("--remote", "-r", help="Remote address for CCU/homegear")
@click.option("--remotePort", "-rp", default=2001, help="Remote port for CCU/homegear")
@click.option("--address", "-a", help="Address of homematic device for tests")
@click.option("--channel", "-c", default=None, help="Homematic device channel")
@click.option("--state", "-s", default=1, help="Set STATE value for actors")
@click.option("--toggle", "-to", is_flag=True, help="Set STATE is this activated")
@click.option("--timer", "-t", default=30, help="Time in sec for waiting of events (debug)")
@click.option("--debug", "-d", is_flag=True, help="Use DEBUG instead INFO for logger")
@click.option("--user", "-u", default="Admin", help="Username")
@click.option("--password", "-p", default="", help="Password")
@click.option("--variable", "-v", default=None, help="Variable for set data")
@click.option("--data", "-vd", default=None, help="Input data for variable")
def cli(local, localport, remote, remoteport, address, channel, state, toggle,
        timer, debug, user, password, variable, data):

    # debug?
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        # Connect to HM
        pyhomematic = HMConnection(interface_id="testpyhomatic",
                                   local=local,
                                   localport=localport,
                                   remote=remote,
                                   remoteport=remoteport,
                                   autostart=True,
                                   resolvenames="json",
                                   rpcusername=user,
                                   rpcpassword=password,
                                   systemcallback=systemcallback)
    except Exception:
        print("Can't init HMConnection!")
        sys.exit(1)

    sleepcounter = 0

    while not pyhomematic.devices and sleepcounter < 20:
        print("Waiting for devices")
        sleepcounter += 1
        time.sleep(1)
    if debug:
        print(pyhomematic.devices)

    # read system variables
    print("******************************")
    if debug:
        print("Read all: %s" % str(pyhomematic.getAllSystemVariables('default')))
        if variable is not None:
            pyhomematic.setSystemVariable(variable, data)
            print("Read: %s" % str(pyhomematic.getSystemVariable(variable)))
        print("******************************")

    # need test a hm object?
    if address in pyhomematic.devices['default']:
        device = pyhomematic.devices['default'][address]

        print("******************************")
        print("* Show metadata from %s" % address)
        print("* Elements: %s / Childs: %i" % (device.ELEMENT, len(device.CHANNELS)))
        print("* Class: %s" % str(device.__class__))
        print("* Base: %s" % str(device.__class__.__bases__))
        print("* Sensor datapoint: %s" % str(device.SENSORNODE))
        print("* Binary datapoint: %s" % str(device.BINARYNODE))
        print("* Write datapoint: %s" % str(device.WRITENODE))
        print("* Attribute datapoint: %s" % str(device.ATTRIBUTENODE))
        print("* Event datapoint: %s" % str(device.EVENTNODE))
        print("* Action datapoint: %s" % str(device.ACTIONNODE))
        print("* Name datapoint: %s" % str(device.NAME))
        if (channel):
            channel_device = pyhomematic.devices_all['default'][address+":"+channel]
            print("* Channel Name datapoint: %s" % str(channel_device.NAME))
        print("******************************")

        # WeatherSensor
        if isinstance(device, WeatherSensor) or isinstance(device, IPWeatherSensor):
            print(" / Temperature: %f" % device.get_temperature())
            print(" / Humidity: %i" % device.get_humidity())
            print(" / Rain Counter: %f" % device.get_rain_counter())
            print(" / Wind Speed: %f" % device.get_wind_speed())
            print(" / Wind Direction: %i" % device.get_wind_direction())
            print(" / Wind Direction Range: %i" % device.get_wind_direction_range())
            print(" / Sunshineduration: %i" % device.get_sunshineduration())
            print(" / Brightness: %i" % device.get_brightness())
            print(" / Is Raining: %s" % str(device.is_raining()))

        # AreaThermostat
        if isinstance(device, AreaThermostat):
            print(" / Temperature: %f" % device.get_temperature())
            print(" / Humidity: %i" % device.get_humidity())

        # ShutterContact
        if isinstance(device, ShutterContact) or isinstance(device, IPShutterContact):
            print(" / Contact open: %s" % str(device.is_open()))

        # Smoke
        if isinstance(device, Smoke):
            print(" / Smoke detect: %s" % str(device.is_smoke()))

        # Motion
        if isinstance(device, Motion):
            print(" / Motion detect: %s" % str(device.is_motion()))
            print(" / Brightness: %i" % device.get_brightness())

        # Remote
        if isinstance(device, Remote):
            print(" / is a Remote")

            if toggle:
                print(" / Press short/long")
                device.press_long(channel)
                device.press_short(channel)

        # Switch
        if isinstance(device, GenericSwitch):
            switch_state = device.is_on(channel)
            print(" / Switch is on: %s" % str(switch_state))

            if toggle:
                if (switch_state):
                    device.set_state(False, channel)
                else:
                    device.set_state(True, channel)
                print(" / Switch toogle to: %s" % str(device.is_on(channel)))
            else:
                print(" / Change state to: %s" % str(bool(state)))
                device.set_state(bool(state), channel)
                print(" / Switch is on: %s" % str(device.is_on(channel)))

        # KeyBlind, IPWKeyBlindMulti
        if isinstance(device, IPWKeyBlindMulti):
            level = device.get_level(int(channel))
            print(" / KeyBlind is on level: %s" % str(level))

            if toggle:
                if (level > 0):
                    device.move_down(int(channel))
                else:
                    device.move_up(int(channel))
                print(" / KeyBlind is on level: %s" % str(level))

        # Thermostat
        if isinstance(device, HMThermostat):
            print(" / Working mode: %i" % device.MODE)
            print(" / Target temperature: %.1f" % device.get_set_temperature())
            print(" / Actual temperature: %.1f" % device.actual_temperature())
        if isinstance(device, IPThermostat):
            print(" / Window is opened: %s" % str(bool(device.get_window_state())))

        ########### Attribute #########
        print(" / RSSI_PEER: %i" % device.get_rssi())

        if isinstance(device, HelperLowBat):
            print(" / Low batter: %s" % str(device.low_batt()))

        if isinstance(device, HelperSabotage):
            print(" / Sabotage: %s" % str(device.sabotage()))

        if isinstance(device, HelperWorking):
            print(" / Working: %s" % str(device.is_working()))

        if isinstance(device, HelperValveState):
            print(" / Valve state: %i" % device.valve_state())

        if isinstance(device, HelperBatteryState):
            print(" / Battery state: %f" % device.battery_state())

    # do nothing for show & debug events
    print("Now waiting for events/callback")
    time.sleep(timer)

    # end
    pyhomematic.stop()

if __name__ == "__main__":
    cli()
