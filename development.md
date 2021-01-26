# Development

## Development Setup

Custom Plugins are shipped as standard Python packages. Just create a python virtual env and add `cbpi`as dependency

{% hint style="info" %}
How to create virtual env in Python  
[https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html)
{% endhint %}

```bash

python3 -m venv venv
source venv/bin/activate
python3 -m pip insatll cbpi
```

##   Sensor

```python
# -*- coding: utf-8 -*-
import asyncio
import random
import re
import random
from aiohttp import web
from cbpi.api import *

'''
Make sure to extend CBPiSensor
'''

@parameters([Property.Number(label="Param1", configurable=True), 
             Property.Text(label="Param2", configurable=True, default_value="HALLO"), 
             Property.Select(label="Param3", options=[1,2,4]), 
             Property.Sensor(label="Param4"), 
             Property.Actor(label="Param5")])
class CustomSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
    
        super(CustomSensor, self).__init__(cbpi, id, props)
        self.value = 0

    
    @action(key="Test", parameters=[])
    async def action1(self, **kwargs):
        '''
        A custom action. Which can be called from the user interface
        '''
        print("ACTION!", kwargs)

    async def run(self):
        '''
        This method is executed asynchronousely 
        In this example the code is executed every second
        '''
        while self.running is True:
            self.value = random.randint(0,50)
            self.push_update(self.value)
            await asyncio.sleep(1)
    
    def get_state(self):
        # return the current state of the sensor
        return dict(value=self.value)


def setup(cbpi):

    '''
    This method is called by the server during startup 
    Here you need to register your plugins at the server
    
    :param cbpi: the cbpi core 
    :return: 
    '''
    cbpi.plugin.register("CustomSensor", CustomSensor)
```
