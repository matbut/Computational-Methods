library("ggplot2")

results = read.csv("data.csv")

avg_results = aggregate( Time ~ Size:Method, data=results, FUN=mean)

avg_results$Std = aggregate( Time ~ Size:Method, data=results, FUN=sd)$Time

ggplot(avg_results, aes(Size,Time,colour=Method, group=Method)) + geom_point()+ geom_line() + geom_errorbar(aes(ymin=Time-2*Std, ymax=Time+2*Std))

ggplot(avg_results, aes(Size,Time,colour=Method, group=Method)) + geom_point()+ geom_line()

