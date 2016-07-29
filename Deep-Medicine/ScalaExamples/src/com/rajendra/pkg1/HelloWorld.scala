package com.rajendra.pkg1

object HelloWorld {
  def main(args:Array[String]){
    println("Hello World")
    println(new HelloWorld().today)
  }
}

import java.util.Date
import java.text.SimpleDateFormat

class HelloWorld{
  //variable definations
  val greeting = "Hello World"
  var count = 0
  
  //scala method defination
  def func(x:Int):Int={
    x*x
  }
  
  //parameterless method
  def today:String={
    val sdf = new SimpleDateFormat("yyyy.MM.dd")
    sdf.format(new Date)
  }
}











