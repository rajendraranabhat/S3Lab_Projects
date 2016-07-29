package com.prisma.util

import java.io._
import scala.io.Source

import org.json4s._
//import org.json4s.JsonAST.JArray
import org.json4s.jackson.JsonMethods._
import org.json4s.jackson.Serialization.write
import org.json4s.jackson.Serialization.read
import org.json4s.JsonDSL._
import org.json4s._

object Utility {
  
  case class Stuff(name:String, age:Int)
   
  def main(args:Array[String]){
    //println("Hello World!")
    //System.gc() //run garbage collector
    //val rawJson = """{"hello": "world", "age": 42}"""
    //println(JSON.parseFull(rawJson))
    
    //Case class
    /*val s = Stuff("David",45)
    println(s.toString())
    println(s.name+" : "+s.age)
    println(s==Stuff("David",34))*/
    
    jsonParser2()
    
    //json4sExample()
    
    
  }
  
  def json4sExample(){
    implicit val formats = DefaultFormats
    
    case class Person(name:String, age:Int)
    val jsValue = parse("""{"name":"john", "age": 28}""")
    val p = jsValue.extract[Person]
    val maybeP = jsValue.extractOpt[Person]
    
    //println(p)
    //println(maybeP)
    
    case class Car(model:String, year:Int, ownerName:Option[String])
    val car1 = parse("""{"model":"c-class","year":2011}""").extract[Car]
    // car1: Car = Car(c-class,2011,None)

    val car2 = parse("""{ "model":"b-class","year":2013,"ownerName": "john doe"}""").extract[Car]
    // car2: Car = Car(b-class,2013,Some(john doe))
    
    //println(car1)
    //println(car2)
    
    //val jarr = JArray()
    val jarr2 = JArray(List(JString("foo"),JInt(42)))
    val jsvalues = jarr2.arr
    
    jarr2.arr.foreach{ 
      jsval => println(s"Hi i'm a ${jsval.getClass}")
    }
    
    //Json obj to string
    //implicit val formats = DefaultFormats
    //case class Person(name:String, age:Int)
    val john = Person("john",45)
    println(write(john))
    val maryAsString = """{"name":"mary", "age":89} """
    println(read[Person](maryAsString))
    
    //val invalidPerson = """{"name":"david","numPets":2}"""
    //read[Person](invalidPerson) //error out
    
    /*case class Person1(name:String, age:Option[Int])
    val john1 = Person1("john",None)
    write(john1)
    val mary = Person1("mary",Some(20))
    write(mary)*/
    
    val obj1: JObject = ("foo","bar") ~ ("baz","quux")
    println(obj1)
    val obj2: JObject = ("foo" -> "bar") ~ ("baz" -> "quux")
    println(obj2)
    
    val array1:JArray = Seq(obj1,obj2)
    println(write(array1))
    
    val array2:JArray = Seq("foo","bar")
    println(write(array2))
  }
  
  
  def jsonParser(){
    
    val myMap = Map("a"->List(3,4),"b"->List(7,8))
    
    //writing to a file
    val jsonString = pretty(render(myMap))
    
    val pw = new PrintWriter(new File("jsonex.json"))
    pw.write(jsonString)
    pw.close()
    
    //reading a file
    val myString = Source.fromFile("jsonex.json").mkString
    println(myString)
    
    val myJSON = parse(myString)
    
    println(myJSON)
    
    //converting from JObject to plain object
    implicit val formats = DefaultFormats
    val myOldMap = myJSON.extract[Map[String,List[Int]]]
    println(myOldMap)
    
  }
  
  def jsonParser1(){
    implicit val formats = DefaultFormats
    val json = """
    [
      {"name": "Foo", "emails": ["Foo@gmail.com", "foo2@gmail.com"]},
      {"name": "Bar", "emails": ["Bar@gmail.com", "bar@gmail.com"]}
    ]
    """
    val json1 = """
    [
      {"name": "Foo", "emails": "foo2@gmail.com"},
      {"name": "Bar", "emails": "bar@gmail.com"}
    ]
    """
    case class User(name: String, emails: String)
    //val myArray = json1.asInstanceOf[JArray]
    //println(myArray.arr)
    val list = json1.values.asInstanceOf[List[Map[String, String]]]
    
    //val obj = parse(json1).extract[User]
    //println(obj)
  }
  
  def jsonParser2(){
    val myObj = parse("""{"foo":"bar"}""").asInstanceOf[JObject]
    println(myObj \ "foo")
    println((myObj \ "foo").toOption)
    println(myObj \ "baz")
    println((myObj \ "baz").toOption)
  }
  
}




//http://apache-spark-user-list.1001560.n3.nabble.com/json-parsing-with-json4s-td7430.html
















