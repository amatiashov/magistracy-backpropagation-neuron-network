"""
Тест состоит в следующем. Выберим на плоскости несколько точек так, можно было определить
некую область с центром в данной точке. Для этого удобно выбрать по одной точке в каждой четверти
координатной плоскости и еще несколько поблизости. Обозначим их A, B, C, D, E.
Теперь в цикле будет генерировать точки на плоскости XOY с нормальным законом распределения
с математическим ожиданием A (или B, или C, или D, или E последовательно) и средним квадратическим
отклонением dispersion и подавать на вход созданного слоя. В результате за N итераций сеть должна
распределить векторы каждого нейрона таким образом, чтобы он максимально совпадал с математическим
ожиданием каждого кластера и при подаче на вход точки, принадлежащей одному из классов, сеть должна
откликнуться единице лишь одним нейроном, а остальные должны выдать нуль.

                                ^
                                |   
                                |             
                                |            B(10, 10)
                                |           *       C(13, 6)
                                |                  *
                                |                 D(5, 4)
                                |               *
                                |     A(2, 2)
                                |   *
                                |
       -------------------------|--------------------------->
                    E(-1, -5)   |
                   *            |
                                |
                                |
                                |
                                |
                                |
                                |
                                |
"""
from random import gauss
from entities.counter_propagation.kohonen_layer import KohonenLayer

# точки математического ожидания для обучения
A = [2, 2]
B = [10, 10]
C = [13, 6]
D = [5, 4]
E = [-1, -5]

# создаем слой с 4 нейронами (по количеству точек) и числом входов 2
layer = KohonenLayer(name="test", number_neurons_in_layer=5, number_of_input_signal=2,
                     use_normalize_data=True, auto_save=False)
# среднее квадратическое отклонение
dispersion = 0.1


def print_result(count, d, *args):
    print("*****************************")
    for arg in args:
        print("-------------{}".format(arg))
        for j in range(count):
            x = [gauss(arg[0], d), gauss(arg[1], d)]
            print(layer.calculate(x), "\t\t", x)
        print("--------------------")
    print("*****************************")

for i in range(1000000):
    layer.learn([gauss(A[0], dispersion), gauss(A[1], dispersion)])
    layer.learn([gauss(B[0], dispersion), gauss(B[1], dispersion)])
    layer.learn([gauss(C[0], dispersion), gauss(C[1], dispersion)])
    layer.learn([gauss(D[0], dispersion), gauss(D[1], dispersion)])
    layer.learn([gauss(E[0], dispersion), gauss(E[1], dispersion)])
    if i % 10000 == 0:
        print_result(5, dispersion, A, B, C, D, E)
