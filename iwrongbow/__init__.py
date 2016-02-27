# A python library for discovering and controlling iRainbow Zigbee bulbs
#
# Copyright 2016 Matthew Garrett <mjg59@srcf.ucam.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import socket

class bridge:
    def __init__ (self, address):
        self.address = address
    def probe(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, 18600))
        s.send("##0A0000")        
    def lights(self):
        lights = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, 18600))
        s.send("##0B0000")
        data = s.recv(1024)
        if len(data) == 0:
            return None
        lightdata = str(data).split('##')
        for bulb in lightdata:        
            bulbdata = bulb.split(',')
            if len(bulbdata) == 2:
                continue
            print bulbdata
            lights.append(light(self, bulbdata[0], bulbdata[6]))
        return lights

class light:
    def __init__ (self, bridge, lightid, name):
        self.bridge = bridge
        self.lightid = lightid
        self.name = name
    def set_brightness(self, brightness):
        command = "##05%s02%0.2X" % (self.lightid, brightness)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.bridge.address, 18600))
        s.send(command)
        return               
    def set_colour(self, red, green, blue):
        command = "##03%s06%0.2X%0.2X%0.2X" % (self.lightid, red, green, blue)
        print command
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.bridge.address, 18600))
        s.send(command)
        return        

def discover():
        s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt (socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto("INLAN:", ('<broadcast>', 18602))
        data = s.recv(1024)
        if len(data) == 0:
            return None
        bridgedata = str(data).split(',')
        return bridge(bridgedata[2])
                                    
