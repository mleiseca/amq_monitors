#!/usr/bin/env python2.4

#
# monitor_amq.py
#
# Collect periodic stats from ActiveMQ JMX
#

import subprocess
from time import strftime


hostname="YOUR_HOST_HERE"
port="1099"

JAVA_HOME="/usr/lib/jvm/java-6-openjdk/jre"
JAVA_BIN=JAVA_HOME+"/bin/java"

cmd_clear_stats=JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar -i reset_stats.txt --url " + hostname + ":" + port
cmd_get_QueueSize=JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar -i queue_size_commands.txt --url " + hostname + ":" + port
cmd_get_MaxEnqueueTime=JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar -i max_enqueue_time.txt --url " + hostname + ":" + port
cmd_get_AverageEnqueueTime=JAVA_BIN + " -jar jmxterm-1.0-alpha-4-uber.jar -i average_enqueue_time.txt --url " + hostname + ":" + port


# Process Queue Sizes
proc_get_QueueSize = subprocess.Popen(cmd_get_QueueSize, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
out_get_QueueSize = proc_get_QueueSize.communicate()[0]
data_QueueSize = dict()
for line in out_get_QueueSize.split('\n'):
  if line.startswith('#mbean'):
    queue_name = line.split('=')[4].strip().replace(':', '')
  elif line.startswith('QueueSize'):
    queue_size = line.split('=')[1].strip().replace(';','')
    data_QueueSize[queue_name] = queue_size

# Process MaxEnqueueTime
proc_get_MaxEnqueueTime = subprocess.Popen(cmd_get_MaxEnqueueTime, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
out_get_MaxEnqueueTime = proc_get_MaxEnqueueTime.communicate()[0]
data_MaxEnqueueTime = dict()
for line in out_get_MaxEnqueueTime.split('\n'):
  if line.startswith('#mbean'):
    queue_name=line.split('=')[4].strip().replace(':', '')
  elif line.startswith('MaxEnqueueTime'):
    max_enqueue_time = line.split('=')[1].strip().replace(';','')
    data_MaxEnqueueTime[queue_name] = max_enqueue_time

# Process AverageEnqueueTime
proc_get_AverageEnqueueTime = subprocess.Popen(cmd_get_AverageEnqueueTime, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
out_get_AverageEnqueueTime = proc_get_AverageEnqueueTime.communicate()[0]
data_AverageEnqueueTime = dict()
for line in out_get_MaxEnqueueTime.split('\n'):
  if line.startswith('#mbean'):
    queue_name=line.split('=')[4].strip().replace(':', '')
  elif line.startswith('MaxEnqueueTime'):
    max_enqueue_time = line.split('=')[1].strip().replace(';','')
    data_MaxEnqueueTime[queue_name] = max_enqueue_time

now = strftime('%Y-%m-%d,%H:%M:%S')
for queue_name in data_QueueSize:
  try:
    queue_size = data_QueueSize[queue_name]
  except KeyError:
    queue_size = 0

  try:
    max_enqueue_time = data_MaxEnqueueTime[queue_name]
  except KeyError:
    max_enqueue_time = 0

  try:
    average_enqueue_time = data_AverageEnqueueTime[queue_name]
  except KeyError:
    average_enqueue_time = 0.0

  print "%s,%s,%s,%s,%s" % (now, queue_name, queue_size, max_enqueue_time, average_enqueue_time)
