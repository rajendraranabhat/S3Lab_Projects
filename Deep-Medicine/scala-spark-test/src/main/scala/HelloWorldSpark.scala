import org.apache.spark.SparkContext

import org.apache.spark.SparkConf
import org.apache.spark._
import java.util.Properties

import scala.annotation.tailrec
import scala.util.Random

import org.apache.log4j.Logger
import org.apache.log4j.LogManager

object HelloWorldSpark {

  def main(args: Array[String]) {
    // set spark context
    val conf = new SparkConf().setAppName("wordcount").setMaster("local[*]")
    val sc = new SparkContext(conf)

    /*val distFile = sc.parallelize(List("hi", "this", "is", "Raj")) //ssc.textFile("readme.txt")
    val words = distFile.flatMap(value => value.split("\\s+"))
    words.foreach { println } */

    /*val data = List("hi","hello","how","are","you")
    val dataRDD = sc.makeRDD(data)
    val pipeRDD = dataRDD.pipe("/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/scala-spark-test/echo.sh")
    println("pipeRDDCollect="+pipeRDD.collect())  
    pipeRDD.foreach { println }*/

    /*val rdd = sc.parallelize(Array("37.75889318222431,-122.42683635321838,37.7614213,-122.4240097", "37.7519528,-122.4208689,37.8709087,-122.2688365"))
    //adds our script to a list of files for each node to download with this job
    //val distScript = "/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/scala-spark-test/finddistance.R"
    val distScript = "/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/scala-spark-test/iris_ml.R"
    //sc.addFile(distScript)
    val piped = rdd.pipe(distScript)//(Seq(SparkFiles.get(distScript)), Map("SEPARATOR" -> ","))
    val result = piped.collect
    println(result.mkString(" "))
    piped.foreach { println }*/

    /*
     //Create a Spark Context
     
      sc
      //Open the source file
      .textFile("alice.txt")

      //Pipe to the R process and read result
      .pipe("/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/scala-spark-test/wrapper.R /home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/scala-spark-test/sanitize.R sanitize")
      //.pipe("wrapper.R sanitize.R sanitize")
      
      //Do the actual wordcount,filter empty words
      .flatMap(line => line.split("\\s+"))
      
      .map(word => (word, 1))
      .filter(word => word._1.length != 0)
      .reduceByKey(_ + _)  

      //Sort descending by count
      .map(_.swap)
      .sortByKey(false)
      .map(_.swap)

      //Take the first 100 and print to stdout
      .take(100)
    
      .foreach(println) */
  
  
    val msg = "{ \"id_post\":\"21\",\"message\":\"blablabla\"}";
    val m1 = msgParse(msg)
    println(m1.id_post)
    
    //Other json read
    //val sqlContext = new org.apache.spark.sql.SQLContext(sc)
    //val jsonDf = sqlContext.jsonFile("data/sp500IndexPEAndDiv.json")
    
}
  
  case class SomeClass(id_post: String, message: String) extends serializable
  
  def msgParse(msg: String): SomeClass = {
    import org.json4s._
    import org.json4s.native.JsonMethods._
    
    implicit val formats = DefaultFormats
    val m = parse(msg).extract[SomeClass]
    return m
  }
}









