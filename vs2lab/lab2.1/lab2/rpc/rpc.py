import constRPC

from context import lab_channel

# Start Thread Client
import threading
import time

class AsynchMsgRecv(threading.Thread):
#init
    def __init__(self, cl, result):
        threading.Thread.__init__(self)
        self.cl = cl
        self.result = result
#thread recv
    def run(self):

        msgrcv = self.cl.chan.receive_from(self.cl.server)
        self.result.append(msgrcv[1])
        return msgrcv[1]


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self

class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        print('Sending append')
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        return msgrcv[1]  # pass it to caller


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)


    def run(self):
        self.chan.bind(self.server)
        while True:
            print("Waiting for request")
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    print("Received append")
                    time.sleep(3)
                    print("Sending ACK ")
                    self.chan.send_to({client}, [constRPC.OK])
                    print("Working")
                    time.sleep(10)
                    print("Sending Result")
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore

