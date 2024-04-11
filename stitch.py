# import cv2
# import numpy as np

# # Load the images in grayscale
# img1 = cv2.imread("img/2.jpg", cv2.IMREAD_GRAYSCALE)
# img2 = cv2.imread("img/1.jpg", cv2.IMREAD_GRAYSCALE)

# # Check if images loaded successfully
# if img1 is None or img2 is None:
#     raise ValueError(
#         "Error: Unable to load images. Make sure the file paths are correct."
#     )

# # Initialize SIFT detector
# sift = cv2.SIFT_create()

# # Find the keypoints and descriptors with SIFT
# kp1, des1 = sift.detectAndCompute(img1, None)
# kp2, des2 = sift.detectAndCompute(img2, None)

# # Match descriptors using FLANN matcher
# FLANN_INDEX_KDTREE = 1
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=50)

# flann = cv2.FlannBasedMatcher(index_params, search_params)
# matches = flann.knnMatch(des1, des2, k=2)

# # Store all the good matches as per Lowe's ratio test
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.7 * n.distance:
#         good_matches.append(m)

# # Minimum number of matches to consider the stitching process
# MIN_MATCH_COUNT = 10
# if len(good_matches) > MIN_MATCH_COUNT:
#     src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#     dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

#     # Find homography
#     M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

#     # Use homography
#     height, width = img2.shape
#     img1_aligned = cv2.warpPerspective(img1, M, (width * 2, height))

#     # Now place the second image within the panorama
#     panorama = img1_aligned
#     panorama[0:height, 0:width] = img2

#     # Save the stitched image
#     cv2.imwrite("img/panorama.jpg", panorama)
#     print("The panorama has been saved to 'panorama.jpg'")
# else:
#     print("Not enough matches found - %d/%d" % (len(good_matches), MIN_MATCH_COUNT))


# ============COLOR IMAGE STITCHING================
# import cv2
# import numpy as np

# MIN_MATCH_COUNT = 10

# # Load the images in color
# img1_color = cv2.imread("img/2.jpg")  # queryImage
# img2_color = cv2.imread("img/1.jpg")  # trainImage

# # Convert to grayscale for feature detection
# img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
# img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)

# # Initialize SIFT detector
# sift = cv2.SIFT_create()

# # Find the keypoints and descriptors with SIFT
# kp1, des1 = sift.detectAndCompute(img1, None)
# kp2, des2 = sift.detectAndCompute(img2, None)

# # FLANN parameters
# FLANN_INDEX_KDTREE = 1
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=50)

# # FLANN based matcher
# flann = cv2.FlannBasedMatcher(index_params, search_params)
# matches = flann.knnMatch(des1, des2, k=2)

# # Need to draw only good matches, so create a mask
# matchesMask = [[0, 0] for i in range(len(matches))]

# # Ratio test as per Lowe's paper
# good = []
# for i, (m, n) in enumerate(matches):
#     if m.distance < 0.75 * n.distance:
#         good.append(m)
#         matchesMask[i] = [1, 0]

# # Homography if enough matches are found
# if len(good) > MIN_MATCH_COUNT:
#     src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
#     dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

#     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

#     # Warp the image using the homography
#     h, w, d = img2_color.shape
#     img1_warped = cv2.warpPerspective(img1_color, M, (w, h))

#     # Now place the second image within the panorama
#     panorama = np.maximum(img1_warped, img2_color)

#     # Save the stitched image
#     cv2.imwrite("img/panorama_color.jpg", panorama)
#     print("The panorama has been saved to 'panorama_color.jpg'")
# else:
#     print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))


import cv2
import numpy as np

# Load the images in color
img1_color = cv2.imread("img/4.jpg")  # queryImage
img2_color = cv2.imread("img/3.jpg")  # trainImage

# Convert to grayscale for feature detection
img1_gray = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)

# Initialize SIFT detector
sift = cv2.SIFT_create()

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1_gray, None)
kp2, des2 = sift.detectAndCompute(img2_gray, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

# FLANN based matcher
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Ratio test as per Lowe's paper
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

# Homography if enough matches are found
MIN_MATCH_COUNT = 10
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Warp the image using the homography
    h1, w1, d = img1_color.shape
    h2, w2, d = img2_color.shape
    img1_warped = cv2.warpPerspective(img1_color, M, (w1 + w2, max(h1, h2)))

    # Create a mask representing the area of the warped image
    img2_mask = np.zeros((h2, w2), dtype=np.uint8)
    img2_mask.fill(255)

    # Warp the mask to get the new mask
    img1_mask_warped = cv2.warpPerspective(img2_mask, M, (w1 + w2, max(h1, h2)))

    # Inverse the mask to get the area to blend on the warped image
    img1_mask_warped_inv = cv2.bitwise_not(img1_mask_warped)

    # Use the mask to create the blended panorama
    img1_warped_blended = cv2.bitwise_and(
        img1_warped, img1_warped, mask=img1_mask_warped_inv
    )
    img2_placed = np.zeros_like(img1_warped, dtype=np.uint8)
    img2_placed[:h2, :w2] = img2_color

    # Combine the two
    panorama = cv2.add(img1_warped_blended, img2_placed)

    # Save the stitched image
    cv2.imwrite("img/panorama_color1.jpg", panorama)
else:
    print(f"Not enough matches are found - {len(good)}/{MIN_MATCH_COUNT}")
    panorama = None

# Show the result
if panorama is not None:
    cv2.imshow("Panorama", panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
