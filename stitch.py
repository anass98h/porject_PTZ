import cv2
import numpy as np

# Load the images in grayscale
img1 = cv2.imread("img/2.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("img/1.jpg", cv2.IMREAD_GRAYSCALE)

# Check if images loaded successfully
if img1 is None or img2 is None:
    raise ValueError(
        "Error: Unable to load images. Make sure the file paths are correct."
    )

# Initialize SIFT detector
sift = cv2.SIFT_create()

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# Match descriptors using FLANN matcher
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Store all the good matches as per Lowe's ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Minimum number of matches to consider the stitching process
MIN_MATCH_COUNT = 10
if len(good_matches) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Find homography
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Use homography
    height, width = img2.shape
    img1_aligned = cv2.warpPerspective(img1, M, (width * 2, height))

    # Now place the second image within the panorama
    panorama = img1_aligned
    panorama[0:height, 0:width] = img2

    # Save the stitched image
    cv2.imwrite("img/panorama.jpg", panorama)
    print("The panorama has been saved to 'panorama.jpg'")
else:
    print("Not enough matches found - %d/%d" % (len(good_matches), MIN_MATCH_COUNT))
