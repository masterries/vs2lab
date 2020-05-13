import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
result_list = cl.append('bar', base_list)

# Start

x = 1
if result_list:
    result = []
    print("ACK Received")
    async_recv = rpc.AsynchMsgRecv(cl, result)
    async_recv.start()
    print("Doing some Counting...")
    while result == []:

        print(x)
        x += 1
	
        time.sleep(1)
    print("Result: {}".format(result[0].value))
else: 
    print("Failure to Receive")
# Ende

cl.stop()
