import imageio
import datetime

# animation of graph 1
numberOfDay = (datetime.date.today()-datetime.date(2020, 4, 1)).days
datelist = [(datetime.date.today() - datetime.timedelta(days=x)
             ).strftime('%Y-%m-%d') for x in range(1, numberOfDay + 1)][::-1]

images = []

for i in datelist:
    images.append(imageio.imread("data/" + i + "/" + i + "_1.png"))

imageio.mimsave("data/animation/animation_" +
                datelist[-1] + "_graph1" + ".gif", images)

# animation of graph 3
numberOfDay = (datetime.date.today()-datetime.date(2020, 4, 4)).days
datelist = [(datetime.date.today() - datetime.timedelta(days=x)
             ).strftime('%Y-%m-%d') for x in range(1, numberOfDay + 1)][::-1]

images = []

for i in datelist:
    images.append(imageio.imread("data/" + i + "/" + i + "_3.png"))

imageio.mimsave("data/animation/animation_" +
                datelist[-1] + "_graph3" + ".gif", images)
