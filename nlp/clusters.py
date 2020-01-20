
from math import sqrt
import random

# from PIL import Image, ImageDraw

VERBOSE = 0


def pearson(v1, v2):
    """Defining closeness between 2 lists of numbers. It uses the Pearson
       correlation. Returns the Pearson correlation coefficient for p1
       and p2.

       The Pearson correlation will try to determine how well two sets of
       data fit onto a straight line. The Pearson correlation code for this
       module will take two lists of numbers and return their correlation
       score.

       Remember that the Pearson correlation is 1.0 when two items match
       perfectly, and is close to 0.0 when there’s no relationship at all.

    """
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)
    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1))
               * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0
    return 1.0 - num / den


class bicluster:
    """Each cluster in a hierarchical clustering algorithm is either a
       point in the tree with two branches, or an endpoint associated
       with an actual row from the dataset (in this case, a
       blog). Each cluster also contains data about its location,
       which is either the row data for the endpoints or the merged
       data from its two branches for other node types.
    """

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hcluster(rows, distance=pearson):
    """Hierarchical clustering builds up a hierarchy of groups by
       continuously merging the two most similar groups. Each of these
       groups starts as a single item, in this case an individual
       blog. In each iteration this method calculates the distances
       between every pair of groups, and the closest ones are merged
       together to form a new group.

       Creating and storing the distances.
    """
    distances = {}
    currentclustid = -1
    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]
    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(
                        clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:
                    closest = d
                    lowestpair = (i, j)
        # calculate the average of the two clusters
        mergevec = [
            (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
            for i in range(len(clust[0].vec))]
        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest, id=currentclustid)
        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    return clust[0]


def readfile(filename):
    """Reading the matrix file."""
    lines = None
    with open(filename) as _file:
        lines = [line for line in _file.readlines()]
    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def printclust(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    for i in range(n):
        pass
        # print(' '),
    if clust.id < 0:
        # negative id means that this is branch
        # print('-')
        pass
    else:
        # positive id means that this is an endpoint
        if labels is None:
            # print(clust.id)
            pass
        else:
            pass
            # print(labels[clust.id])
    # now print the right and left branches
    if clust.left is not None:
        printclust(clust.left, labels=labels, n=n + 1)
    if clust.right is not None:
        printclust(clust.right, labels=labels, n=n + 1)


def getheight(clust):
    """Defining the height of a cluster."""
    # Is this an endpoint? Then the height is just 1
    if clust.left is None and clust.right is None:
        return 1
    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left is None and clust.right is None:
        return 0
    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))
        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))
        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll,
                   bottom - h2 / 2), fill=(255, 0, 0))

        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


# def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
#     # height and width
#     h = getheight(clust) * 20
#     w = 1200
#     depth = getdepth(clust)
#     # width is fixed, so scale distances accordingly
#     scaling = float(w - 150) / depth
#     # Create a new image with a white background
#     img = Image.new('RGB', (w, h), (255, 255, 255))
#     draw = ImageDraw.Draw(img)
#     draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))
#     # Draw the first node
#     drawnode(draw, clust, 10, (h / 2), scaling, labels)
#     img.save(jpeg, 'JPEG')


def hcluster_to_json(clust, labels=None):
    """Turning a cluster to a json object with children.
    Example of the returned object:
    {
        name: 'TheName',
        children: [
            {
                name: "first TheName's child",
                children: [
                    {...}, {...}, {...}
                ]
            }, {
                name: "second TheName's child",
                children: [
                    {...}, {...}, {...}
                ]
            }
        ]
    }
    """
    root = {}

    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)
    # width is fixed, so scale distances accordingly
    scaling = float(w - 150) / depth

    def processnode(node, x: int, y: int, scaling, parent: dict = None):
        """Processing cluster nodes."""

        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2

        # Line length
        ll = clust.distance * scaling

        obj = {} if parent else root

        # obj.update(dict(x=int(x), y=int(y), id=node.id))

        if node.id < 0:
            # this is a branch
            obj['type'] = 'branch'
            # obj['name'] = 'branch'
            # a branch should always have children
            if 'children' not in obj:
                obj['children'] = []
            if parent:
                parent['children'].append(obj)

            processnode(
                node.left, x=x + ll, y=top + h1 / 2,
                scaling=scaling, parent=obj)
            processnode(
                node.right, x=x + ll, y=bottom - h2 / 2,
                scaling=scaling, parent=obj)
        else:
            # this is an actual node (leaf)
            obj['size'] = sum(node.vec)
            obj['type'] = 'node'
            obj['name'] = labels[node.id]

            # a node always expects a parent
            parent['children'].append(obj)

    processnode(clust, x=10, y=h / 2, scaling=scaling)

    return root, depth


def rotatematrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def kcluster(rows, distance=pearson, k=4):
    """
    Rendering a k-means cluster.
    :param rows:
    :param distance:
    :param k:
    :return:
    """
    # Determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
              for i in range(len(rows[0]))]
    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))] for j in range(k)]
    lastmatches = None
    bestmatches = []
    for t in range(100):
        if VERBOSE:
            pass
            # print('Iteration %d' % t)
        bestmatches = [[] for i in range(k)]
        # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)
        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches

        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs
    return bestmatches


def print_clusters(kclust, rows):
    """Printing the clusters."""
    for k in kclust:
        # print('\n')
        # print([rows[_] for _ in k])
        pass


def get_clusters(kclust, rows):
    """Getting the titles for the clusters."""
    out = []
    for k in kclust:
        out.append([rows[_] for _ in k])
    return out


def tanimoto(v1, v2):
    """
    """
    c1, c2, shr = 0, 0, 0
    for i in range(len(v1)):
        if v1[i] != 0:
            c1 += 1  # in v1
        if v2[i] != 0:
            c2 += 1  # in v2
        if v1[i] != 0 and v2[i] != 0:
            shr += 1  # in both
    return 1.0 - (float(shr) / (c1 + c2 - shr))


def scaledown(data, distance=pearson, rate=0.01):
    n = len(data)

    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)]
                for i in range(0, n)]

    # Randomly initialize the starting points of the locations in 2D
    loc = [[random.random(), random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                           for x in range(len(loc[i]))]))

        # Move points
        grad = [[0.0, 0.0] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                # The error is percent difference between the distances

                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]
                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                grad[k][0] += ((loc[k][0] - loc[j][0]) /
                               fakedist[j][k]) * errorterm
                grad[k][1] += ((loc[k][1] - loc[j][1]) /
                               fakedist[j][k]) * errorterm

                # Keep track of the total error
                totalerror += abs(errorterm)
        if VERBOSE:
            pass
            # print(totalerror)

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror:
            break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]

    return loc


# def draw2d(data, labels, jpeg='mds2d.jpg'):
#     img = Image.new('RGB', (2000, 2000), (255, 255, 255))
#     draw = ImageDraw.Draw(img)
#     for i in range(len(data)):
#         x = (data[i][0] + 0.5) * 1000
#         y = (data[i][1] + 0.5) * 1000
#         draw.text((x, y), labels[i], (0, 0, 0))
#     img.save(jpeg, 'JPEG')


# def main():
#
#     # blognames,words,data
#     rows, cols, data = readfile('data/blogdata.txt')
#
#     # clust = hcluster(data)
#     # # printclust(clust, labels=rows)
#     # drawdendrogram(clust, rows, jpeg='blogclust.jpg')
#
#     # rdata = rotatematrix(data)
#     # wordclust = hcluster(rdata)
#     # drawdendrogram(wordclust, labels=cols, jpeg='wordclust.jpg')
#
#     # k-means clustering
#
#     kclust = kcluster(data, k=10)
#     print_clusters(kclust, rows)
#
#     # wants, people, data = readfile('txtdata/zebo.txt')
#     # clust = hcluster(data, distance=tanimoto)
#     # drawdendrogram(clust, wants)
#
#     # blognames, words, data = readfile('txtdata/blogdata.txt')
#     # coords = scaledown(data)
#     # draw2d(coords, blognames, jpeg='blogs2d.jpg')
#
#
# if __name__ == "__main__":
#     main()
