#!/usr/bin/env python2.4
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
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
import argparse


parser = argparse.ArgumentParser(description='Read the enqueue/dequeue rates from an AMQ broker or specific queue. Outputs: date,time,enqueue_rate,dequeue_rate,rate_difference ')
parser.add_argument('--hostname', required=True)
parser.add_argument('--port', required=True)
parser.add_argument('--broker', required=True)
parser.add_argument('--queue', help='To look only at a particular queue, provide a value here. Otherwise look at the whole broker')
parser.add_argument('--interval', default=30,type=float, help='number of seconds to sleep before reading again')
parser.add_argument('--javapath', default='', help='Provide a fully qualified path to a java installation')
parser.add_argument("-v", "--verbose", help="increase output verbosity",
		                    action="store_true")
args = parser.parse_args()



hostname = args.hostname
port = args.port
broker = args.broker
queue = args.queue
SLEEP_SECONDS = args.interval

JAVA_BIN=args.javapath+"java"

if args.verbose:
    print args 
BASE_COMMAND = "get -b org.apache.activemq:BrokerName="+broker+",Type=Broker"
if queue:
    BASE_COMMAND = "get -b org.apache.activemq:BrokerName="+broker+",Type=Queue,Destination=" + queue
else:
    BASE_COMMAND = BASE_COMMAND



get_dequeue_count = "echo \"" + BASE_COMMAND + " TotalDequeueCount \""
get_enqueue_count = "echo \"" + BASE_COMMAND + " TotalEnqueueCount \""
if queue:
    get_dequeue_count = "echo \"" + BASE_COMMAND + " DequeueCount \""
    get_enqueue_count = "echo \"" + BASE_COMMAND + " EnqueueCount \""


cmd_get_dequeue_count = get_dequeue_count + " | " + JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar --url " + hostname + ":" + port + " 2>/dev/null"
proc_get_dequeue_count = subprocess.Popen(cmd_get_dequeue_count, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

cmd_get_enqueue_count = get_enqueue_count + " | " + JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar --url " + hostname + ":" + port + " 2>/dev/null"
proc_get_enqueue_count = subprocess.Popen(cmd_get_enqueue_count, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

if args.verbose: 
    print "enqueue_count process: " + cmd_get_enqueue_count
    print "dequeue_count process: " + cmd_get_dequeue_count
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
