#!/bin/bash
#
# monitor_amq.sh
#
# Collect periodic stats from ActiveMQ JMX
#
# Parameters:
# host - host to connect to
# port - port running JMX
# sleep - period to wait
#

host="YOUR_HOST_HERE"
port="1099"

# setup java environment
JAVA_HOME="/usr/lib/jvm/java-6-openjdk/jre"
CLASS_PATH="${CLASS_PATH}:."
JAVA_BIN=$(which java)
export JAVA_HOME CLASS_PATH

# Reset stats ${JAVA_BIN} -jar jmxterm-1.0-alpha-4-uber.jar -i operations.txt --url YOUR_HOST_HERE:1099
${JAVA_BIN} -jar jmxterm-1.0-alpha-4-uber.jar  -i reset_stats.txt --url ${host}:${port} >/dev/null 2>&1


# Get QueueSizes
temp_file=/tmp/queue_sizes.$$
${JAVA_BIN} -jar jmxterm-1.0-alpha-4-uber.jar  -i queue_size_commands.txt --url ${host}:${port} > ${temp_file} 2>&1
python -c "
import sys
from time import strftime
now=strftime('%Y-%m-%d,%H:%M:%S')
qfile_name = sys.argv[1]
qfile=open(qfile_name, 'r')
queue_data={}
qfile.seek(0)
for line in qfile.readlines():
  if line.startswith('#mbean'):
    queue=line.split('=')[4].strip().replace(':', '')
  elif line.startswith('QueueSize'):
    queue_size=line.split('=')[1].strip().replace(';','')
    queue_data[queue] = queue_size
for queue in queue_data:
   print '%s,QueueSize,%s,%s' % (now, queue, queue_data[queue])
" ${temp_file}
rm ${temp_file}

# Get MaxEnqueueTime
temp_file=/tmp/queue_times.$$
${JAVA_BIN} -jar jmxterm-1.0-alpha-4-uber.jar  -i max_enqueue_time.txt --url ${host}:${port} > ${temp_file} 2>&1
python -c "
import sys
from time import strftime
now=strftime('%Y-%m-%d,%H:%M:%S')
qfile_name = sys.argv[1]
qfile=open(qfile_name, 'r')
queue_data={}
qfile.seek(0)
for line in qfile.readlines():
  if line.startswith('#mbean'):
    queue=line.split('=')[4].strip().replace(':', '')
  elif line.startswith('MaxEnqueueTime'):
    queue_size=line.split('=')[1].strip().replace(';','')
    queue_data[queue] = queue_size
for queue in queue_data:
   print '%s,MaxEnqueueTime,%s,%s' % (now, queue, queue_data[queue])
" ${temp_file}
rm ${temp_file}

# Get AverageEnqueueTime
temp_file=/tmp/queue_times.$$
${JAVA_BIN} -jar jmxterm-1.0-alpha-4-uber.jar  -i average_enqueue_time.txt --url ${host}:${port} > ${temp_file} 2>&1
python -c "
import sys
from time import strftime
now=strftime('%Y-%m-%d,%H:%M:%S')
qfile_name = sys.argv[1]
qfile=open(qfile_name, 'r')
queue_data={}
qfile.seek(0)
for line in qfile.readlines():
  if line.startswith('#mbean'):
    queue=line.split('=')[4].strip().replace(':', '')
  elif line.startswith('AverageEnqueueTime'):
    queue_size=line.split('=')[1].strip().replace(';','')
    queue_data[queue] = queue_size
for queue in queue_data:
   print '%s,AverageEnqueueTime,%s,%s' % (now, queue, queue_data[queue])
" ${temp_file}
rm ${temp_file}
