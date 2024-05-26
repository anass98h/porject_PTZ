import cv2
import glob
import concurrent.futures
import time

def read_and_resize(image_path, size=(800, 600)):
    img = cv2.imread(image_path)
    if img is not None:
        img = cv2.resize(img, size)
    return img

# The function is used to stitch images together
# It takes a list of images as input and returns the stitched image
def stitch_images(images):
    stitcher = cv2.Stitcher.create()
    status, stitched_img = stitcher.stitch(images)
    return status, stitched_img

def main():
    image_paths = glob.glob("img/*.jpg")
    images = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        resized_images = executor.map(read_and_resize, image_paths)

    for img in resized_images:
        if img is not None:
            images.append(img)


    start = time.time()
    status, stitched_img = stitch_images(images)
    end = time.time() 

    if status == cv2.Stitcher_OK:
        print("Time taken to stitch the images: ", end - start, " milliseconds")
        cv2.imwrite("img/stitchedOutput.jpg", stitched_img)
    else:
        print("Images could not be stitched!")

if __name__ == "__main__":
    main()
