
import asyncio
from cbpi.api.timer import Timer

from cbpi.api import *
import logging


@parameters([Property.Number(label="Timer", description="Time in Minutes", configurable=True), 
             Property.Number(label="Temp", configurable=True),
             Property.Sensor(label="Sensor"),
             Property.Kettle(label="Kettle")])
class MashStep(CBPiStep):

    def __init__(self, cbpi, id, name, props):
        super().__init__(cbpi, id, name, props)
        self.timer = None

    def timer_done(self):
        self.state_msg = "Done"
        asyncio.create_task(self.next())

    async def timer_update(self, seconds, time):
        self.state_msg = "{}".format(time)
        self.push_update()
    
    def start_timer(self):
        if self.timer is None:
            self.time = int(self.props.get("Timer", 0)) * 60
            self.timer = Timer(self.time, self.timer_done, self.timer_update)
        self.timer.start()

    async def stop_timer(self):
        if self.timer is not None:
            await self.timer.stop()
            self.state_msg = "{}".format(self.timer.get_time())

    async def next(self):
        if self.timer is not None:
            await self.timer.stop()
            self.state_msg = ""
        await super().next()

    async def stop(self):
        await super().stop()
        await self.stop_timer()

    async def reset(self):
        self.state_msg = ""
        self.timer = None
        await super().reset()

    async def execute(self):
        if self.timer is None:
            self.state_msg = "Waiting for Target Temp"
            self.push_update()
        else:
            if self.timer is not None and self.timer.is_running() is False:
                self.start_timer()
        sensor_value = 0
        
        while True:
            await asyncio.sleep(1)
            sensor_value = self.get_sensor_value(self.props.get("Sensor"))
            if sensor_value.get("value") >= 2 and self.timer == None:
                self.start_timer()
                    
@parameters([Property.Number(label="Timer", description="Time in Minutes", configurable=True)])
class WaitStep(CBPiStep):

    def __init__(self, cbpi, id, name, props):
        super().__init__(cbpi, id, name, props)
        self.timer = None

    def timer_done(self):
        self.state_msg = "Done"
        
        asyncio.create_task(self.next())

    async def timer_update(self, seconds, time):
        self.state_msg = "{}".format(time)
        self.push_update()
    
    def start_timer(self):
        if self.timer is None:
            self.time = int(self.props.get("Timer", 0)) * 60
            self.timer = Timer(self.time, self.timer_done, self.timer_update)
        self.timer.start()

    async def stop_timer(self):
        if self.timer is not None:
            await self.timer.stop()
            self.state_msg = "{}".format(self.timer.get_time())

    async def next(self):
        if self.timer is not None:
            await self.timer.stop()
            self.state_msg = ""
        await super().next()

    async def stop(self):
        await super().stop()
        await self.stop_timer()

    async def reset(self):
        self.state_msg = ""
        self.timer = None
        await super().reset()

    async def execute(self):
        self.start_timer()
        while True:
            await asyncio.sleep(1)

@parameters([Property.Number(label="Timer", description="Time in Minutes", configurable=True),
                Property.Actor(label="Actor")])
class ActorStep(CBPiStep):

    def __init__(self, cbpi, id, name, props):
        super().__init__(cbpi, id, name, props)
        self.timer = None

    def timer_done(self):
        self.state_msg = "Done"
        asyncio.create_task(self.actor_off(self.actor_id))
        asyncio.create_task(self.next())

    async def timer_update(self, seconds, time):
        self.state_msg = "{}".format(time)
        self.push_update()
    
    def start_timer(self):
        if self.timer is None:
            self.time = int(self.props.get("Timer", 0)) * 60
            self.timer = Timer(self.time, self.timer_done, self.timer_update)
        self.timer.start()

    async def stop_timer(self):
        if self.timer is not None:
            await self.timer.stop()
            self.state_msg = "{}".format(self.timer.get_time())

    async def next(self):
        if self.timer is not None:
            await self.timer.stop()
            self.state_msg = ""
        await super().next()

    async def stop(self):
        await super().stop()
        await self.actor_off(self.actor_id)
        await self.stop_timer()

    async def reset(self):
        self.state_msg = ""
        self.timer = None
        await super().reset()

    async def execute(self):
        self.start_timer()
        self.actor_id = self.props.get("Actor")
        await self.actor_on(self.actor_id)
        while True:
            await asyncio.sleep(1)
            
def setup(cbpi):
    '''
    This method is called by the server during startup 
    Here you need to register your plugins at the server

    :param cbpi: the cbpi core 
    :return: 
    '''
    
    cbpi.plugin.register("ActorStep", ActorStep)
    cbpi.plugin.register("WaitStep", WaitStep)
    cbpi.plugin.register("MashStep", MashStep)
    