# -*- coding: utf-8 -*-
"""
  feature_helpers.py
  
  @authors: @MichaelCurrie, @JimHokanson
  
  Some helper functions that assist in the calculation of the attributes of
  WormFeatures
  
  
  © Medical Research Council 2012
  You will not remove any copyright or other notices from the Software; 
  you must reproduce all copyright notices and other proprietary 
  notices on any copies of the Software.

"""
import numpy as np
import collections
from wormpy import config

__ALL__ = ['get_worm_velocity',
           'get_bends', 
           'get_amplitude_and_wavelength', 
           'get_eccentricity_and_orientation']  # for posture


def get_angle():
  """
    get_angle: obtain the angle of a subset of the 49 points of a worm for
               each frame
    
    returns: A numpy array of shape (n) and stores the worm body's "angle" 
             for each frame of video
    
  """
  body_x, body_y = nw.get_partition('body', 'skeletons', True)  # shape (33, n)
  # diff calculates each body point difference between the 33 body points
  # the we take the mean of these differences for each frame
  average_diff_x = np.nanmean(np.diff(body_x, n=1, axis=0), axis=0)# shape (n)
  average_diff_y = np.nanmean(np.diff(body_y, n=1, axis=0), axis=0)# shape (n)
  
  # body_angle has shape (n) and stores the worm body's "angle" 
  # for each frame of video
  body_angle = np.arctan2(average_diff_y, average_diff_x) * (180 / np.pi)

  return body_angle

def get_worm_velocity(nw, ventral_mode=0):
  """
    get_worm_velocity:
      Compute the worm velocity (speed & direction) at the
      head-tip/head/midbody/tail/tail-tip
   
    INPUTS: nw: a NormalizedWorm instance
            ventral_mode: the ventral side mode:
              0 = unknown
              1 = clockwise
              2 = anticlockwise
    %   Outputs:
    TODO: fix this description to mention it is a dictionary
          velocity - the worm velocity; each field has subfields for the
            "speed" and "direction":
              headTip = the tip of the head (1/12 the worm at 0.25s)
              head    = the head (1/6 the worm at 0.5s)
              midbody = the midbody (2/6 the worm at 0.5s)
              tail    = the tail (1/6 the worm at 0.5s)
              tailTip = the tip of the tail (1/12 the worm at 0.25s)



  """

  # Let's use some partitions.  
  # NOTE: head_tip and tail_tip overlap head and tail, respectively, and
  #       this set of partitions does not cover the neck and hips
  partition_keys = ['head_tip', 'head', 'midbody', 'tail', 'tail_tip']
  
  body_angle = get_angle()
  
  TIME_SCALES = \
    {
      'head_tip': config.TIP_DIFF,
      'head': config.BODY_DIFF,
      'midbody': config.BODY_DIFF,
      'tail': config.BODY_DIFF,
      'tail_tip': config.TIP_DIFF
    }  
  
  for partition_key in partition_keys:
    x, y = nw.get_partition(partition_key, 'skeletons', True)
    h__compute_velocity(x, y, body_angle, 
                        TIME_SCALES[partition_key], ventral_mode)
  
  return 0

