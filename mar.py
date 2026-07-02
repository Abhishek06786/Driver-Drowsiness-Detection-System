from scipy.spatial import distance

def mouth_aspect_ratio(mouth):

    vertical = distance.euclidean(mouth[2], mouth[3])

    horizontal = distance.euclidean(mouth[0], mouth[1])

    mar = vertical / horizontal

    return mar