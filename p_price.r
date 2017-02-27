args = commandArgs(TRUE)
folder = args[1]
file = args[2]
top_price = as.integer(args[3])
pngname = args[4]

# read price data as vector
m_price = as.vector(as.matrix(read.csv(paste(folder,file,sep="\\"),header=TRUE)))

# remove NA and cut too high data
m_price = m_price[!is.na(m_price)]
m_price = m_price[m_price<=top_price]

# calculate price ranges
#price.max = max(m_price)
#price.min = min(m_price)
#range = c(price.min+c(0:100)*(price.max-price.min)/100)
range = c(0:50)*top_price/50

# calculate price bar data
range.bar = c()
for(i in 1:50){
	range.bar = append(range.bar, sum(m_price>=range[i] & m_price<range[i+1]))
}

plot.bar = data.frame(PriceRange = range[1:50],ItemNumber = range.bar)

# plot bar graph
png(paste0(folder,"\\",Sys.Date(),".png"),width=2000,height=500)
mp = barplot(plot.bar$ItemNumber,xlab="price range",ylab="item number",axes=F,cex.lab=1.5)
axis(1,at=mp,labels=plot.bar$PriceRange,cex.axis=1.5)
axis(2,at=seq(0,max(range.bar),100),cex.axis=1.5)
dev.off()