import zmq
import random
import time

class Ventillator():
    def __init__(self, sender_addr: str, sink_addr: str) -> None:
        context = zmq.Context()
        
        self.sender = context.socket(zmq.PUSH)
        self.sender.bind(sender_addr)

        self.sink = context.socket(zmq.PUSH)
        self.sink = self.sink.connect(sink_addr)

    def start(self):
        print("Press Enter when the workers are ready: ")
        _ = input()
        print("Sending tasks to workers...")

        # The first message is "0" and signals start of batch
        self.sink_socket.send(b'0')

        # Initialize random number generator
        random.seed()

        # Send 100 tasks
        total_msec = 0
        for task_nbr in range(100):

            # Random workload from 1 to 100 msecs
            workload = random.randint(1, 100)
            total_msec += workload

            self.sender.send_string(f"{workload}")

        print(f"Total expected cost: {total_msec} msec")

        # Give 0MQ time to deliver
        time.sleep(1)