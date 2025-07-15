library(tidyverse)
library(here)

data <- read_tsv(here('extractedData', 'all_talkturns_with_sentiment_scores.tsv'), col_names =TRUE)

#make new column: -1 if negative sentiment, 0 if neutral, 1 if positive
sentiment_vector <- rep("unknown", nrow(data))
sentiment_vector <- data$talkturn_sentiment_label

sentiment_vector[data$talkturn_sentiment_label == "negative"] <- -1
sentiment_vector[data$talkturn_sentiment_label == "neutral"]  <-  0
sentiment_vector[data$talkturn_sentiment_label == "positive"] <-  1

data[["sentiment_number_score"]] <- as.numeric(sentiment_vector)
data$session_number_factor <- as.factor(data$session_number)

#data %>%
#  filter(session_number <=300) %>%
#  ggplot(aes(x = session_number_factor, y = sentiment_number_score)) +
#    geom_boxplot()

data %>%
  filter(talkturn_num_words >= 8, session_number <= 100) %>%
  group_by(session_number, patient_or_therapist) %>%
  mutate(avg_sentiment_number = mean(sentiment_number_score)) %>%
  select(patient_or_therapist, avg_sentiment_number, session_number) %>%
  unique %>%
   ggplot(aes(x = session_number, y = avg_sentiment_number, color = patient_or_therapist)) +
    geom_line() + 
    theme_minimal()
