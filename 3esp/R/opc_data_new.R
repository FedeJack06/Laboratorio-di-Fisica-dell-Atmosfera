#'Program to read data from Smart Citizen Kit particle counter and produce outputs
#'needed for writing the report
#'#' title: "opc data 2025"
#' author: "Erika Brattich"
#' date: "29 March, 2025"
rm(list = ls())   #clean the environment from previously used data


#install the libraries, if they are not in the environment
#load the libraries in the environment

packages <- c(
  "openair",
  "lattice",
  "ggplot2",
  "dplyr"
)

for(pkg in packages){
  
  if(!require(pkg, character.only=T)){install.packages(pkg)} 
  
  library(pkg, character.only=T)
}

#'set the working directory and the file to be read, change as appropriate;
#'then organize properly the data for the successive calculations & plots
#set working directory first
#modify as needed
setwd("/home/federico/unibo/atmLab/3esp/R")

#set the name of the file to be read, change as appropriate
file_in <- "20-10-14_prove.csv"   

#read data table, skip first 2 lines after the header
datos <- read.table(file=file_in, sep=",", na.string="null", as.is=TRUE, header=TRUE, skip = 2)

#remove first row containing sample data
datos <- datos[-1,]

#in the "Time" column, substitute T  with a space and remove Z 
datos$Time <- sub("T", " ", datos$Time)
datos$Time <- sub("Z", "", datos$Time)

#read the "Time" as date, specifying the format
datos$date <- as.POSIXct(datos$Time, format = "%Y-%m-%d %H:%M:%S", "GMT")


#'convert particle counts to PM [microgram/m-3]; attention to the units 
#'as particle density is given in g cm-3; the diameter is in micrometers; 
#'the particle numbers in the respective size bins are divided by 0.1 L (flow rate)
#'create the matrices which will contain the data, now filled with NAs

#create a matrix of 1 row, 7 columns containing the size bins in the first row (header)
bin.opc<-matrix(c(0.30, 0.50, 1.0, 2.5, 5.0, 10.0, 15.0),1,7)

#create matrix of diameters of the counter, all NAs for now, 1 row and 6 columns:
#note, the matrix has 1 column less than the size bins
D.opc<-matrix(NA,1,6)

#create matrix of NAs, same number of rows as datos (your data) and 6 columns, 
#note: the matrix has the same number of columns as D.opc
m.opc<-matrix(NA,nrow(datos),6)

#name the columns of m.opc pasting the text "bin", a sequence of numbers from 1 to 6, 
#and the text "_opc"
colnames(m.opc)<-c(paste0("bin",seq(1:6),"_opc"))

#extract the portion of datos (your data) containing the particle counts 
opc.s<-datos[,13:18]*10^-3  #convert counts/0.1 L to counts/cm3 

#'for loop: for each size bin, calculate the Lower Bound, the Upper Bound, the Diameter, and then 
#'the mass
for(i in 1:6){
  LB<-bin.opc[,i]
  UB<-bin.opc[,i+1]
  D.opc[,i]<-LB*(1/4*(1+(UB/LB)^2)*(1+(UB/LB)))^(1/3)
  m.opc[,i]<-1.65*opc.s[,i]*(D.opc[,i]*10^-4)^3*pi/6
}

#calculate the concentration in ug/m3 for each size bin
C.opc<-m.opc*10^13

#'calculate PM mass concentrations summing up the appropriate size bins
#PM1
pm1<-cbind(apply(C.opc[,1:2],1,sum,na.rm=FALSE))

#PM2.5
pm2.5<-cbind(apply(C.opc[,1:3],1,sum,na.rm=FALSE))

#PM10
pm10 <- cbind(apply(C.opc[,1:5],1,sum,na.rm=FALSE))

#add the calculated pm data to the datos (your data)
datos <- cbind(datos, pm1, pm2.5, pm10)

#'compare pm retrieved from the sensor with that calculated manually, using scatterplots, with linear regression
scatterPlot(datos, x ="PM.1.0", y = "pm1", method="scatter", xlab = "measured PM1 (ug/m3)", ylab ="calculated PM1 (ug/m3)", linear = TRUE)
scatterPlot(datos, x ="PM.2.5", y = "pm2.5", method="scatter", linear = TRUE, xlab = "measured PM2.5 (ug/m3)", ylab ="calculated PM2.5 (ug/m3)")
scatterPlot(datos, x ="PM.10.0", y = "pm10", method="scatter", linear = TRUE, xlab = "measured PM10 (ug/m3)", ylab ="calculated PM10 (ug/m3)")

