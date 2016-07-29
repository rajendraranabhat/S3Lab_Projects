package com.prisma.util

import scala.io.Source
import scala.collection.mutable.ArrayBuffer
import java.io._;
import scala.beans.BeanProperty

object ScalaUtil {
  
  def main(args: Array[String]){
    //println("Hello World")
    //chap2_scalaLoops()
    //chap3_scalaArray()
    //chap4_scalaMap()
    //chap5_scalaClass()
    //chap6_scalaObject()
    chap7_scalaPackage()
    //chap8_scalaClass()
    //chap9_scalaio()
  }  
  
  def chap9_scalaio(){
    val source = Source.fromFile("readme.txt","UTF-8")
    val lineIterator = source.getLines()
    /*for(l <- lineIterator)
      println(l)*/
      
    val lines = source.getLines().toArray;
    val contents = source.mkString;
    //println("lines="+lines)
    
    //val tokens = source.mkString.split("\\s+");
    //val numbers = tokens.map(_.toDouble)
    //println(numbers)
    
    //print("How old are you?")
    //val age = readInt();
    //println("age="+age);
    
    /*val source1 = Source.fromURL("http://horstmann.com","UTF-8")
    val source2 = Source.fromString("Hello, World");
    val source3 = Source.stdin
    println("Source1"+source1)
    println("Source2"+source2)*/
    
    //Reading Binary Files
    /*val file = new java.io.File("readme.txt")
    val in = new FileInputStream(file)
    val bytes = new Array[Byte](file.length.toInt)
    in.read(bytes)
    in.close()*/
    
    //Writing files
    val out = new java.io.PrintWriter("out.txt")
    for(i<- 1 to 100)
      out.println(i)
    out.close()
    //out.print("%6d %10.2f".format(quantity, price))
    
    /*import java.io.File
    def subdirs(dir:File):Iterator[File]={
      val children = dir.listFiles.filter(_.isDirectory())
      children.toIterator ++ children.toIterator.flatMap(subdirs_)
    }*/
    
    //Scala serializer
    /*class Person extends Serializable{
      private val friends = scala.collection.mutable.ArrayBuffer[Person]() //OK--ArrayBuffer is serializable
    }
    
    val fred = new Person()
    val out1 = new ObjectOutputStream(new FileOutputStream("test.obj"))
    out1.writeObject(fred)
    out1.close()
    val in = new java.io.ObjectInputStream(new FileInputStream("test.obj"))
    val savedFred = in.readObject().asInstanceOf[Person]
    println(savedFred)*/
    
    import sys.process._
    //"ls -al .."!   //unix command
    //"ls -al .."!   //unix command
    "ls -al .." #| "grep sec"! //Piping command
    
    //redirect
    "ls -al .." #> new File("output.txt")  //output
    "ls -al .." #>> new File("output.txt") //append
    "grep sec" #< new File("output.txt")
    //"grep Scala" #< new java.net.URL("http://horstmann.com/index.html") ! //from url
    
    //val p = Process(cmd, new File(dirName), ("LANG", "en_US"))
    //"echo 42" #| p !
    
    //Regular Expression
    val numPattern = "[0-9]+".r
    val wsnumsPattern = """\s+[0-9]+\s+""".r
    /*for(matchString <- numPattern.findAllIn("99 bottles, 98 bottles")){
       println(matchString) 
    }*/
    
    val matches = numPattern.findAllIn("99 bottles, 98 bottles").toArray
    //println(matches)
    
    val m1 = wsnumsPattern.findFirstIn("99 bottles, 98 bottles")
    //println(m1)
    
    numPattern.replaceFirstIn("99 bottles, 98 bottles","XX")
    
    numPattern.replaceAllIn("99 bottles, 98 bottles", "XX")
    
    val numitemPattern = "([0-9]+) ([a-z]+)".r
    val numitemPattern(num, item) = "99 bottles"
    //for(numitemPattern(num,item)<- numitemPattern.findAllIn("99 bottles, 98 bottles"))
    //  println(num+" "+item)
      
    //Exercise
    //1.
    val source1 = Source.fromFile("readme.txt","UTF-8")
    val lineIterator1 = source1.getLines()
    val lines1 = source1.getLines().toArray;
    val contents1 = source1.mkString;
    println(lines1.length)
    var len = lines1.length
    do{
      if(len>0 && lines1(len-1).length() > 12)        
        println(lines1(len-1))
      len = len - 1
    }while(len>=0)    
      
    println(lines1.getClass)
    //println(contents1)
    
    /*println(lineIterator1)
    for(l <- lineIterator1)
      println(l)*/
    
    val source2 = Source.fromFile("out1.txt","UTF-8")    
    val lines2 = source2.getLines().toList;
    val sum = lines2.map { x => x.toFloat }.reduce{(x,y)=> x+y}
    val max = lines2.map { x => x.toFloat }.reduce{(x,y) => if (x > y) x else y}
    val min = lines2.map { x => x.toFloat }.reduce{(x,y) => if (x < y) x else y}
    println(sum)
    println(max)
    println(min)
    
    for(i <- 1 to 10){
      println(i+"--"+math.pow(i, 2)+"--"+math.pow(i, -1))
    }
    
    class Person extends Serializable{
      private val friends = scala.collection.mutable.ArrayBuffer[Person]() //OK--ArrayBuffer is serializable
      
      def addFriends(person:Person){
        friends.append(person)
      }
    }
    
    val fred = new Person()
    val rom  = new Person()
    val hary = new Person()
    
    fred.addFriends(rom)
    fred.addFriends(hary)
    
    val out1 = new ObjectOutputStream(new FileOutputStream("test.obj"))
    out1.writeObject(fred)
    out1.close()
    val in = new java.io.ObjectInputStream(new FileInputStream("test.obj"))
    val savedFred = in.readObject().asInstanceOf[Person]
    println(savedFred)    
  }
  
