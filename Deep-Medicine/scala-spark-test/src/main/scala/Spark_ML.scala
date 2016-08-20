import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark._

import org.apache.spark.mllib.linalg.{Vector, Vectors}
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.rdd.RDD
import org.apache.spark.mllib.linalg.{Matrix, Matrices}
import org.apache.spark.SparkContext
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.classification.{SVMModel, SVMWithSGD}
import org.apache.spark.mllib.evaluation.BinaryClassificationMetrics
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.mllib.optimization.L1Updater
import org.apache.spark.mllib.classification.{LogisticRegressionModel, LogisticRegressionWithLBFGS}
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.mllib.regression.StreamingLinearRegressionWithSGD
import org.apache.spark.streaming._

object Spark_ML {
  
  def main(args: Array[String]) {
    
     // set spark context
    val conf = new SparkConf().setAppName("SparkSQL").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)
    
    // Create a dense vector (1.0, 0.0, 3.0).
    /*val dv:Vector = Vectors.dense(1.0,0.0,3.0)
    // Create a sparse vector (1.0, 0.0, 3.0) by specifying its indices and values corresponding to nonzero entries.
    val sv1:Vector = Vectors.sparse(3,Array(0,2),Array(1.0,3.0))
    // Create a sparse vector (1.0, 0.0, 3.0) by specifying its nonzero entries.
    val sv2:Vector = Vectors.sparse(3,Seq((0,1.0),(2,3.0)))
    
    println(dv+" "+sv1+" "+sv2)
    
    // Create a labeled point with a positive label and a dense feature vector.
    val pos = LabeledPoint(1.0, Vectors.dense(1.0,0.0,3.0))
    
    // Create a labeled point with a negative label and a sparse feature vector.
    val neg = LabeledPoint(0.0, Vectors.sparse(3, Array(0, 2), Array(1.0, 3.0)))    
    //val examples: RDD[LabeledPoint] = MLUtils.loadLibSVMFile(sc, "data/mllib/sample_libsvm_data.txt")
    
    // Create a dense matrix ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))
    val dm:Matrix = Matrices.dense(3,2,Array(1.0,3.0,5,2,4,6))*/
    
    LSVM(sc)
    
        
  }  
  
  def LSVM(sc: SparkContext){
    // Load training data in LIBSVM format.
    val data = MLUtils.loadLibSVMFile(sc, "data/sample_libsvm_data.txt")

    // Split data into training (60%) and test (40%).
    val splits = data.randomSplit(Array(0.6, 0.4), seed = 11L)
    val training = splits(0).cache()
    val test = splits(1)

    // Run training algorithm to build the model
    val numIterations = 100
    val model = SVMWithSGD.train(training, numIterations)

    // Clear the default threshold.
    model.clearThreshold()

    // Compute raw scores on the test set.
    val scoreAndLabels = test.map { point =>
      val score = model.predict(point.features)
      (score, point.label)
    }

    // Get evaluation metrics.
    val metrics = new BinaryClassificationMetrics(scoreAndLabels)
    val auROC = metrics.areaUnderROC()

    println("Area under ROC = " + auROC)

    /*val svmAlg = new SVMWithSGD()
    svmAlg.optimizer
          .setNumIterations(200)
          .setRegParam(0.1)
          .setUpdater(new L1Updater)
    val modelL1 = svmAlg.run(training)*/

    //Save and load model
    sc.parallelize(Seq(model), 1).saveAsObjectFile("model/scalaSVMWithSGDModel")
    //model.save(sc, "model/scalaSVMWithSGDModel")
    //val sameModel = SVMModel.load(sc, "model/scalaSVMWithSGDModel")
    val sameModel = sc.objectFile[SVMModel]("model/scalaSVMWithSGDModel").first()
    sc.stop()
  }
  
  /*def Logistic(sc: SparkContext){
    // Load training data in LIBSVM format.
    val data = MLUtils.loadLibSVMFile(sc, "data/sample_libsvm_data.txt")
    // Split data into training (60%) and test (40%).
    val splits = data.randomSplit(Array(0.6,0.4), seed=11L)
    val training = splits(0).cache()
    val test = splits(1)
    
    //Run training algorithm to build the model
    val model = new LogisticRegressionWithLBFGS().setNumClasses(10).run(training)
    
    //Compute raw socres on the test ste
    val predictionAndLabels = test.map{
      case LabeledPoint(label, features)=>
        val prediction = model.predict(features)
        (prediction,label)
    }
    
    //Get evaluation metrices
    val metrics = new MulticlassMetrics(predictionAndLabels)
    val accuracy = metrics.accuracy
    println(s"Accuracy = $accuracy")    
  }*/
  
  /*def LinearRegressionWithSGD(sc: SparkContext){
    // Load and parse the data
    val data = sc.textFile("data/lpsa.data")
    val parsedData = data.map{line=>
        val parts = line.split(',')
        LabeledPoint(parts(0).toDouble, Vectors.dense(parts(1).split(' ').map(_.toDouble)))
    }.cache()
    
    //Building the model
    val numIterations = 100
    val stepSize = 0.0000001
    val model = LinearRegressionWithSGD.train(parsedData, numIterations, stepSize)
    
    //Evaluate model on training examples and compute training error
    val valuesAndPreds = parsedData.map{point=>
      val prediction = model.predict(point.features)
      (point.label,prediction)
    }
    
    val MSE = valuesAndPreds.map{case(v,p)=>math.pow((v-p),2)}.mean()
    println("training Mean Squared Error= "+MSE)    
    
  }*/
  
  /*def LinearStreamingRegressionWithSGD(conf: SparkConf){
    val ssc = new StreamingContext(conf, Seconds(1))
    val trainingData = ssc.textFileStream(args(0)).map(LabeledPoint.parse).cache()
    val testData = ssc.textFileStream(args(1)).map(LabeledPoint.parse)
    
    val numFeatures = 3
    val model = new StreamingLinearRegressionWithSGD()
                 .setInitialWeights(Vectors.zeros(numFeatures))

    model.trainOn(trainingData)
    model.predictOnValues(testData.map(lp => (lp.label, lp.features))).print()

    ssc.start()
    ssc.awaitTermination()
  }*/
  
}













