# This file is a "Hello, world!" in R language for wandbox.

data(iris)                               ## the "hello, world" of statistics.
summary(iris)                            ## a simple summary of the columns
fit <- lm(Sepal.Length ~ . , data=iris)  ## basic regression
summary(fit)                             ## summary

cat("All done\n")

source("test1.R"); source("test2.R")

test1()
test2()

# R language references:
#   https://cran.r-project.org/manuals.html
