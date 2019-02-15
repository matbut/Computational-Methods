aprox <- function(avg_results_method,method) {

	avg_results_method = avg_results[avg_results$Method==method,]

	fit_method = lm(Time ~ poly(Size,3), data=avg_results_method)

	newdata = data.frame(Size = seq(10,500, length.out=50))

	newdata$Time = predict(fit_method, newdata)

	newdata$Method = paste(method,"Aprox", sep="")

	return(newdata)
}

library("ggplot2")

results = read.csv("data.csv")

avg_results = aggregate( Time ~ Size:Method, data=results, FUN=mean)

ggplot(avg_results,aes(Size,Time,colour=Method, group=Method)) + geom_point()

for(method in c("naive","better","blas")){
}
	newdata = aprox(avg_results,"naive");
	last_plot() + geom_line(data=newdata, aes(Size,Time))
	newdata = aprox(avg_results,"better");
	last_plot() + geom_line(data=newdata, aes(Size,Time))
	newdata = aprox(avg_results,"blas");
	last_plot() + geom_line(data=newdata, aes(Size,Time))

