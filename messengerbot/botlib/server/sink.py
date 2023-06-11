import sys
import time
import zmq

class Sink():
    def __init__(self, addr="tcp://*:5558") -> None:
        pass
        self.c = zmq.Context()

        # Socket to receive messages on
        self.receiver = self.c.socket(zmq.PULL)
        self.receiver.bind(addr)

    def start(self):
        # Wait for start of batch
        s = self.receiver.recv()

        # Start our clock now
        tstart = time.time()

        # Process 100 confirmations
        for task_nbr in range(100):
            s = self.receiver.recv()
            if task_nbr % 10 == 0:
                sys.stdout.write(':')
            else:
                sys.stdout.write('.')
            sys.stdout.flush()

        # Calculate and report duration of batch
        tend = time.time()
        print(f"Total elapsed time: {(tend-tstart)*1000} msec")