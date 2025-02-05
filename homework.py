class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self,
        training_type,
        duration,
        distance,
        speed,
        calories
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    LEN_STEP = 0.65
    M_IN_KM = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    K_1 = 0.035
    MIN_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            ) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
    WEIGHT_MULTIPLIER = 0.035
    K_2 = 0.029
    KMH_TO_MS = 0.278
    CM_IN_M = 100

    def get_spent_calories(self):
        speed_m_s = self.get_mean_speed() * self.KMH_TO_MS
        return (
            (self.WEIGHT_MULTIPLIER * self.weight + (
                speed_m_s ** 2 / (self.height / self.CM_IN_M)
            ) * self.K_2 * self.weight)
            * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP = 1.38
    MEAN_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2

    def get_mean_speed(self):
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self):
        calories = (
            (
                self.get_mean_speed() + 1.1
            ) * 2 * self.weight * self.duration
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