#'compare pm retrieved from the sensor with that calculated manually, using time series plot
timePlot(datos, pollutant = c("PM.1.0", "pm1"), group = TRUE, name.pol=c("measured PM1", "calculated PM1"), ylab="PM1 (ug/m3)")
timePlot(datos, pollutant = c("PM.2.5", "pm2.5"), group = TRUE, name.pol=c("measured PM2.5", "calculated PM2.5"), ylab="PM2.5 (ug/m3)")
timePlot(datos, pollutant = c("PM.10.0", "pm10"), group = TRUE, name.pol=c("measured PM10", "calculated PM10"), ylab="PM10 (ug/m3)")


#calculate statistical indexes for comparison between "modeled" and "observed" PM data, 
#for each PM fraction
stat_PM1<-modStats(datos, mod="pm1", obs ="PM.1.0", na.rm=TRUE)
stat_PM2.5<-modStats(datos, mod="pm2.5", obs ="PM.2.5", na.rm=TRUE)
stat_PM10<-modStats(datos, mod="pm10", obs ="PM.10.0", na.rm=TRUE)

# merge the statistical parameters into a single dataframe
stat_PM <- cbind(stat_PM1, stat_PM2.5, stat_PM10)

#save the dataframe to a txt file in the working directory
write.table(stat_PM, file="evaluation statistics PM.txt",  dec=".", sep ="\t", col.names=T, row.names=F, append=F)

#'extract a portion of the data and calculate spearman correlation, then save the coefficient 
#'as txt file
data_manual <- datos[,20:22]
data_autom <- datos[,10:12]
corr<-cor(data_manual, data_autom, method="spearman")
write.table(corr, file="spearman correlations PM.txt",  dec=".", sep ="\t", col.names=T, row.names=T, append=F)


#'select the first subset of data (e.g., in the courtyard); modify date and time as appropriate
start.date <- as.POSIXct("2020-10-14 08:19:00", format = "%Y-%m-%d %H:%M", "GMT" )
end.date <- as.POSIXct("2020-10-14 08:49:00", format = "%Y-%m-%d %H:%M", "GMT")
subdata1 <- subset(datos, date >= start.date & date < end.date)


#'select the second subset of data (e.g., at the bus stop ..); modify date and time and repeat as appropriate;
#'repeat if necessary
start.date<-as.POSIXct("2020-10-14 09:00:00", format = "%Y-%m-%d %H:%M", "GMT")
end.date<-as.POSIXct("2020-10-14 09:30:00", format = "%Y-%m-%d %H:%M", "GMT")
subdata2 <- subset(datos, date >= start.date & date <= end.date)


# average the data for the specified phase, save to new data .txt file, with decimal point, tab separated
datos_first <-timeAverage(subdata1, avg.time = "30 min", statistic = "mean", vector.ws=FALSE)
datos_second <-timeAverage(subdata2, avg.time = "30 min", statistic = "mean", vector.ws=FALSE)

write.table(datos_first, file="first period average.txt",  dec=".", sep ="\t", col.names=T, row.names=F, append=F)
write.table(datos_second, file="second period average.txt",  dec=".", sep ="\t", col.names=T, row.names=F, append=F)

#extract just particle number from the two subsets
PN1 <- datos_first[,13:18]
PN2 <- datos_second[,13:18]

flow_rate <- 0.01*10^3   #flow rate in L to flow rate in cm3
PN_1 <- PN1/flow_rate  #counts are given in number/0.01 L; conversion of counts to #/cm3
PN_2 <- PN2/flow_rate  #counts are given in number/0.01 L; conversion of counts to #/cm3
ylim <- c(0.01,200) #set the limits for the yaxis scale; to be modified as appropriate


