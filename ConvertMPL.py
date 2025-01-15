############################################################################
#
#  Program: GDCM (Grassroots DICOM). A DICOM library
#
#  Copyright (c) 2006-2011 Mathieu Malaterre
#  All rights reserved.
#  See Copyright.txt or http://gdcm.sourceforge.net/Copyright.html for details.
#
#     This software is distributed WITHOUT ANY WARRANTY; without even
#     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the above copyright notice for more information.
#
############################################################################

"""
display a DICOM image with matPlotLib via numpy

Caveats:
- Does not support UINT12/INT12

Usage:

 python ConvertMPL.py DICOM_IMAGE_FILE

Thanks:
  plotting example - Ray Schumacher 2009
"""

import gdcm
import numpy
from matplotlib import pyplot as plt


def get_gdcm_to_numpy_typemap():
    """Returns the GDCM Pixel Format to numpy array type mapping."""
    _gdcm_np = {
        gdcm.PixelFormat.UINT8: numpy.uint8,
        gdcm.PixelFormat.INT8: numpy.int8,
        gdcm.PixelFormat.UINT16: numpy.uint16,
        gdcm.PixelFormat.INT16: numpy.int16,
        gdcm.PixelFormat.UINT32: numpy.uint32,
        gdcm.PixelFormat.INT32: numpy.int32,
        gdcm.PixelFormat.FLOAT32: numpy.float32,
        gdcm.PixelFormat.FLOAT64: numpy.float64,
    }
    return _gdcm_np


def get_numpy_array_type(gdcm_pixel_format):
    """Returns a numpy array typecode given a GDCM Pixel Format."""
    return get_gdcm_to_numpy_typemap()[gdcm_pixel_format]


def gdcm_to_numpy(image):
    """Converts a GDCM image to a numpy array."""
    pi = image.GetPhotometricInterpretation()
    pi_type = pi.GetType()
    print("PhotoInterp:", pi)
    if pi_type == 3:
        print("WARNING: Palette image not fully decoded")
    if pi_type == 1:
        cmap = "gray"
    elif pi_type == 2:
        cmap = "gray_r"
    else:
        cmap = None

    pf = image.GetPixelFormat()
    samples_per_pixel = pf.GetSamplesPerPixel()

    assert (
        pf.GetScalarType() in get_gdcm_to_numpy_typemap().keys()
    ), f"Unsupported array type {pf}"

    shape = image.GetDimensions()  # (x, y, z) = (cols, rows, frames)
    shape.reverse()
    if samples_per_pixel > 1:
        shape.append(samples_per_pixel)

    dtype = get_numpy_array_type(pf.GetScalarType())
    image_buffer = image.GetBuffer()
    gdcm_array = image_buffer.encode("utf-8", errors="surrogateescape")  # bytes
    result = numpy.frombuffer(gdcm_array, dtype=dtype)
    result.shape = shape
    return result, cmap


if __name__ == "__main__":
    import sys

    r = gdcm.ImageReader()
    filename = sys.argv[1]
    r.SetFileName(filename)
    if not r.Read():
        sys.exit(1)
    numpy_array, cmap = gdcm_to_numpy(r.GetImage())
    print("numpy_array.shape:", numpy_array.shape)
    print("cmap:", cmap)
    
    grayscale = False
    if cmap is not None:
        grayscale = cmap.startswith("gray")
    # gray (frames, rows, cols) same len as rgb (rows, cols, pix)
    if len(numpy_array.shape) == 4 or (grayscale and len(numpy_array.shape) == 3) :
        # Multi-frame image.
        print(f"Warning: only displaying 3 of {numpy_array.shape[0]} images")
        num_images = min(3, numpy_array.shape[0])
        fig, axs = plt.subplots(1, num_images)
        for idx, ax in enumerate(axs):
            ax.set_title(f"{idx+1}")
            # Many other possible colormaps (cmap).
            ax.imshow(numpy_array[idx], cmap=cmap)
        plt.show()
    else:
        # Single-frame image
        fig, ax = plt.subplots()
        ax.set_title(filename)
        # Many possible colormaps (cmap).
        ax.imshow(numpy_array, cmap=cmap)
        plt.show()
