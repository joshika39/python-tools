from . import Worker, Sink, Ventillator

def main():
    vent = Ventillator("tcp://*:5557", "tcp://localhost:5558")
    sink = Sink("tcp://*:5558")
    worker = Worker("tcp://localhost:5557", "tcp://localhost:5558")

if __name__ == "__main__":
    main()