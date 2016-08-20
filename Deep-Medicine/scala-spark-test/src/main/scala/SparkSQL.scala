import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf


object SparkSQL {

  def main(args: Array[String]) {
    // set spark context
    val conf = new SparkConf().setAppName("SparkSQL").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)
    
    // createSchemaRDD is used to implicitly convert an RDD to a SchemaRDD.
    import sqlContext.createSchemaRDD

    // Define the schema using a case class.
    // Note: Case classes in Scala 2.10 can support only up to 22 fields. To work around this limit,
    // you can use custom classes that implement the Product interface.
    case class Person(name: String, age: Int)
    
    // Create an RDD of Person objects and register it as a table.
    //val people = sc.textFile("people.txt").map(_.split(",")).map(p => Person(p(0), p(1).trim.toInt))
    val people = sc.textFile("people.txt")
    
    ////people.registerTempTable("people")
    
    // SQL statements can be run by using the sql methods provided by sqlContext.
    //val teenagers = sqlContext.sql("SELECT name FROM people WHERE age >= 13 AND age <= 19")
    ////val teenagers = sqlContext.sql("SELECT * FROM people")
    
    // The results of SQL queries are SchemaRDDs and support all the normal RDD operations.
    // The columns of a row in the result can be accessed by ordinal.
    ////teenagers.map(t=>"Name: "+t(0)).collect().foreach(println)
    //println(teenagers.collect())
    
    // The schema is encoded in a string
    val schemaString = "name age"
    
    // Import Spark SQL data types and Row.
    import org.apache.spark.sql._
    
    // Generate the schema based on the string of schema
    val schema = StructType(schemaString.split(" ").map(fieldName=>StructField(fieldName,StringType,true)))
    // Convert records of the RDD (people) to Rows.
    val rowRDD = people.map(_.split(",")).map(p=>Row(p(0),p(1).trim))
    
    // Apply the schema to the RDD.
    val peopleSchemaRDD = sqlContext.applySchema(rowRDD, schema)
    
    //Register the SchemaRDD as a table
    peopleSchemaRDD.registerTempTable("people")
    
    // SQL statements can be run by using the sql methods provided by sqlContext
    val results = sqlContext.sql("select name from people")
    
    // The results of SQL queries are SchemaRDDs and support all the normal RDD operations.
    // The columns of a row in the result can be accessed by ordinal.
    results.map(t=>"Name: "+t(0)).collect().foreach(println)
    
    
    /*val people1 = sqlContext.jsonFile("people.json")
    people1.printSchema()
    people1.registerTempTable("people1")
    val teenagers = sqlContext.sql("select name from people1")
    teenagers.map(t=>"Name: "+t(0)).collect().foreach(println)
    val anotherPeopleRDD = sc.parallelize("""{"name":"Yin","address":{"city":"Columbus","state":"Ohio"}}""" :: Nil)
    val anotherPeople = sqlContext.jsonRDD(anotherPeopleRDD)
    println(anotherPeople)*/
    
    
  }
}





