#'plot average particle size distributions for the two phases to compare them 
#plot the particle size distribution for the first period
plot(D.opc, PN_1[1,], ylim = ylim, xlab = expression(paste("dD (", mu, "m)")), ylab = expression(paste("dN/dln(D) (cm"^"-3",")")), log ="xy",  type ="o", col ="red")
#add a new plot on the same figure
par(new=TRUE)
#plot the particle size distribution for the second period on the same graph
plot(D.opc, PN_2[1,], ylim=ylim, type="o", yaxt="n",xaxt="n", ann =FALSE, col ="blue", log="xy")
#old version of the code in which y axis ticks were added only later, specifying here the position of the ticks
#ticks <- c(0.01, 0.1, 1,10, 100, 1000) #modify as appropriate
#axis(side=2, at=ticks, labels=ticks)

legend(3.5, 90, legend =c("first subset", "second subset"), col =c("red", "blue"), lty=c(1,1), cex=0.8)

#'convert particle number distributions into particle surface distributions, and then plot
S.opc <- pi*D.opc^2
PS1 <- S.opc*PN_1
PS2 <- S.opc*PN_2

ylim <- c(1,100) #set the limits for the yaxis scale; to be modified as appropriate

#'plot average particle surface distributions for the two periods 
#plot the particle surface distribution for the first period
plot(D.opc, PS1[1,], ylim=ylim, xlab = expression(paste("dD (", mu, "m)")), ylab = expression(paste("dS/dln(D) ( ", mu, "m"^"2","cm"^"-3",")")), log ="xy",  type ="o", col ="red")
#add a new plot on the same figure
par(new=TRUE)
#plot the particle size distribution for the second period on the same graph
plot(D.opc, PS2[1,], ylim=ylim, type="o", ann =FALSE, yaxt="n",xaxt="n",  col ="blue", log="xy")
#old version of the code in which y axis ticks were added only later, specifying here the position of the ticks
#ticks <- c(0.1, 1, 10, 100) #modify as appropriate
#axis(side=2, at=ticks, labels=ticks)

#add the legend for the plot
legend(3.5, 90, legend =c("first subset", "second subset"), col =c("red", "blue"), lty=c(1,1), cex=0.8)

#'convert particle number distribution into particle volume distributions, and then plot
V.opc <- pi/6*D.opc^3
PV1 <- V.opc*PN_1
PV2 <- V.opc*PN_2
ylim <- c(1,100) #set the limits for the yaxis scale; to be modified as appropriate

#'plot average particle volume distributions for the two periods
#plot the particle volume distribution for the first period
plot(D.opc, PV1[1,], ylim=ylim,  xlab = expression(paste("dD (", mu, "m)")), ylab = expression(paste("dV/dln(D) ( ", mu, "m"^"3","cm"^"-3",")")), log ="xy",  type ="o", col ="red")
#add a new plot on the same figure
par(new=TRUE)
#plot the particle volume distribution for the second period on the same graph
plot(D.opc, PV2[1,], ylim=ylim, type="o", yaxt="n",xaxt="n", ann =FALSE, col ="blue", log="xy")
#old version of the code in which y axis ticks were added only later, specifying here the position of the ticks
#ticks <- c(1, 10, 100)#modify as appropriate
#axis(side=2, at=ticks, labels=ticks)

#add the legend for the plot
legend(3.5, 90, legend =c("first subset", "second subset"), col =c("red", "blue"), lty=c(1,1), cex=0.8)

#calculate summary statistics to compare the two phases; repeat if necessary
sta_period1 <- summary(subdata1)
write.table(sta_period1, file="first period summary statistics.txt",  dec=".", sep ="\t", col.names=T, row.names=F, append=F)
sta_period2 <- summary(subdata2)
write.table(sta_period2, file="second period summary statistics.txt",  dec=".", sep ="\t", col.names=T, row.names=F, append=F)

#find mean for the particle number in 0.3 micron bin; change as appropriate
period1_mu0.3 <- mean(subdata1$PN.0.3, na.rm =TRUE)
period2_mu0.3 <- mean(subdata2$PN.0.3, na.rm =TRUE)

#find standard deviation for the particle number in 0.3 micron bin
period1_sd0.3 <- sd(subdata1$PN.0.3, na.rm =TRUE)
period2_sd0.3 <- sd(subdata2$PN.0.3, na.rm =TRUE)


