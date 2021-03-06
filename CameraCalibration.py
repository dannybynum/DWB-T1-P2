import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import glob
#import time


def calibrate_me():


    os.chdir('C:/Users/bynum/documents/udacity/term1/DWB-T1-P2')

    test_image = cv2.imread('camera_cal/calibration1.jpg')

    #The Distortion coefficients woulc be obtained by running something like this example:
    #    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, 
    #                                       imgpoints, gray.shape[::-1], None, None)


    # Count the number of inside corners in x for calibration target/board you took pictures of for nx and ny
    # This is needed for the built in cv2 functions for finding the corners in a checkerboard image
    nx = 9
    ny = 6

    # Create arrays to hold Image Points (detected corners) and
    # Object points - real world x,y,z for perfect chessboard representation
    set_of_objpts = []
    set_of_imgpts = []

    # For the objpts array I just use unitless/normalized even spacing to represent a perfect array
    # The units could be anything - whatever scale fits the real world - i.e 1 increment in this array 
    # could represent ~1 inch or 1 ft. or 5.8inches.  Since spacing is all equal the so-called
    # real world object points are just evenly spaced integer numbers - this makes the chessboard a
    # convenient image to use for calibration

    # The format/structure/content of object points array is left-to-right then top to bottom single list of 
    # (x,y,z) points -- so we can may an array of zeros that is nx*ny by 3 as follows:
    objpts = np.zeros(((nx*ny),3), np.float32)

    # objpts is a nx*ny by 3 array but the 3rd value (z) is always zero so we
    # use objpts[:,:2] to say give me all nx*ny rows and give me ":2" two values from each row
    # the .T.reshape interacts with what mgrid is doing to give us the format we want which is
    # [  [0,0,0], [1,0,0], .....[nx,ny,0]] becuase this matches up well with the format
    # that the cv2.findChessboardCorners will return for the image points
    objpts[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)


    # Read in a set of of calibration images that we'll use to calculate distortion coefficients for this camera
    # uses the glob library and function which relies on consistent file names with minor number variations
    paths_of_cal_imgs = glob.glob('camera_cal/calibration*.jpg')
    cal_images_used_count = 0


    # Read in each cal image in succession and if the inside corners arae found
    # then append the list of image points to the overall set of image points so 
    # we can use them to calcualte a camera distortion matrix
    for sing_cal_img_path in paths_of_cal_imgs:
    #for sing_cal_img_path in paths_of_cal_imgs[:3]:
    # uncomment above line to only step through 3 images while building for loop the first time

        fname = sing_cal_img_path
        img = cv2.imread(fname)
        

        # Convert to grayscale -- when using cv2.imread it comes in as BGR
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        corner_found_flag, corners = cv2.findChessboardCorners(img_gray, (nx, ny), None)

        # If found, draw corners
        if corner_found_flag == True:
            ##Draw and display the corners to visulaize the results
            #cv2.drawChessboardCorners(img, (nx, ny), corners, corner_found_flag)
            #plt.imshow(img)
            #plt.show()
            
            # Fixme - I have to close each successive window to see the next one
            # I'd like for it to close and move on to next one after ~2sec
            # plt.show(block=False)
            # time.sleep(5)
            # plt.close('all')

            #if found append this list of image points for a single image to the overall set for this camer
            # and make a count to display how many images used,
            set_of_imgpts.append(corners)
            cal_images_used_count+=1

            # Even though objpts is the same for each image we create a set here to match the size of the set of
            # detected image points to make the next step of creating the transformation  easier
            set_of_objpts.append(objpts)

        else:
            pass
            #print("image", fname, " skipped due to corners not found")

    print("Camera Calibration Completed")
    print("Number of Calibration Images Used = ", cal_images_used_count)

    # For the same of the image we pass into the calibrateCamera function
    # we really just want 1280,720 (in this example) - we get that by taking the values
    # in the gray image and then using the -1 to reverse them.  note that .shape is built into numpy
    img_shape = img_gray.shape[::-1]
    #print (img_shape)

    # Now that we have sets of image points from all calibation images and corresponding sets of ojbect points (same in each set - same chessboard),
    # we can use the built in cv2 function "calibrateCamera" to calculate the camera matrix and distortion matrix we need to un-distort images
    cal_found_flag, cam_mtx, dist_coeffs, cam_rvecs, cam_tvecs = cv2.calibrateCamera(set_of_objpts, set_of_imgpts, img_shape, None, None)

    # Now finally we can "undistort an image", in this case test_img is calibration1.jpg
    # and then we can plot the result.
    undistorted_image = cv2.undistort(test_image, cam_mtx, dist_coeffs, None, cam_mtx)

    return(cam_mtx, dist_coeffs, test_image, undistorted_image)



# # Now plot the result using the subplot feature in matplotlib so you can put the original and undistorted images side by side
# cam_mtx, dist_coeffs, test_image, undistorted_image = CalibrateMe()
# fig, subplt = plt.subplots(1, 2, figsize=(18,7))
# fig.tight_layout()

# subplt[0].imshow(test_image)  #, cmap = 'gray')
# subplt[0].set_title('Original Image', fontsize=10)

# subplt[1].imshow(undistorted_image, cmap='gray')
# subplt[1].set_title('Undistorted Image', fontsize=10)
# plt.show()