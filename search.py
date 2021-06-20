from colordescriptor import ColorDescriptor
from seacher import Searcher
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required=True, help="Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required=True, help="Path to the query image")
ap.add_argument("-r", "--result-path", required=True, help="Path to the result path")
args = vars(ap.parse_args())

# BGR
cd = ColorDescriptor((10, 12, 4))

# load the query image and describe it
query = cv2.imread(args["query"])
features = cd.describe2d(query)

# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features)
if results is not None:
    # display the query
    cv2.imshow("Query", query)
    # loop over the results
    for (score, resultID) in results[:10]:
        # load the result image and display it
        print(resultID)
        print(score)
        result = cv2.imread(args["result_path"] + "/" + resultID)
        cv2.imshow("Result", result)
        cv2.waitKey(0)
else:
    print("Not found")