  def chap8_scalaClass(){
    
    class Person{
      val name = "PersonClass"
      override def toString = getClass.getName+"[name="+name+"]"  
    }
    
    class Employee extends Person{
      override def toString = super.toString+"[Salary="+name+"]"
    }
    
    val p = new Employee()
    println(p.toString())
    
    if(p.isInstanceOf[Employee]){
      val s = p.asInstanceOf[Employee] //s has type Employee
      //obj.isInstanceOf[Cl]  ; obj instanceof Cl
      //obj.asInstanceOf[Cl]  ; (Cl) obj
      //classOf[Cl]  ; Cl.class
    }
    p match{
      case s: Employee => println("Obj") //Process s as Employee
      case _ => println("..") //p wasn't a Employee
    }
    
    /*final override def equals(other:Any)={
      val that = other.asInstanceOf[Item]
      if(that==null) false
      else description == that.description && price == that.price
    }*/
    
    class Shape{
      def area:Double = 0.0
    }
    
    class Rectangle(val width:Double, val height:Double) extends Shape{
      override def area:Double = width*height
    }
    class Circle(val radius:Double) extends Shape{
      override def area:Double = scala.math.Pi*radius*radius
    }
    
    println("Area="+new Circle(3).area)
    
    trait flying{
      def fly()=println("flying")
    }
    trait gliding{
      def gliding()=println("gliding")
    }
    class Vehicle(speed:Int){
      val mph:Int = speed
      def race() = println("Racing")
    }
    class Car(speed:Int) extends Vehicle(speed){
      override val mph:Int = speed
      override def race() = println("Racing Car")
    }
    class Bike(speed:Int) extends Vehicle(speed){
      override val mph:Int = speed
      override def race() = println("Racing Bike")
    }
    class AirCraft(speed:Int) extends Vehicle(speed) with flying with gliding{
      override val mph: Int = speed
      override def race() = println("Racing")
      override def fly() = println("Flying")
      override def gliding() = println("Gliding")
    }
    
    val vehicle1 = new Car(200)
    val vehicle2 = new Bike(100)
    val vehicle3 = new AirCraft(300)
    vehicle3.fly()
    val vehicleList = List(vehicle1, vehicle2, vehicle3)
    println(vehicleList)
    val fastestVehicle = vehicleList.maxBy { _.mph }
    println(fastestVehicle)
    
    //Closure
    var y = 3
    val multiplier = (x:Int)=> x*y
    println(multiplier(3))
    
    //Curried function
    val add = (x:Int, y:Int) => x+y
    def add1(x:Int)(y:Int) = x+y
    def add2(x:Int) = (y:Int) => x+y
    
    println(add1(1)(2))
    
    //Chapter8 exercise
    class SavingAccount(initialBalance: Double){
      private var monthlyCounter = 0;
      private var balance = initialBalance
      def earnMonthlyInterest()   = {monthlyCounter=0}
      def deposit(amount:Double)  = {if(monthlyCounter<=3) balance += amount else balance += amount-1; monthlyCounter + monthlyCounter+1;}
      def withdraw(amount:Double) = {if(monthlyCounter<=1) balance += amount else balance += amount-1;monthlyCounter + monthlyCounter+1;}
    }
    
    class BankAccount(initialBalance: Double){
      private var balance = initialBalance
      //def deposit(amount:Double)  = {balance += amount;balance}
      //def withdraw(amount:Double) = {balance -= amount; balance}
    }    
    
    //class CheckingAccount(initialBalance: Double) extends BankAccount(initialBalance){
    class CheckingAccount(initialBalance: Double) extends SavingAccount(initialBalance){
      private var balance = initialBalance
      //override def deposit(amount:Double)  = {balance += amount-1;balance}
      //override def withdraw(amount:Double) = {balance -= amount-1; balance}
    }
    
    val chkAcct = new CheckingAccount(200)
    println(chkAcct.deposit(10))
    println(chkAcct.withdraw(10))
    
    class Point(x:Double, y:Double){
      
    }
    class LabeledPoint(name:String, x:Double, y:Double) extends Point(x,y){
      println(name+"--"+x+"--"+"--"+y)
    }
    
    val label = new LabeledPoint("Black Thursday", 1929, 230.07)
    println(label)
    
    trait Shape2{
      def centerPoint(x:Double)
    }
    class Rectangle2 extends Shape2{
        override  def centerPoint(x:Double)={println("Rectangle2")}        
    }    
    class Circle2 extends Shape2{
        override  def centerPoint(x:Double)={println("Circle2")}        
    }
    
    val obj2 = new Circle2()
    println(obj2.centerPoint(3))
    
    class Square extends java.awt.Rectangle{
      
    }    
  }
  
