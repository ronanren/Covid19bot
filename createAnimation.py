import imageio
import datetime

# (0) Prendre en compte les graphiques jusqu'a aujourd'hui
# (1) Prendre en compte les graphiques jusqu'a hier
aujd = 1

# Animation du graphe 1
numberOfDay = (datetime.date.today()-datetime.date(2020, 3, 18)).days
datelist = [(datetime.date.today() - datetime.timedelta(days=x)
             ).strftime('%Y-%m-%d') for x in range(aujd, numberOfDay + 1)][::-1]

images = []

for i in datelist:
    images.append(imageio.imread("data/" + i + "/" + i + "_1.png"))


imageio.mimsave("data/animation/animation_" + datelist[-1] + "_graph1" + ".gif", images, fps = 7.5)

# Animation du graphe 2
numberOfDay = (datetime.date.today()-datetime.date(2020, 3, 18)).days
datelist = [(datetime.date.today() - datetime.timedelta(days=x)
             ).strftime('%Y-%m-%d') for x in range(aujd, numberOfDay + 1)][::-1]

images = []

for i in datelist:
    images.append(imageio.imread("data/" + i + "/" + i + "_2.png"))

imageio.mimsave("data/animation/animation_" + datelist[-1] + "_graph2" + ".gif", images, fps = 7.5)

# Animation du graphe 3
numberOfDay = (datetime.date.today()-datetime.date(2020, 4, 17)).days
datelist = [(datetime.date.today() - datetime.timedelta(days=x)
             ).strftime('%Y-%m-%d') for x in range(aujd, numberOfDay + 1)][::-1]

images = []

for i in datelist:
    images.append(imageio.imread("data/" + i + "/" + i + "_3.png"))

imageio.mimsave("data/animation/animation_" + datelist[-1] + "_graph3" + ".gif", images, fps = 7.5)