def h__compute_velocity(x, y, body_angle, time_scale, ventral_mode=0):
  """
    h__compute_velocity:
      The velocity is computed not using the nearest values but values
      that are separated by a sufficient time (scale_time). If the encountered 
      values are not valid, the width of time is expanded up to a maximum of
      2*scale_time (or technically, 1 scale time in either direction)

      INPUT:
        x, y: two numpy arrays of shape (p, n) where p is the size of the 
              partition of worm's 49 points, and n is the number of frames 
              in the video
              
        body_angle: the angle between the mean of the first-order differences
        
        time_scale: either config.TIP_DIFF or config.BODY_DIFF, which are
                    fractions like 0.5 or 0.25.
        
        ventral_mode: the ventral side mode:
              0 = unknown
              1 = clockwise
              2 = anticlockwise
              
  """
  num_frames = np.shape(x)[1]
  
  # TODO: insert description of what sampling_scale is used for
  
  # We require sampling_scale to be an odd integer
  # We calculate the scale as a scalar multiple of FPS.  We require the 
  # scalar multiple of FPS to be an ODD INTEGER.
  ostensive_sampling_scale = time_scale * config.FPS
  
  # We need sampling_scale to be an odd integer, so 
  # first we check if we already have an integer.
  if((ostensive_sampling_scale).is_integer()):
    # In this case ostensive_sampling_scale is an integer.  
    # But is it odd or even?
    if(ostensive_sampling_scale % 2 == 0): # EVEN so add one
      sampling_scale = ostensive_sampling_scale + 1
    else:                                  # ODD
      sampling_scale = ostensive_sampling_scale
  else:
    # Otherwise, ostensive_sampling_scale is not an integer, 
    # so take the nearest odd integer
    sampling_scale_low  = np.floor(ostensive_sampling_scale)
    sampling_scale_high = np.ceil(ostensive_sampling_scale)
    if(sampling_scale_high % 2 == 0): 
      sampling_scale = sampling_scale_low
    else:
      sampling_scale = sampling_scale_high

  # Create numpy arrays filled with NaNs to start with
  speed          = np.empty((1, num_frames)).fill(np.NaN)
  direction      = np.empty((1, num_frames)).fill(np.NaN)
  body_direction = np.empty((1, num_frames)).fill(np.NaN)
  
  # If we don't have enough frames to satisfy our sampling_scale,
  # return with nothing.
  if(sampling_scale > num_frames):
      velocity = {'speed': speed, 'direction': direction}
      return velocity

  # Compute the body part direction.

  # ME: add get_angle() here....

  d_x = nanmean(diff(x(pointsI,:), 1, 1), 1)
  d_y = nanmean(diff(y(pointsI,:), 1, 1), 1)
  
  pointAngle = atan2(d_y, d_x) * (180 / pi)
  
  # Compute the coordinates.
  x_mean = mean(x(pointsI,:), 1)
  y_mean = mean(y(pointsI,:), 1)
  
  # Compute the speed using back/front nearest neighbors bounded at twice the scale.
  scale_minus_1 = sampling_scale - 1
  half_scale    = scale_minus_1 / 2
  
  start_index = 1+half_scale
  end_index   = n_frames-half_scale
  
  middle_indices     = (start_index:end_index) + half_scale

  """
  #   our start_index frame can only have one valid frame (frame 1)
  #   afterwards it is invalid
  #
  #   To get around this we'll pad with bad values (which we'll never match)
  #   then shift the final indices
  #
  #   e.g.
  #   scale = 5
  #   start = 3 - this means we grab +/- 2, so we need to have our indices
  #       padded by 2 when we grab, or alternatively do a filter (i.e. if statement
  #   and removal of indices, which I think is slower)
  #
  #   NaN NaN 1 2 3
  #   1   2   3 4 5  <- temporary indices
  #
  #   Then at the end shift everything by 2 
  #
  #   This allows us to remove conditionals ...
  
  matched_left_mask  = false(1,length(middle_indices))
  matched_right_mask = false(1,length(middle_indices))
  
  #This tells us whether each value is useable or not for velocity
  #Better to do this out of the loop ...
  is_good_value_mask = [false(1,half_scale) ~isnan(x_mean) false(1,half_scale)]
  
  #These will be the final indices from which we estimate the velocity
  left_indices  = NaN(1,length(middle_indices))
  right_indices = NaN(1,length(middle_indices))
  
  #NOTE: This might be faster if we only tested unmatched values ...
  #NOTE: We could also switch the matched logic to avoid the negation ...
  for iShift = half_scale:scale_minus_1
      
      #We grab indices that are the appropriate distance from the current
      #value. If we have not yet found a bound on the given side, and the
      #index is valid, we keep it.
      left_indices_temp  = middle_indices - iShift
      right_indices_temp = middle_indices + iShift
      
      is_good_left       = is_good_value_mask(left_indices_temp)
      is_good_right      = is_good_value_mask(right_indices_temp)
      
      #Use if the value is good and not set ..
      use_left  = ~matched_left_mask  & is_good_left
      use_right = ~matched_right_mask & is_good_right
      
      left_indices(use_left)   = left_indices_temp(use_left)
      right_indices(use_right) = right_indices_temp(use_right)
      
      matched_left_mask(use_left)   = true
      matched_right_mask(use_right) = true
  end
  
  left_indices   = left_indices    - half_scale #Remove the offset ...
  right_indices  = right_indices   - half_scale
  middle_indices = middle_indices  - half_scale
  
  #Filter down to usable values
  #NOTE: Some values may not have valid points on one or both sides ...
  keep_mask = ~isnan(left_indices) & ~isnan(right_indices)
  
  left_indices   = left_indices(keep_mask)
  right_indices  = right_indices(keep_mask)
  middle_indices = middle_indices(keep_mask)
  
  #--------------------------------------------------------------------------
  
  d_x = x_mean(right_indices) - x_mean(left_indices)
  d_y = y_mean(right_indices) - y_mean(left_indices)
  distance = sqrt(d_x.^ 2 + d_y.^ 2)
  time     = (right_indices - left_indices)./ fps
  speed(middle_indices) = distance./time
  
  direction(middle_indices)   = pointAngle(right_indices) - pointAngle(left_indices)
  direction(direction < -180) = direction(direction < -180) + 360
  direction(direction > 180)  = direction(direction > 180)  - 360
  direction = direction./fps
  
  # Sign the speed.
  #--------------------------------------------------------
  motionDirection = atan2(d_y, d_x) * (180 / pi)
  bodyDirection(middle_indices) = motionDirection - bodyAngle(left_indices)
  
  bodyDirection(bodyDirection < -180) = bodyDirection(bodyDirection < -180) + 360
  bodyDirection(bodyDirection > 180)  = bodyDirection(bodyDirection > 180)  - 360
  
  speed(abs(bodyDirection) > 90) = -speed(abs(bodyDirection) > 90)
  
  # Sign the direction for dorsal/ventral locomtoion.
  if ventralMode < 2 % + = dorsal direction
      direction = -direction
  end
  """

  velocity = {'speed': speed, 'direction': direction}
  return velocity