  def chap6_scalaObject(){
    /*object helloWorld extends App{
      println("Hello !!")
    }*/
    class Point(a:Int,b:Int){a+b}
    val point = new Point(3,4)
    //println(point)
    
    class Reverse(str:String){
      def rev(){
        return str.reverse  
      }      
    }
    
    object Color extends Enumeration{
      type Color = Value
      val RED, BLUE, GREEN, YELLOW, BLACK = Value
    }
    
    //println(new Reverse("Hello").rev())
    Color.values foreach println    
  }
  
  def chap5_scalaClass(){
    class Counter{
      private var value = 0
      def increment(){if(value<=Int.MaxValue)value += 1}
      def current() = value
    }
    
    val myCounter = new Counter()
    myCounter.increment()
    println(myCounter.current+"--"+myCounter.current())
    
    class Person{
      private var privateAge = 0
      def age = privateAge
      def age_=(newValue:Int){
        if(newValue>privateAge)privateAge=newValue
      }      
    }
    
    val fred = new Person()
    fred.age = 30
    fred.age = 21 //Can't get younger
    println(fred.age)
    
    class Person1{
      private var name=""
      var age = 0
      
      def this(name:String){
        this()
        this.name = name
      }
      def this(name:String,age:Int){
       this(name)
       if(age<0)this.age=0
       else this.age = age
      }      
    }
    
    val p1 = new Person1
    val p2 = new Person1("Fred")
    val p3 = new Person1("Fred",42)
    
    class BankAccount{
      var balance:Double = 0;
      
      def this(balance:Double){
        this()
        this.balance = balance
      }
      
      def deposit(amt:Double)  = (balance=balance+amt)
      def withdraw(amt:Double) = (balance=balance-amt)      
    }
    
    val bank = new BankAccount(500)
    bank.deposit(200)
    println(bank.balance)   
    
    //2
    class Time(var hours:Int, var minutes:Int){
       def before(other:Time)=(other.hours*60 + other.minutes<hours*60+minutes)  
       def interval(other:Time)=(other.hours*60 + other.minutes<hours*60+minutes)
    }
    val time1 = new Time(1,30)
    println("time1="+time1)
    println(time1.before(new Time(1,20)))   
    
    class Student(@BeanProperty name:String,@BeanProperty id:Long){
      
    }
    
    val p5 = new Person1("Fred",-2)
    println(p5.age)
    
    class Person2(name:String){
      var firstName = name.split("\\s+")(0)
      var lastName = name.split("\\s+")(1)
    }
    
    println(new Person2("Rajendra Bhat").lastName)
    
    class Car(val manufactuer : String, val model: String, val year: Int = -1, var license: String = "") {
	    override def toString = "Car(%s, %s, %d, %s)".format(manufactuer, model, year, license)
    }

    val c1 = new Car("Honda", "Civic", 2011, "xx123zz")
    println(c1)
    val c2 = new Car("Hummer", "H1", 2010)
    println(c2)
    val c3 = new Car("Opel", "Astra")
    println(c3)
    println(c3.toString())
    println("manufactuer="+c3.manufactuer)
    
    class LongEmployee {
	    private var _name = "John Q. Public"
	    var salary = 0.0

    	def this(n: String, s: Double) {
    		this()
    		_name = n;
    		salary = s;
    	}
    
    	def name = _name // read-only property, but private var
    	override def toString = "LongEmployee(%s, %f)".format(name, salary)
    }

    val l1 = new LongEmployee()
    println(l1)    
  }
  
