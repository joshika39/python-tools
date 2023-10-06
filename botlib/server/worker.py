import sys
import time
import zmq

class Worker():
    def __init__(self, pull_addr: str, push_addr: str) -> None:
        context = zmq.Context()
        self.receiver = context.socket(zmq.PULL)
        self.receiver.connect(pull_addr)

        # Socket to send messages to
        self.sender = context.socket(zmq.PUSH)
        self.sender.connect(push_addr)


    def start(self):
        # Process tasks forever
        while True:
            s = self.receiver.recv()

            # Simple progress indicator for the viewer
            sys.stdout.write('')
            sys.stdout.flush()

            # Do the work
            time.sleep(int(s)*0.001)

            # Send results to sink
            self.sender.send(b'')