def get_bends(nw):
  """
    INPUT: A NormalizedWorm object
    OUTPUT: A dictionary containing bends data
  
  """
  # We care only about the head, neck, midbody, hips and tail 
  # (i.e. the 'normal' way to partition the worm)
  p = nw.get_partition_subset('normal')
  
  bends = {}
  
  for partition_key in p.keys():
    # retrieve the part of the worm we are currently looking at:
    bend_angles = nw.get_partition(partition_key, 'angles')
    
    bend_metrics_dict = {}
    # shape = (n):
    bend_metrics_dict['mean'] = np.nanmean(a=bend_angles, axis = 0) 
    bend_metrics_dict['std_dev'] = np.nanstd(a=bend_angles, axis = 0)
    
    # Sign the standard deviation (to provide the bend's 
    # dorsal/ventral orientation):
    
    # First find all entries where the mean is negative
    mask = np.ma.masked_where(condition=bend_metrics_dict['mean'] < 0,
                              a=bend_metrics_dict['mean']).mask
    # Now create a numpy array of -1 where the mask is True and 1 otherwise
    sign_array = -np.ones(np.shape(mask)) * mask + \
                 np.ones(np.shape(mask)) * (~mask)
    # Finally, multiply the std_dev array by our sign_array
    bend_metrics_dict['std_dev'] = bend_metrics_dict['std_dev'] * sign_array
    
    bends[partition_key] = bend_metrics_dict
    
  # The final bends dictionary now contains a mean and standard 
  # deviation for the head, neck, midbody, hips and tail.
  return bends


def get_amplitude_and_wavelength(theta_d, sx, sy, worm_lengths):
  """
  
  
     Inputs
     =======================================================================
     theta_d      : worm orientation based on fitting to an ellipse, in
                     degrees
     sx           : [49 x n_frames]
     sy           : [49 x n_frames]
     worm_lengths : [1 x n_frames], total length of each worm
  
  
     Output: A dictionary with three elements:
     =======================================================================
     amplitude    :
         .max       - [1 x n_frames] max y deviation after rotating major axis to x-axis
         .ratio     - [1 x n_frames] ratio of y-deviations (+y and -y) with worm centered
                      on the y-axis, ratio is computed to be less than 1
     wavelength   :
         .primary   - [1 x n_frames]
         .secondary - [1 x n_frames] this might not always be valid, even 
                       when the primary wavelength is defined
     track_length  : [1 x n_frames]
  
     
     Old Name: getAmpWavelength.m
     TODO: This function was missing from some of the original code
     distributions. I need to make sure I upload it.
  
  
     Nature Methods Description
     =======================================================================
     Amplitude. 
     ------------------
     Worm amplitude is expressed in two forms: a) the maximum
     amplitude found along the worm body and, b) the ratio of the maximum
     amplitudes found on opposing sides of the worm body (wherein the smaller of
     these two amplitudes is used as the numerator). The formula and code originate
     from the publication “An automated system for measuring parameters of
     nematode sinusoidal movement”6.
     The worm skeleton is rotated to the horizontal axis using the orientation of the
     equivalent ellipse and the skeleton’s centroid is positioned at the origin. The
     maximum amplitude is defined as the maximum y coordinate minus the minimum
     y coordinate. The amplitude ratio is defined as the maximum positive y coordinate
     divided by the absolute value of the minimum negative y coordinate. If the
     amplitude ratio is greater than 1, we use its reciprocal.
  
     Wavelength
     ------------------------
     Wavelength. The worm’s primary and secondary wavelength are computed by
     treating the worm’s skeleton as a periodic signal. The formula and code
     originate from the publication “An automated system for measuring
     parameters of nematode sinusoidal movement”6. The worm’s skeleton is
     rotated as described above for the amplitude. If there are any
     overlapping skeleton points (the skeleton’s x coordinates are not
     monotonically increasing or decreasing in sequence -- e.g., the worm is
     in an S shape) then the shape is rejected, otherwise the Fourier
     transform computed. The primary wavelength is the wavelength associated
     with the largest peak in the transformed data. The secondary wavelength
     is computed as the wavelength associated with the second largest
     amplitude (as long as it exceeds half the amplitude of the primary
     wavelength). The wavelength is capped at twice the value of the worm’s
     length. In other words, a worm can never achieve a wavelength more than
     double its size.
  
     Tracklength
     -----------------------------
     Track Length. The worm’s track length is the range of the skeleton’s
     horizontal projection (as opposed to the skeleton’s arc length) after
     rotating the worm to align it with the horizontal axis. The formula and
     code originate from the publication “An automated system for measuring
     parameters of nematode sinusoidal movement”.
  
  
     Code based on:
     ------------------------------------------------
     BMC Genetics, 2005
     C.J. Cronin, J.E. Mendel, S. Mukhtar, Young-Mee Kim, R.C. Stirb, J. Bruck,
     P.W. Sternberg
     "An automated system for measuring parameters of nematode
     sinusoidal movement" BMC Genetics 2005, 6:5
  
  """
  amp_wave_track = \
    collections.namedtuple('amp_wave_track', 
                           ['amplitude', 'wavelength', 'track_length'])
  amp_wave_track.amplitude = 'yay1'
  amp_wave_track.wavelength = 'yay2'
  amp_wave_track.track_length = 'yay3'

  onw = nw.re_orient_and_centre()  


  return amp_wave_track


