# -*- coding: utf-8 -*-
#Created on Wed May 14 18:17:38 2025
#@authors: Andrea Faggi (Python) & Erika Brattich (R)

#clean environment first
rm(list=ls())

# Load required libraries
library(readr)
library(dplyr)
library(tidyr)


# Set working directory
setwd('C:/Users/erika.brattich2/Downloads/prova/stats/')

# Initialize empty dataframes
image_sr <- NULL
box1_sr <- NULL
line1_sr <- NULL
cursor1_sr <- NULL

# Loop through files (frames): pay attention to their number and eventually change it
for (i in 0:247) {
  # Read fixed-width file
  b <- read_fwf(paste0('Rec-Lab_prova-000001_', i, ' - Stats.txt'), 
                col_positions = fwf_widths(rep(31, 5)))
  
  # Rename columns; the names have to change depending on your choice of cursors, boxes, ...
  colnames(b) <- c('Statistic', 'Image', 'Box 1', 'Line 1', 'Cursor 1')
  
  # Filter and transpose specific rows
  b_filtered <- b %>%
    filter(Statistic %in% c('Mean [C]', 'Std. Dev. [C]', 'Center [C]', 
                            'Maximum [C]', 'Minimum [C]', 'Number of Pixels'))
  
  # Extract specific statistics
  image_temp <- data.frame(
    Mean = b_filtered$Image[b_filtered$Statistic == 'Mean [C]'],
    StdDev = b_filtered$Image[b_filtered$Statistic == 'Std. Dev. [C]'],
    Max = substr(b_filtered$Image[b_filtered$Statistic == 'Maximum [C]'], nchar(b_filtered$Image[b_filtered$Statistic == 'Maximum [C]'])-4, nchar(b_filtered$Image[b_filtered$Statistic == 'Maximum [C]'])),
    Min = substr(b_filtered$Image[b_filtered$Statistic == 'Minimum [C]'], nchar(b_filtered$Image[b_filtered$Statistic == 'Minimum [C]'])-4, nchar(b_filtered$Image[b_filtered$Statistic == 'Minimum [C]']))
  )
  
  box1_temp <- data.frame(
    Mean = b_filtered$`Box 1`[b_filtered$Statistic == 'Mean [C]'],
    StdDev = b_filtered$`Box 1`[b_filtered$Statistic == 'Std. Dev. [C]'],
    Max = substr(b_filtered$`Box 1`[b_filtered$Statistic == 'Maximum [C]'], nchar(b_filtered$`Box 1`[b_filtered$Statistic == 'Maximum [C]'])-4, nchar(b_filtered$`Box 1`[b_filtered$Statistic == 'Maximum [C]'])),
    Min = substr(b_filtered$`Box 1`[b_filtered$Statistic == 'Minimum [C]'], nchar(b_filtered$`Box 1`[b_filtered$Statistic == 'Minimum [C]'])-4, nchar(b_filtered$`Box 1`[b_filtered$Statistic == 'Minimum [C]']))
  )
  
  line1_temp <- data.frame(
    Mean = b_filtered$`Line 1`[b_filtered$Statistic == 'Mean [C]'],
    StdDev = b_filtered$`Line 1`[b_filtered$Statistic == 'Std. Dev. [C]'],
    Max = substr(b_filtered$`Line 1`[b_filtered$Statistic == 'Maximum [C]'], nchar(b_filtered$`Line 1`[b_filtered$Statistic == 'Maximum [C]'])-4, nchar(b_filtered$`Line 1`[b_filtered$Statistic == 'Maximum [C]'])),
    Min = substr(b_filtered$`Line 1`[b_filtered$Statistic == 'Minimum [C]'], nchar(b_filtered$`Line 1`[b_filtered$Statistic == 'Minimum [C]'])-4, nchar(b_filtered$`Line 1`[b_filtered$Statistic == 'Minimum [C]']))
  )
  
  cursor1_temp <- data.frame(
    Mean = b_filtered$`Cursor 1`[b_filtered$Statistic == 'Mean [C]'],
    StdDev = b_filtered$`Cursor 1`[b_filtered$Statistic == 'Std. Dev. [C]'],
    Max = substr(b_filtered$`Cursor 1`[b_filtered$Statistic == 'Maximum [C]'], nchar(b_filtered$`Cursor 1`[b_filtered$Statistic == 'Maximum [C]'])-4, nchar(b_filtered$`Cursor 1`[b_filtered$Statistic == 'Maximum [C]'])),
    Min = substr(b_filtered$`Cursor 1`[b_filtered$Statistic == 'Minimum [C]'], nchar(b_filtered$`Cursor 1`[b_filtered$Statistic == 'Minimum [C]'])-4, nchar(b_filtered$`Cursor 1`[b_filtered$Statistic == 'Minimum [C]']))
  )
  
  # Combine results
  if (is.null(image_sr)) {
    image_sr <- image_temp
    box1_sr <- box1_temp
    line1_sr <- line1_temp
    cursor1_sr <- cursor1_temp
  } else {
    image_sr <- rbind(image_sr, image_temp)
    box1_sr <- rbind(box1_sr, box1_temp)
    line1_sr <- rbind(line1_sr, line1_temp)
    cursor1_sr <- rbind(cursor1_sr, cursor1_temp)
  }
}

# Convert to numeric
image_sr[] <- lapply(image_sr, as.numeric)
box1_sr[] <- lapply(box1_sr, as.numeric)
line1_sr[] <- lapply(line1_sr, as.numeric)
cursor1_sr[] <- lapply(cursor1_sr, as.numeric)

#add a column index, corresponding to the frame - comment if you do not need it
image_sr$ID <- seq.int(nrow(image_sr))
box1_sr$ID <- seq.int(nrow(box1_sr))
line1_sr$ID <- seq.int(nrow(line1_sr))
cursor1_sr$ID <- seq.int(nrow(cursor1_sr))


setwd('C:/Users/erika.brattich2/Downloads/prova/')

# Save dataframes as csv (change to write.table if you prefer other types of txt files)
write.csv(image_sr, 'stats_image.csv', row.names = FALSE)
write.csv(box1_sr, 'stats_box1.csv', row.names = FALSE)
write.csv(line1_sr, 'stats_line1.csv', row.names = FALSE)
write.csv(cursor1_sr, 'stats_cursor1.csv', row.names = FALSE)
