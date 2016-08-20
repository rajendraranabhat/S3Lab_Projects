#!/usr/bin/env Rscript

# load the package
library(mda)
data(iris)

# fit model
#fit <- mda(Species~., data=iris)

#save(fit,file = "fit.rda")

# summarize the fit
#summary(fit)

# make predictions
#load("/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/scala-spark-test/fit.rda")
load("fit.rda")

predictions <- predict(fit, iris[,1:4])
# summarize accuracy
pred = table(predictions, iris$Species)