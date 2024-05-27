
Image Stitching
This program reads, resizes, and stitches together multiple images into a single panoramic image using OpenCV.

How It Works
1. Read and Resize Images: The read_and_resize function reads images from a specified directory (img/) and resizes them to 800x600 pixels.
2. Concurrent Processing: Images are read and resized concurrently using a ThreadPoolExecutor to improve performance.
3. Image Stitching: The stitch_images function uses OpenCV's Stitcher class to stitch the resized images into a panoramic image.
4. Execution: The main function reads, resizes, and stitches images. It also measures and prints the time taken to stitch the images.

Run the code using the following command from command prompt:
'python stitch_images.py'

NOTE: Ensure you have OpenCV installed.