  def chap4_scalaMap(){
    //println("Hello")
    val scores = Map("Alice"->10, "Bob"->3,"Cindy"->8) //HashMap
    val mutable_score = scala.collection.mutable.Map("Alice"->10, "Bob"->3,"Cindy"->8) //HashMap
    println(scores)
    println(mutable_score)
    
    val bobsScore = if(scores.contains("Bob")) scores("Bob") else 0
    println(bobsScore)
    val bobsScore1 = scores.getOrElse("Bob", 0)
    println(bobsScore1)
    
    //Exercises
    val prices = scala.collection.mutable.Map("laptop"->10.0,"mouse"->4.0,"monitor"->10.0)
    for((key,value)<-prices){
      prices(key)= prices(key)*0.9
      println(key+"--"+value)
      //println(prices(key)*0.9)
    }
    println(prices)
    //Alternative
    val prices1 = scala.collection.mutable.Map("laptop"->10.0,"mouse"->4.0,"monitor"->10.0)
    val discount = for((k,v)<-prices1) yield(k,0.9*v)
    println(discount)
    
    /*val file_map = new scala.collection.mutable.HashMap[String, Int]
    val in = new java.util.Scanner(new java.io.File("readme.txt"))
    while (in.hasNext()){
      println(in.next())
      file_map  += (in.next()->1)
    }    
    println(file_map)   */ 
    
    val source = Source.fromFile("readme.txt", "UTF-8")
    val tokens = source.mkString.split("\\s+")

    var freq = new scala.collection.immutable.HashMap[String, Int]
    //var freq = new scala.collection.immutable.SortedMap[String, Int]
    tokens foreach { token =>
    	freq = freq + (token -> (freq.getOrElse(token, 0) + 1) )
    } 
    println(freq)
    
    println("Hello".zip("World"))
    println("Hello".zip("World").toMap)
    
    val t = (1, 3.14, "Fred")
    println(t._2)
    val (first,second,third) = t
    println(second)
    
    def minmax(values: Array[Int])=(values.max,values.min)    
    println(minmax(Array(1,2,3,4,5)))
    
    def lteqgt(values: Array[Int], v: Int)=(values.filter { x => x<v },values.filter { x => x==v },values.filter { x => x>v })
    println(lteqgt(Array(1,2,3,4,5),3))
  }
  
