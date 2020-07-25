# Apache Kafka with MongoDB (Python)

### Overview :

When there are many Source Systems and many target systems and they all have to exchange data with one another, things become complicated. That is why Apache Kafka comes in. 

Apache Kafka is a distributed publish-subscribe messaging system and a robust queue that can handle a high volume of data and enables you to pass messages from one end-point to another.

MongoDB stores data in JSON-like documents, which makes the database very flexible and scalable.

In This project message (JSON type) is produced and consumed on Kafka topic and based on the "action" key in message various MongoDB 
operations is performed. 

Here we will go through following steps:
1. Installation and path set 
2. File Descriptions
3. Workflow
4. Acknowledgements

Let’s Start !

## Installation and path set (windows):

If you already have Apache Kafka and MongoDB installed you can skip this step.

### Apache Kafka Installation:

1. Download jdk and install it (Kafka and zookeeper needs java to run) 
	https://www.oracle.com/java/technologies/javase-jdk8-downloads.html

2. Download Apache Kafka and extract it 
      https://kafka.apache.org/downloads.html > Binary downloads > Scala 2.13 .tgz file

3. Copy the extracted Kafka directory and paste it to root (i.e C:/ drive)

### Set path 

1. Copy windows directory in kafka folder (C:\kafka_2.12-2.5.0\bin\windows) (version can be different)

2. Open "Edit the system environment variables" in your system > click on Environment variables

3. In "User Variables for your_username" > single click on Path > click the "edit" button > click "New" button and paste 
	path in step 1 to it > click "ok".

### Start zookeeper and kafka

1. Create new folder in C:\kafka_2.12-2.5.0, name it data.

2. In data, create 2 new folders zookeeper and kafka.

3. Copy the path C:\kafka_2.12-2.5.0\data\zookeeper and open zookeeper.properties in config (C:\kafka_2.12-2.5.0\config) and search for 
	dataDir and paste this path in that and reverse the slashes (dataDir=C:/kafka_2.12-2.5.0/data/zookeeper)

4.  Now copy path for kafka in data folder (C:\kafka_2.12-2.5.0\data\kafka) and open server.properties and paste this path with reverse
	slash in log.dirs (log.dirs=C:/kafka_2.12-2.5.0/data/kafka)

Refer to CLI commands.txt file inorder to start zookeeper and kafka and for further kafka cli commands.

### MongoDB Installations (windows)
 
1. Open www.mongodb.com > software > Community Server and download the MongoDB for windows, package is msi. Here is the link of video
	which will help you to complete install MongoDB (https://www.youtube.com/watch?v=FwMwO8pXfq0). You won't face any problem in it.

## File Descriptions

Here is the description of each file in this repository

### CLI commands.txt

This File contains all the command line commands you need to know for kafka (with comments), including:

	1. Start zookeeper and Kafka server
	2. Kafka commands like creating topics, producer, consumer and some others

I recommend you to go through this file before heading to python files.

### producer.py

We can send message to topic directly through this file without creating one in command line. But it will alot default properties to the topic (like number of partitions and replication factor). I recommend to first create topic in command line and then produce through this 
file.

Here KafkaProducer object is created and message is produced through the topic "test_topic". 

Message is the json type which includes driver details and based on the "action" key in message, changes will be made to MongoDB table.

Kafka sends message in the form of bytes, that is why it first converted to string and then to bytes.

### mapping_conversions.py

It is created for make the json more flexible. It has a function convert_keys which is called from driver.py file. It basically maps the 
input with desired output of JSON.

For Example:
There is "driver_id" key in message which has a dictionary value but present as a string in message. I want to convert that to dict. But
if "driver_id" don't come in my message I want to skip this process. 

Another Example:
"driver_qualification" is mapped to "driver_education". 

This file is basically used to map input values and their types to desired values and types.

If you don't want to use this file, you can comment where it is called in driver.py file. But you should explore it. It provide great flexiblity to input data.

### driver.py

This is the where consumer it created. Message which is produced by the producer is consumed here and based on "action" key in message 3
functions are performed.

1. If the value in "action" key is "I", consumed message is inserted in MongoDB table "driver".

2. If the value in "action" key is "U", consumed message is upserted in MongoDB i.e based on unique_key ("cargo_number"), if there is   	   nothing in mongodb then consumed message is inserted, Otherwise updated (updation is based on "modified_datetime" key in message,
   if that value is greater than previous stored value only then update will execute. Though it can removed if not needed).

3. If the value in "action" key is "D", unique key i.e "cargo_number" in my case is fetched from input message and if any
   record found in  Mongo table, then that record will delete.

4. If any value apart from "I/U/D" passed in input message. That will be consider as a bad message.

## Workflow

1. First the zookeeper, server and MongoDB connections are made in CLI (refer CLI commands.txt file)

2. Message is created is producer.py file and send over Kafka topic.

3. That message is consumed in driver.py file and first that message is mapped to desired message by passing it to mapping_conversions.py
   file. Then based on the "action" key, corresponding function is called and MongoDB operations performed.

## Acknowledgements

Kafka installation and path setup is inspired from Udemy Course: https://www.udemy.com/course/apache-kafka/ by Stephane Maarek. Rest of the work is according to my requirements. Also stackoverflow helped me at some stages.