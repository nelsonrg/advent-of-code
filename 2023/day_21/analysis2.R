library(tidyverse)

data <- read_csv("test_output.csv")

data <- data |>
  mutate(steps = steps+5,
         cycle_num = floor(steps / 11),
         lag_feature = as.factor(steps %% 11))

data |>
  group_by(lag_feature) |>
  mutate(delta = values / lag(values)) |>
  arrange(lag_feature, steps) |>
  View()

ggplot(data,
       aes(x = cycle_num,
           y = values,
           color = lag_feature)) +
  geom_point() +
  geom_line() +
  theme_bw()

model <- lm(values ~ lag_feature*poly(cycle_num, degree = 2),
            data = data |> filter(cycle_num >= 00))

summary(model)

new_data <-
  tibble(
    steps = c(500, 1000, 5000)
  ) |>
  mutate(
    cycle_num = floor((steps - 5) / 11),
    lag_feature = as.factor(steps %% 11)
  )

predict(model, new_data)

par(mfrow=c(2,2))
plot(model)