  def chap3_scalaArray(){
    //Exercise
    //Array(0 until 10).foreach { println }
    val arr = Array(1,2,5,4,6)
    //println(arr.length)
    /*for(i<-0 until arr.length if(i%2==0))
      yield println(arr(i))
*/    
    val arr2 = arr
    arr2.grouped(2).flatMap {
      case Array(x,y)=>Array(y,x)
      case Array(x)=>Array(x)
    }.foreach { println }
    
    //println(arr2)
    //arr2.grouped(2).foreach { println }
    
    println(arr.map { x => x.toDouble }.sum/arr.length)
    
    scala.util.Sorting.quickSort(arr)
    println(arr.reverse.foreach(println))
    
    val b = ArrayBuffer(1, 7, 2, 9,9)
    println(b.sorted.reverse)
    
    println(b.toSet)
    
    import java.awt.datatransfer._
    val flavors = SystemFlavorMap.getDefaultFlavorMap().asInstanceOf[SystemFlavorMap]
    val flav = flavors.getNativesForFlavor(DataFlavor.imageFlavor)
    println(flav)
  }
  
  def chap2_scalaLoops(){
    
    //def fact(a:Int):Int=if(a<=0) 1 else a*fact(a-1)
    //println(fact(4))
    
    def signum(a:Double):Int=if(a>0) 1 else if(a==0) 0 else -1    
    println(signum(-34))
    
    //for (i <- (1 to 10).reverse) println(i)    
    //for (i <- (10 to 1 by -1)) println(i)
    
    def countdown(n: Int){
      for (i <- (n to 1 by -1)) println(i)
    }    
    //countdown(5)
    
    def product(s : String)=(for (c <- s) yield c.toLong).product
    
    println(product("Hello"))
    
    def product1(s:String):Double={
      if(s.length()<=0) 1
      else{
        product1(s.tail)*s.head.toDouble
      }
    }
    
    println(product1("Hello"))
        
  }
  
  def chap7_scalaPackage(){
  
    /*package object random1 {
    	var seed : Int = 0
    
    	def setSeed(value: Int) = seed = value
    	def nextInt() = {
    		seed = seed * 1664525 + 1013904223 % (2 ^ 32)
    		seed
    	}
  	  def nextDouble() : Double = nextInt().toDouble / Int.MaxValue.toDouble
    }

    setSeed((System.currentTimeMillis() / 1000).toInt)

	  println(seed)
	  (1 to 5).foreach(x => println(nextInt()))
	  (1 to 5).foreach(x => println(nextDouble()))*/
    
    
    /*import java.util.{HashMap => JavaHashMap, Map => JavaMap}
    import collection.mutable.{HashMap => ScalaHashMap, Map => ScalaMap}
    import collection.JavaConversions.mapAsScalaMap
    
    val j: ScalaMap[Int, String] = new java.util.HashMap[Int,String]
    
    j.put(1, "One");
    j.put(2, "Two");
    
    val s: ScalaMap[Int, String] = new ScalaHashMap();
    
    for((k, v) <- j) s += ( k -> v)
    
    println(s)*/
    
    /*import java.lang.System._

    val user = getProperty("user.name")
    val password = Console.readLine("password:")
    
    if (password != "secret")
    	err.println("Invalid password!")
    else
    	println("Welcome %s!".format(user))*/
    
  }
}


    
    


