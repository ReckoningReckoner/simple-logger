#!/usr/bin/python3

import json
import subprocess
import datetime
import time

SETTINGS_FILE = "./settings.json"
settings = json.load(open("./settings.json"))

pids = settings["pids"]
delimeter = settings["delimeter"]
sample_time = settings["sample time"]
ps_output_arguments = settings["ps output arguments"]
load_averages_filepath = settings["load averages filepath"]
logfile_path = settings["logfile path"]

combined_pids = " ".join(settings["pids"])

with open(logfile_path, "a") as logfile:
    while True:
        try:
            date = datetime.datetime.now().isoformat()
            load_averages = open(load_averages_filepath).read().strip()

            ps_output = \
                subprocess \
                .run(["ps", "-p", combined_pids, "-o", ps_output_arguments],
                     stdout=subprocess.PIPE)

            usages = str(ps_output.stdout, "utf-8").split("\n")[1:-1]
            usages = \
                delimeter \
                .join([" ".join(usage.split()) for usage in usages])

            log_entry = date + delimeter + ps_output + delimeter + usages
            logfile.write(log_entry)

            time.sleep(sample_time)  # sleep
        except KeyboardInterrupt:
            logfile.close()