def get_eccentricity_and_orientation(contour_x, contour_y):
  """
  % get_eccentricity   
  %
  %   [eccentricity, orientation] = seg_worm.feature_helpers.posture.getEccentricity(xOutline, yOutline, gridSize)
  %
  %   Given x and y coordinates of the outline of a region of interest, fill
  %   the outline with a grid of evenly spaced points and use these points in
  %   a center of mass calculation to calculate the eccentricity and
  %   orientation of the equivalent ellipse.
  %
  %   Placing points in the contour is a well known computer science problem
  %   known as the Point-in-Polygon problem.
  %
  %   http://en.wikipedia.org/wiki/Point_in_polygon
  %
  %   This function became a lot more complicated in an attempt to make it 
  %   go much faster. The complication comes from the simplication that can
  %   be made when the worm doesn't bend back on itself at all.
  %
  %
  %   OldName: getEccentricity.m
  %
  %
  %   Inputs:
  %   =======================================================================
  %   xOutline : [96 x n_frames] The x coordinates of the contour. In particular the contour
  %               starts at the head and goes to the tail and then back to
  %               the head (although no points are redundant)
  %   yOutline : [96 x n_frames]  The y coordinates of the contour "  "
  %   
  %   N_ECCENTRICITY (a constant from config.py):
  %              (scalar) The # of points to place in the long dimension. More points
  %              gives a more accurate estimate of the ellipse but increases
  %              the calculation time.
  %
  %   Outputs: a namedtuple containing:
  %   =======================================================================
  %   eccentricity - [1 x n_frames] The eccentricity of the equivalent ellipse
  %   orientation  - [1 x n_frames] The orientation angle of the equivalent ellipse
  %
  %   Nature Methods Description
  %   =======================================================================
  %   Eccentricity. 
  %   ------------------
  %   The eccentricity of the worm’s posture is measured using
  %   the eccentricity of an equivalent ellipse to the worm’s filled contour.
  %   The orientation of the major axis for the equivalent ellipse is used in
  %   computing the amplitude, wavelength, and track length (described
  %   below).
  %
  %   Status
  %   =======================================================================
  %   The code below is finished although I want to break it up into smaller
  %   functions. I also need to submit a bug report for the inpoly FEX code.

  Translation of: SegwormMatlabClasses / 
  +seg_worm / +feature_helpers / +posture / getEccentricity.m
  """
  # TODO: translate this function from Jim's code
  EccentricityAndOrientation = \
    collections.namedtuple('EccentricityAndOrientation', 
                           ['eccentricity', 'orientation'])
                           
  EccentricityAndOrientation.eccentricity = 'eccentricity example'
  EccentricityAndOrientation.wavelength = 'wavelength example'

  return EccentricityAndOrientation
  
  
  
  
  
  
  
