rm(list=ls())

# -*- coding: utf-8 -*-
#Created on Wed May 14 18:17:38 2025

#@authors: Andrea Faggi (Python) & Erika Brattich (R)
# libraries
library(readr)
library(ggplot2)

# Set working directory
setwd('C:/Users/erika.brattich2/Downloads/prova')

# open csv files previously created with Open_Merge_Stats script 
df <- read_csv('stats_image.csv')


y_min <- df$Mean - df$StdDev
y_max <- df$Mean + df$StdDev

# Create the plot using ggplot2
p <- ggplot(df, aes(x = seq_along(df$Mean))) +
  # Background and grid
  # Error bar for mean with standard deviation
  geom_errorbar(
    aes(ymin = y_min, 
        ymax = y_max, color="blue"),
    width = 0.1
  ) +
  geom_point(
    aes(y = Mean, color="blue"), 
    shape = 1# hollow circle
    ) +
  
  geom_line(
    aes(y=Mean, colour="blue")
  )+
  
  # Maximum points
  geom_point(
    aes(y = Max, colour="orange"), 
    shape = 22,  # square
    fill = "transparent"
  ) +
  geom_line(
    aes(y=Max, colour="orange"))+
  
  # Minimum points
  geom_point(
    aes(y = Min, colour="darkgreen"), 
    shape = 24,  # triangle
    fill = "transparent"
  ) +
  
  geom_line(
    aes(y=Min, colour="darkgreen")
  ) +
  # Labels and title
  labs(
    x = "Frame", 
    y = "Temperature [°C]", 
    title = "Frame Image statistics"
  ) + 
  # Add legend manually

  scale_color_manual(
   name = "Statistics",
  values = c("blue", "darkgreen", "orange"),
  labels = c("mean with std", "minimum", "maximum"))
      # format legend
     # scale_fill_manual(name = "Statistics", values = c("blue", "darkgreen", "orange"), labels = c("mean with std", "minimum", "maximum"))+
  #theme(legend.position="top")
p + theme_minimal()
