import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object SparkRDD {
  def main(args: Array[String]) {
    
    // set spark context
    val conf = new SparkConf().setAppName("SparkSQL").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)
    
    val data = Array(1,2,3,4,5)
    val distData = sc.parallelize(data)    
    val dist_reduce = distData.reduce((a,b)=>a+b)
    println(dist_reduce)
    
    val lines = sc.textFile("readme.txt")
    val lineLengths = lines.map(s=>s.length)
    val totalLength = lineLengths.reduce((a,b)=>a+b)
    println(totalLength)
    
    val broadcastVar = sc.broadcast(Array(1,2,3))
    println(broadcastVar.value)
    
    //Accumulator
    val accum = sc.accumulator(0, "My Accumulator")
    val add = sc.parallelize(Array(1,2,3,4)).foreach(x=>accum+=x)
    println(accum.value)
  }
}









