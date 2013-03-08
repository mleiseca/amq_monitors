#!/usr/bin/env python2.4

#
# scalability.py
#
# Collect scalability stats from ActiveMQ JMX
#
# Output enqueue_rate - dequeue_rate
# Where enqueue_rate = (messages_enqueued(1_min) - messages_enqueued(0_min))/60
# Where dequeue_rate = (messages_dequeued(1_min) - messages_dequeued(0_min))/60
#

import subprocess
from time import strftime, sleep


hostname="YOUR_HOST_HERE"
port="1099"
queue="order.processing.start"
SLEEP_SECONDS=30

JAVA_HOME="/usr/lib/jvm/java-6-openjdk/jre"
JAVA_BIN=JAVA_HOME+"/bin/java"

BASE_COMMAND = "get -b org.apache.activemq:BrokerName=ghinternal,Type=Queue,Destination="

get_dequeue_count = "echo \"" + BASE_COMMAND + queue + " DequeueCount \""
cmd_get_dequeue_count = get_dequeue_count + " | " + JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar --url " + hostname + ":" + port + " 2>/dev/null"
proc_get_dequeue_count = subprocess.Popen(cmd_get_dequeue_count, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

get_enqueue_count = "echo \"" + BASE_COMMAND + queue + " EnqueueCount \""
cmd_get_enqueue_count = get_enqueue_count + " | " + JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar --url " + hostname + ":" + port + " 2>/dev/null"
proc_get_enqueue_count = subprocess.Popen(cmd_get_enqueue_count, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

# Get initial values
initial_enqueue_count = float(proc_get_enqueue_count.communicate()[0].split('=')[1].strip().lstrip().strip(';'))
initial_dequeue_count = float(proc_get_dequeue_count.communicate()[0].split('=')[1].strip().lstrip().strip(';'))

# Wait 30 seconds
sleep(SLEEP_SECONDS)

# Get new values
proc_get_dequeue_count = subprocess.Popen(cmd_get_dequeue_count, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
proc_get_enqueue_count = subprocess.Popen(cmd_get_enqueue_count, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
final_enqueue_count = float(proc_get_enqueue_count.communicate()[0].split('=')[1].strip().lstrip().strip(';'))
final_dequeue_count = float(proc_get_dequeue_count.communicate()[0].split('=')[1].strip().lstrip().strip(';'))

# Calculate rate
enqueue_count_delta = final_enqueue_count - initial_enqueue_count
dequeue_count_delta = final_dequeue_count - initial_dequeue_count
dequeue_rate = dequeue_count_delta/float(SLEEP_SECONDS)
enqueue_rate = enqueue_count_delta/float(SLEEP_SECONDS)

# Calculate difference in rates
rate_difference = enqueue_rate - dequeue_rate

# Get current date
now = strftime('%Y-%m-%d,%H:%M:%S')

print "%s,%0.4f,%0.4f,%0.4f" % (now, enqueue_rate, dequeue_rate, rate_difference)
