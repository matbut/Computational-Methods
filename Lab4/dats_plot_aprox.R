library("ggplot2")

results = read.csv("data.csv")

avg_results = aggregate( Time ~ Size:Method, data=results, FUN=mean)

avg_results_better = avg_results[avg_results$Method=="better",]

fit_better = lm(Time ~ poly(Size,3), data=avg_results_better)

newdata = data.frame(Size = seq(10,500, length.out=500))

newdata$Time = predict(fit_better, newdata)

newdata$Method = "betterAprox"

ggplot(results,aes(Size,Time,colour=Method, group=Method)) + geom_point()

last_plot() + geom_line(data=newdata, aes(Size,Time))
