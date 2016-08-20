name := "Acclerometer Spark Analytics"

version := "1.0"

scalaVersion := "2.10.4"

libraryDependencies += "org.apache.spark" %% "spark-core" % "1.2.0"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "1.2.0"

libraryDependencies += "org.apache.spark" %% "spark-streaming" % "1.2.0"

libraryDependencies += "org.apache.spark" %% "spark-streaming-twitter" % "1.2.0"

libraryDependencies += "org.apache.spark" %% "spark-mllib" % "1.2.0"

libraryDependencies += "com.datastax.spark" %% "spark-cassandra-connector" % "1.6.0-M1"

libraryDependencies += "com.datastax.cassandra" % "cassandra-driver-core" % "3.0.0"

libraryDependencies += "org.json4s" %% "json4s-native" % "3.3.0"

libraryDependencies += "org.json4s" %% "json4s-jackson" % "3.3.0"

libraryDependencies += "joda-time" % "joda-time" % "2.9.4"
