Date: 2016-10-01 13:54
Title: hadoop包依赖问题
Category: 我是码农
Slug: articles/2016/10/hadoop_dependency
tags: apache, 分布式, bug_fix
summary: A bug fix when using hadoop

##问题
###来源
天网项目中，会将所有的依赖包和相关数据文件一起打包，然后在集群上执行，但实际在集群上执行过程中，发现无法获取IP对应的地理位置信息。

###分析
首先分析代码中获取IP对应的地理位置信息的代码：

	public static String getCityOfIP(String dbPath, String ip) {
    	String city = "";
    	File f = new File(dbPath);
    	if (!f.exists()) {
        	return city;
    	}
    
    	LookupService ls = null;
        
    	try {
        	ls = new LookupService(f, LookupService.GEOIP_MEMORY_CACHE);
    	} catch (IOException e) {
        	// TODO Auto-generated catch block
        	e.printStackTrace();
    	}

    	Location llocation = ls.getLocation(ip);

    	if (llocation != null) {
        	city = llocation.city;
    	}
    	
    	ls.close();
    	
    	if (city == null) {
        	city = "NULL";
    	}

    	return city;
	}

上面这段代码的功能获取IP对应城市，dbPath指向一个存储对应关系的数据文件。调用该函数的代码是：

	String GEO_CITY = Toolkit.getCityOfIP("GeoLiteCity.dat", ip);
	
可以看到，dbPath是一个相对路径，这就要求在集群上有对应的文件。分析graphAbnormal中的make.sh文件：

	javac -d bin/ -sourcepath src/ -cp lib/hadoop-2-core.jar:lib/hadoop-2-tools.jar:lib/htrace-core-3.1.0-incubating.jar:lib/protobuf-java-2.4.1.jar:lib/json-simple.jar:lib/jedis-2.4.2.jar:lib/geoip-api-1.2.15-SNAPSHOT.jar:lib/ini4j-0.5.5-SNAPSHOT.jar src/baidu/scloud/data/fhl/cf/proto/FenghuolunCfRequestProtos.java src/graphabnormal/*.java src/baidu/scloud/data/BccProtos.java
	jar cvfm graphAbnormal_fat.jar mymainfest GeoIP.dat GeoLiteCity.dat lib/* src/* -C bin .

发现，原有的逻辑认为把所有的文件都打入jar包，在执行的过程中，就能通过相对路径找到对应的文件及jar包依赖。经过试验发现，jar包可以依赖（*为什么jar包可以依赖呢？*），但是数据文件不能依赖。

###转化描述
在hadoop上运行jar包时，如果依赖第三方库或者一些文件资源，如何将资源上传到集群上？

##解决方法
###方案
hadoop在运行jar包时，支持添加第三方库及资源文件，但是需要使用相应的类对参数进行解析。

GenericOptionsParser这个类，用来解释常用的Hadoop命令行选项，并根据需要，对Configuration对象设置相应的值。通常不直接使用GenericOptionsParser类，更方便的方法是：实现Tool接口，通过ToolRunner来调用，而ToolRunner内部最终还是调用的GenericOptionsParser类。（资料2）

	The supported generic options are:

     	-conf <configuration file>     specify a configuration file
     	-D <property=value>            use value for given property
     	-fs <local|namenode:port>      specify a namenode
     	-jt <local|jobtracker:port>    specify a job tracker
     	-files <comma separated list of files>    specify comma separated
                            files to be copied to the map reduce cluster
     	-libjars <comma separated list of jars>   specify comma separated
                            jar files to include in the classpath.
     	-archives <comma separated list of archives>    specify comma
             separated archives to be unarchived on the compute machines.

原有的代码中已经使用了GenericOptionsParser这个类，直接添加-files参数应该就可以上传资源文件，但事实并非如此。会出现如下报警：

	WARN mapreduce.JobResourceUploader: Hadoop command-line option
	parsing not performed. Implement the Tool interface and execute
	your application with ToolRunner to remedy this.
	
这说明资源并没有上传到集群上，提示实现Tool接口，并使用ToolRunner来执行。按照参考资料3种的方法对代码进行改造之后依然存在这个问题。而根据资料4的回答发现，核心问题并不是要实现Tool接口，而是要使用正确的配置（看后面的代码修改就能明白）。本节开头也提到了，使用GenericOptionsParser和Tool接口并无本质的区别。

###修改方法
对所有的三个MR任务的JobConf进行修改

	JobConf job = new JobConf(GraphAbnormal.class);
	==>
	JobConf job = new JobConf(conf, GraphAbnormal.class);
	
##参考资料
1. http://hadoop.apache.org/docs/r1.2.1/api/org/apache/hadoop/util/GenericOptionsParser.html
2. http://blog.csdn.net/fover717/article/details/8079351
3. https://hadoopi.wordpress.com/2013/06/05/hadoop-implementing-the-tool-interface-for-mapreduce-driver/
4. http://stackoverflow.com/questions/28333080/getting-the-tool-interface-warning-even-though-it-is-implemented