# Below we want to plot (visualize) the data distribution for our 2 places in the same figure

## Plot counts
# Define bin width for histogram
binw = 25
sum_first <-rowSums(subdata1[,13:18], na.rm =TRUE)
sum_second <-rowSums(subdata2[,13:18], na.rm =TRUE)

period1_mu <- mean(sum_first, na.rm =TRUE)
period2_mu <- mean(sum_first, na.rm =TRUE)

period1_sd <- sd(sum_first, na.rm =TRUE)
period2_sd <- sd(sum_second, na.rm =TRUE)


ggplot() +
  # Plot histograms for places 1 and 2
  ## Place 1 - courtyard
  # Histogram
  geom_histogram(aes(x = sum_first, fill = "#5ab4ac"), # define what's being plotted, color
                 color = "white", # create outline of each bar
                 alpha = 0.8, # change transparency
                 position = "stack", # plot on top of other graphs
                 binwidth = binw,
                 data = subdata1) +
  # Density plot
  geom_density(
    aes(x = sum_first, y = binw * ..count..),
    color = "brown",
    lwd = 1, position = "stack",
    show.legend = F,
    data = subdata1)+
  
  ## Place 2 - at the bus stop
  # Histogram
  geom_histogram(aes(x = sum_second, fill = "#d8b365"),
                 color = "white",
                 alpha = 0.8,
                 position = "stack",
                 binwidth = binw,
                 data = subdata2) +
  # Density Plot
  geom_density(
    aes(x = sum_second, y = binw * ..count..),
    color = "blue",
    lwd = 1,
    position = "stack",
    show.legend = F,
    data = subdata2) +  
  # Style
  # labels
  labs(title = ">0.3um PM Count", x = "Total >0.3um PM (per 0.1 L)", y = "Count") +
  # format legend
  guides(color = guide_legend(override.aes=list(size=1))) +
  # change colors
  scale_fill_manual(name = "Place", values = c("#d8b365", "#5ab4ac"), labels = c("courtyard", "bus stop")) +
  # scale_color_manual(values = c("#d8b365", "#5ab4ac")) +
  theme(legend.position=c(0.80, 0.85)) # reposition legend


## Plot normal distribution
# Place 1 - courtyard
x1norm <- seq(period1_mu - unique(range(period1_mu)/2), period1_mu + 
                unique(range(period1_mu)/2), length.out = 1000) # Create range of x-vals to plot over
y1norm <- dnorm(x1norm, mean = period1_mu, sd = period1_sd) # Create normally distributed data from newly created x-vals
# Create new data.frame
courtyard_ydnorm <- data.frame(x1norm, y1norm)

# Repeat for Place 2
x2norm <- seq(period2_mu - unique(range(period2_mu)/2), period2_mu + 
                unique(range(period2_mu)/2), length.out = 1000) # Create range of x-vals to plot over

y2norm <- dnorm(x2norm, mean = period2_mu, sd = period2_sd) # Create normally distributed data from newly created x-vals
busstop_sqnorm <- data.frame(x2norm, y2norm)

# Reset bin width
binw = 75
ggplot() +
  # Place 1
  geom_histogram(aes(x = sum_first, y = ..density.., fill = "1"),
                 color = "white", alpha = 0.8,
                 position = "stack",
                 binwidth = binw,
                 data = subdata1) +
  geom_line(aes(x = x1norm, y = y1norm, color = "1"),
            lwd = 1,
            show.legend = F,
            data = courtyard_ydnorm) +
  # Vertical line at mean
  geom_vline(aes(xintercept = period1_mu, color = "1"), lwd = 1, linetype = "dashed",
             show.legend = F) +
  # Place 2
  geom_histogram(aes(x = sum_second, y = ..density.., fill = "2"),
                 color = "white", alpha = 0.8,
                 position = "stack",
                 binwidth = binw,
                 data = subdata2) +
  geom_line(aes(x = x2norm, y = y2norm, color = "2"),
            lwd = 1,
            show.legend = F,
            data = busstop_sqnorm) +
  # Vertical line at mean
  geom_vline(aes(xintercept = period2_mu, color = "2"), lwd = 1, linetype = "dashed", 
             show.legend = F) +
  # Style
  # labels
  labs(title = ">0.3um PM Probability Density", x = "Total >0.3um PM (per 0.1 L)", y = "Density") +
  # format legend
  guides(color = guide_legend(override.aes=list(size=1))) +
  # change colors
  scale_fill_brewer(name = "Place", palette = "Set1", labels = c("Courtyard", "Bus stop")) +
  scale_color_brewer(palette = "Set1") +
  theme(legend.position=c(0.80, 0.85)) # re-position legend


