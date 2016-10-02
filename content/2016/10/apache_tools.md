Date: 2016-10-01 13:47
Modified: 2016-10-01 14:08
Title: Apache tools
Category: 我是码农
Slug: articles/2016/10/apache_tools
tags: apache, 分布式, tools
status: draft
summary: Apache分布式工具的简介，随时修改

##hadoop
###yarn
##zookeeper
###简介
主要是用来维护和监控你存储的数据的状态变化。通过监控这些数据状态的变化，从而可以达到基于数据的集群管理。
##kafka
###简介
Kafka is a distributed, partitioned, replicated commit log service. It provides the functionality of a messaging system, but with a unique design.

kafka保证

1. Messages sent by a producer to a particular topic partition will be appended in the order they are sent. That is, if a message M1 is sent by the same producer as a message M2, and M1 is sent first, then M1 will have a lower offset than M2 and appear earlier in the log.
2. A consumer instance sees messages in the order they are stored in the log.
3. For a topic with replication factor N, we will tolerate up to N-1 server failures without losing any messages committed to the log.

###数据持久化
Java内存使用的两个特点：

1. The memory overhead of objects is very high, often doubling the size of the data stored (or worse).
2. Java garbage collection becomes increasingly fiddly and slow as the in-heap data increases.

kafka使用系统提供的filesystem和pagecache来存储数据，并以紧凑的bytes来组织数据，相较于使用java对象，使用同样的内存，可以多存储4倍的数据。不仅如此，还能使用更多的内存。由于内存与文件系统的映射由系统维护，代码也可以简化。如果服务重启，由于内存直接与文件影射，并且由系统维护，因此不需要初始化的操作。

###partition
leader和follower对应的是partition，一个partition有1个leader和0～n个follwers，由配置文件决定。

Kafka保证一个partition内消息有序，同一topic下的不同partition不保证顺序。 

Kafka动态维护一个in-sync replicas（ISR）集合，作为候选leader，并且始终将最新的ISR集合持久化到ZooKeeper中。如果当前leader失效了，某一个follower（ISR）会自动成为新的leader。在Kafka集群中，每个服务器扮演者两个角色，它既作为它的一些partition的leader，也是其它partition的follower。这样保证了集群中的负载均衡。

###producer
producer决定将message发送到哪个partition，通常是由key值和指定的partition算法决定，默认的，如果没有指定key，使用round-robin

###broker


###consumer
Kafka中的broker是无状态的，这意味着消息的消费状态由consumer维护。(**如果consumer重启了，是从最旧的消息消费吗？是否会持久化存储offset**)

consumer需要提交OffsetAndMetadata。 Kafka provides the option to store all the offsets for a given consumer group in a designated broker (for that group) called the offset manager. 