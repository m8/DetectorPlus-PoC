# FILE VARS
FILE_NAME = "example.log"
THREADS = {}

# DETECTOR VARS
DELTA_THRESHOLD = 500
WARNING_THRESHOLD = 0.5
ALARM_THRESHOLD = 1
WINDOW_SIZE = 4

# Thread or process structure
class Thread():
    thread_id = 0
    timestamps = []

    suspicious_reads = 0
    warning_cnt = 0
    score = 0
    read_cnt = 0

    def __init__(self, id,ts):
        self.thread_id = id
        self.timestamps = []
        self.timestamps.append(ts)

def read_file(file):
    lines = open(file=file).readlines()
    for line in lines:
        splitted = line.split(';')
        splitted = [str(item).replace(' ','') for item in splitted]
        if(splitted[1] != "0000000000000000"):
            if(splitted[1] in THREADS):
                THREADS[splitted[1]].timestamps.append(splitted[2])
            else:
                THREADS[splitted[1]] = Thread(splitted[1],splitted[2])

# Implementation of Detector Plus
def detector(thread:Thread):
    counter = 0
    window_index = 0
    for ts in thread.timestamps:
        try:
            diff = int(thread.timestamps[counter + 1]) - int(ts) - 200
            print(diff)
            thread.read_cnt += 1
            
            if(diff < DELTA_THRESHOLD):
                thread.suspicious_reads += 1

                if(thread.read_cnt == WINDOW_SIZE):
                    window_index += 1
                    score = thread.suspicious_reads / thread.read_cnt
                    thread.read_cnt = 0
                    thread.suspicious_reads = 0

                    if(score > WARNING_THRESHOLD):
                        print(window_index, thread.thread_id, "WARNING")
                        thread.warning_cnt += 1

                        if(thread.warning_cnt >= ALARM_THRESHOLD):
                            print(window_index, thread.thread_id, "ALARM")
                            thread.warning_cnt = 0
                    else:
                        thread.warning_cnt = 0        
        except:
            continue
        
        counter += 1

def main():
    read_file(FILE_NAME)
    for key, value in THREADS.items():
        detector(value)
        
def print_deltas():
    read_file(FILE_NAME)
    for key, value in THREADS.items():
        counter = 1
        for k in range(int(len(value.timestamps) / 2) + 1):
            diff = int(value.timestamps[counter]) - int(value.timestamps[counter-1]) - 200
            counter += 2
            print(diff)

if __name__ == "__main__":
    main()