## Perform t-test
# Hypothesis test intro and visualization: PM in courtyard vs. PM at the bus stop

ttest_PM = t.test(sum_first, sum_second, alternative='two.sided', var.equal = FALSE, 
                  conf.level = 0.95)
## Look at results
ttest_PM

# put the results into a table
write.table(cbind(ttest_PM$parameter, ttest_PM$p.value), file="ttest_2locations.txt",  dec=".", sep ="\t", col.names=T, row.names=T, append=F)

#Plot t-test results

# Calculate & save distribution
#x_t <- seq(-6,6, length.out = nrow(subdata1))
x_t <- seq(-6,6, length.out = 100)
y_t <- dt(x_t, df = ttest_PM$parameter)

# Save as data frame
ttest <- data.frame(x_t = x_t, y_t = y_t)
# Save Critical Value
crit_val_hi <- qt(0.975, ttest_PM$parameter)

crit_val_lo <- qt(0.025, ttest_PM$parameter)
# Create shaded area
shade1 <- rbind(c(crit_val_hi,0), cbind(subset(ttest, x_t > crit_val_hi),0), c(Inf,0))
shade2 <- rbind(c(crit_val_lo,0), c(-Inf,0), cbind(subset(ttest, x_t < crit_val_lo),0))

# Plot
ggplot(ttest, aes(x = x_t, y = y_t)) +
  # Plot t-test line
  geom_line() +
  # Plot shaded area - where you would reject null hypothesis
  geom_segment(aes(x = crit_val_hi, y = 0, xend = crit_val_hi, yend = dnorm(crit_val_hi))) +
  geom_segment(aes(x = crit_val_lo, y = 0, xend = crit_val_lo, yend = dnorm(crit_val_lo))) +
  geom_polygon(data = shade1, aes(x=x_t, y=y_t, fill="red")) +
  geom_polygon(data = shade2, aes(x=x_t, y=y_t, fill="red")) +
  # Plot horizontal & vertical lines at 0 (for aesthetics)
  geom_hline(yintercept = 0) +
  geom_vline(xintercept = ttest_PM$null.value, col = "red", lwd = 0.5) +
  # Plot where your critical value i.s
  geom_vline(xintercept = ttest_PM$statistic, col = "blue", lwd = 2) + # Plot normalized mean for Place 2
# No legend
guides(fill="none") +
  # Add labels
  labs(title = "T-Test Results", x = "t-value", y = "Density")
# Are the hypothesis test conclusions you get from the two figures consistent with the conclusions
# you get by comparing the p-value with 5%?


## Alternative to plot Time-Series Data
ggplot(data = datos) +
  geom_line(aes(x = date, y = pm1)) +
  labs(title = "Time-Series Data", x = "Date", y = "PM1 (ug/m3)")



#calculate the moments of the particle number size distributions
#first option using the formulae on the right 

#moment of order zero is just the total number of particles
totPN1 <- cbind(apply(PN1[,1:6], 1, sum, na.rm=FALSE))
totPN2 <- cbind(apply(PN2[,1:6], 1, sum, na.rm=FALSE))

#moment of order one is the average particle diameter multiplied the moment of order zero
mean_diam <- mean(D.opc)
mom1_1 <- totPN1 * mean_diam
mom1_2 <- totPN2 * mean_diam

#moment of order two is the average surface area multiplied the moment of order zero and divided by pi
mean_area <-pi*mean_diam^2
mom2_1 <- mean_area* totPN1 / pi
mom2_2 <- mean_area* totPN2 / pi

#moment of order three is the average volume multiplied six times the moment of order zero
#and divided by pi

mean_vol <- pi/6*mean_diam^3
mom3_1 <- mean_vol * 6 * totPN1/pi
mom3_2 <- mean_vol * 6 *totPN2/pi

#second option is to define a function


########