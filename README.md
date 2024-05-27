
# Synchronized PTZ Camera Control for Panoramic Imaging

This repository contains the source code and associated files for the project on synchronized Pan-Tilt-Zoom (PTZ) camera control for panoramic imaging, aimed at enhancing surveillance systems by creating comprehensive panoramic views from multiple cameras.

## Repository Structure

- `/model_and_synchronization` - Contains the code for modeling and synchronizing PTZ cameras.
  - `panoramic_images.py` - Python script for simulating panoramic views using PTZ camera inputs.
- `/Stitch_images` - Contains the code and resources for stitching multiple images into a single panoramic image.
  - `stitch_images.py` - Python script that implements the image stitching functionality.
  - `/img` - Directory containing sample images used for testing the stitching process.

## Setup and Installation

1. **Clone the Repository:**
   ```
   git clone https://github.com/anass98h/porject_PTZ.git
   ```
2. **Navigate to the Project Directory:**
   ```
   cd porject_PTZ
   ```

### Dependencies

Ensure you have Python installed on your system. The projects use various libraries, which you can install using the following command:
```
pip install pygame opencv-python-headless
```

## Usage

### Model and Synchronization

Navigate to the `/model_and_synchronization` directory:
```
cd model_and_synchronization
```
To run the panoramic viewer, execute:
```
python panoramic_images.py
```
This script utilizes Pygame to simulate a PTZ (Pan, Tilt, Zoom) camera system for panoramic viewing. Below are detailed instructions on how to interact with the simulation:

- **Zooming**: Use the `up arrow` key to zoom in and the `down arrow` key to zoom out.
- **Camera Selection**: Press number keys `1` through `5` to select different cameras for individual control.
- **Moving Selected Camera**: Once a camera is selected, use the keys:
  - `J` to move left
  - `L` to move right
  - `I` to move up
  - `K` to move down
- **Panoramic Navigation**: 
  - Use `W` to move all cameras up
  - Use `A` to move all cameras left
  - Use `S` to move all cameras down
  - Use `D` to move all cameras right
- **Click Navigation**: Clicking on the background image will move all cameras to center on the click location.
- **Add/Remove Cameras**:
  - Press `Z` to add a camera (up to a predefined limit).
  - Press `X` to remove a camera (cannot reduce below one camera).

This interactive simulation allows users to explore different configurations and control schemes of a PTZ camera network, adjusting views dynamically to simulate surveillance operations.

### Stitch Images

Navigate to the `/Stitch_images` directory:
```
cd Stitch_images
```
Run the Python script:
```
python stitch_images.py
```
This script reads images from the `img/` directory, resizes them uniformly, and stitches them together into a single panoramic image using OpenCV's `Stitcher` class. Here’s a brief rundown of its operation:

- **Concurrent Image Processing**: Images are processed in parallel to improve performance.
- **Stitching**: The final panoramic image is compiled and output, with performance metrics reported, including the time taken to stitch the images.

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request. For significant changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

For any queries regarding this project, please contact us through the GitHub issue tracker associated with this repository.

## Acknowledgments

- Thanks to SAAB Air Traffic Management for their collaboration.
- Thanks to all contributors and testers who have helped to refine these systems.
