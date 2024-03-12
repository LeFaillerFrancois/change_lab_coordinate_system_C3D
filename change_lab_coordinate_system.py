# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:25:11 2024

@author: flefaill
"""

import btk
import numpy as np

def change_lab_coordinate_system(filename, transform_type="y_to_x", overwrite=False):
    """
    Change the coordinate system of the markers in a motion capture file.

    Parameters:
        filename (str): The name of the c3d file to be modified.
        transform_type (str, optional): The type of transformation to be applied. 
            Options are "y_to_x" (default) or "y_to_z".
        overwrite (bool, optional): Whether to overwrite the original file with the transformed data. 
            If False (default), the modified data is saved as "modified_filename".

    Returns:
        None
    """
    
    # Define the rotation matrix based on the transform_type argument
    if transform_type == "y_to_x":
        # Rotation matrix around z axis for switching coordinate systems from Y-axis to X-axis
        rotate_matrix = np.array([[0, -1, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]])
    elif transform_type == "y_to_z":
        # Rotation matrix around x axis for switching coordinate systems from Y-axis up to Z-axis up
        rotate_matrix = np.array([[1, 0, 0],
                                  [0, 0, 1],
                                  [0, -1, 0]])
    else:
        # Default to y_to_x transform if an invalid transform_type is provided up
        rotate_matrix = np.array([[0, -1, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]])

    # Load a c3d file and return its acquisition
    def load_c3d(filename):
        reader = btk.btkAcquisitionFileReader()
        reader.SetFilename(filename)
        reader.Update()
        acq = reader.GetOutput()
        return acq

    # Perform matrix multiplication between each marker coordinates and the rotation matrix for each frame
    def rotate(marker):
        for i in range(len(marker)):
            marker[i,:] = marker[i,:] @ rotate_matrix
        return marker

    acq = load_c3d(filename)  # Load the desired c3d file
    nb_marker = acq.GetPointNumber()  # Number of markers

    # Iterate through all markers of the acquisition and replace the coordinates of the markers with their transformed coordinates
    for i in range(nb_marker):
        marker = acq.GetPoint(i)  # Select marker i
        marker_temp = marker.GetValues()  # Get coordinates of marker i
        marker_temp = rotate(marker_temp)  # Matrix multiplication for each frame
        marker.SetValues(marker_temp)  # Replace with the new coordinates

    # Write to the c3d file if overwrite is True
    writer = btk.btkAcquisitionFileWriter()
    writer.SetInput(acq)
    if overwrite:
        writer.SetFilename(filename)
    else : 
        new_file_name = "modified_"+filename
        writer.SetFilename(new_file_name)
    writer.Update()


# Example usage:
#------------------------------------------------------------------------------

# Usage: change_lab_coordinate_system("Gait_05.c3d", transform_type="y_to_z", overwrite=True)
