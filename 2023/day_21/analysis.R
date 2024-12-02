library(tidyverse)

data <- read_csv("test_results.csv")

data <- data |>
  mutate(differences = values - lag(values),
         step_delta = steps - 1,
         cycle_num = floor(steps / 11),
         lag_feature = as.factor(steps %% 11))

model <- lm(differences ~ cycle_num*lag_feature,
            data = data |> filter(step_delta < 250))

summary(model)

yhat <- predict(model, data)

plot(differences ~ step_delta,
     type = "l",
     data = data)
lines(data$step_delta, yhat, type = "l", col = "red")

par(mfrow=c(2,2))
plot(model)

sum(predict(model, data |> filter(step_delta <= 500)))

new_data <- tibble(
  step_delta = 1:1000
) |>
  mutate(cycle_num = floor(step_delta / 11),
         lag_feature = as.factor(step_delta %% 11))

sum(predict(model, new_data))

## Another approach
data |>
  filter(lag_feature == 10) |>
  mutate(d = differences / lag(differences)) |>
  View()

model2 <- lm(differences ~ cycle_num*lag_feature,
             data = data |> filter(step_delta < 250))

summary(model2)
yhat2 <- predict(model2, data)

plot(differences ~ steps,
     type = "l",
     data = data)
lines(data$steps, yhat2, type = "l", col = "red")

sum(predict(model2, data))
