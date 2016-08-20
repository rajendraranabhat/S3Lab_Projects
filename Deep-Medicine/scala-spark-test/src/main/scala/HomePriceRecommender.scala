import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{Path, FileSystem}
import org.apache.spark.mllib.feature.{StandardScalerModel, StandardScaler}
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LinearRegressionModel
import org.apache.spark.mllib.regression.{LinearRegressionWithSGD, LabeledPoint}
import org.apache.spark.mllib.stat.Statistics
import org.apache.spark.{SparkContext, SparkConf}

case class Home(mlsNum:Double, city:String, sqFt:Double, bedrooms:Double, bathrooms:Double,
                garage:Double, age:Double, acres:Double, price:Double)

object HomePriceRecommender extends Serializable{
  def main(args: Array[String]): Unit = {
    
    // set spark context
    val conf = new SparkConf().setAppName("SparkSQL").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)
    
    /*val linRegModel = sc.objectFile[LinearRegressionModel]("model/linReg.model").first()
    val scalerModel = sc.objectFile[StandardScalerModel]("model/scaler.model").first()

    // home.age, home.bathrooms, home.bedrooms, home.garage, home.sqF
    println(linRegModel.predict(scalerModel.transform(Vectors.dense(11.0, 2.0, 2.0, 1.0, 2200.0))))
    sc.stop()*/

    
    val homeData = sc.textFile("data/homeprice.data")
    val parsed = homeData.map(line=>parse(line))
    
    //look at some statics of the data
    val priceStats = Statistics.colStats(parsed.map(home=>Vectors.dense(home.price)))
    println("Price mean: "+priceStats.mean)
    println("Price max: "+priceStats.max)
    println("Price min: "+priceStats.min)
    
    //filter out anomalous data
    val filtered = parsed.filter(home=>(home.price>100000.0 && home.price <400000.0 && home.sqFt>1000.0))
    
    println("filtered "+filtered.collect())
    filtered.foreach { println }
    
    //see how correlated price and square feet are
    val corr = Statistics.corr(filtered.map(home=>home.price),filtered.map(home=>home.sqFt))
    println("Price and Square feet corr: "+corr)
    
    //Convert to labeled data for MLLib
    val labelData = filtered.map{ home =>
      LabeledPoint(home.price, Vectors.dense(home.age, home.bathrooms,home.bedrooms, home.garage, home.sqFt))
    }.cache()
    
    //Scale features to 0 mean and common variance
    val scaler = new StandardScaler(withMean=true, withStd=true).fit(labelData.map(x=>x.features))
    
    println("Scaler mean: "+scaler.mean.toArray.mkString(","))
    println("Scaler variance: "+scaler.variance.toArray.mkString(","))
    
    val scaledData = labelData.map{data=>
      LabeledPoint(data.label, scaler.transform(Vectors.dense(data.features.toArray)))  
    }
    
    val numIterations = 1000
    val stepSize = 0.2
    //Setup linear regression model and ensure it finds the intercept
    val linearReg = new LinearRegressionWithSGD()
    linearReg.setIntercept(true)
    linearReg.optimizer
      .setNumIterations(numIterations)
      .setStepSize(stepSize)
      
    //run linear regression
    val model =  linearReg.run(scaledData)
    println("Model: "+model)
    
    //determine how well the model predicts the trained data's home prices
    val valuesAndPreds = scaledData.map{point=>
      val prediction = model.predict(point.features)
      (point.label,prediction)
    }
    
    val power = valuesAndPreds.map{
      case(v,p)=>math.pow((v-p),2)
    }
    
    //Mean square error
    val MSE = power.reduce((a,b)=> a+b)/power.count()
    println("<<Mean Square Error: "+MSE)
    
    //persist model
    //sc.parallelize(Seq(model), 1).saveAsObjectFile("model/linReg.model")
    //sc.parallelize(Seq(scaler), 1).saveAsObjectFile("model/scaler.model")
    
  }
  
  // parse home price data into case class
  def parse(line:String)={
    val split = line.split('|')
    val mlsNum = split(0).toDouble
    val city = split(1).toString
    val sqFt = split(2).toDouble
    val bedrooms = split(3).toDouble
    val bathrooms = split(4).toDouble
    val garage = split(5).toDouble
    val age = split(6).toDouble
    val acres = split(7).toDouble
    val price = split(8).toDouble
    Home(mlsNum, city,sqFt, bedrooms, bathrooms,garage,age,acres,price)
  }
}





