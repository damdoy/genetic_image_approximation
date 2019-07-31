import numpy as np
import random
import copy
import math
from parameters import *

def clamp(val, a, b):
   if(val < a):
      return a
   if(val > b):
      return b
   return val

class Shape:
   def __init__():
      pass

   def get_colour():
      pass

   def mutate(self):
      pass

class Circle(Shape):
   def __init__(self, centre_x, centre_y, radius, colour_r, colour_g, colour_b, max_size_x, max_size_y, alpha):
      self.centre = [centre_x, centre_y]
      self.radius = radius
      self.colour = [colour_r, colour_g, colour_b]
      self.alpha = np.clip(alpha, 10, 245)
      self.max_size = [max_size_x, max_size_y]

   def get_colour(self):
      return self.colour[0]+(self.colour[1]<<8)+(self.colour[2]<<16)

   def mutate(self):
      #apply gaussian random mutation
      self.centre[0] = clamp(int( self.centre[0] + (random.gauss(0,1)*10)*mutation_rate ), 0, self.max_size[0])
      self.centre[1] = clamp(int( self.centre[1] + (random.gauss(0,1)*10)*mutation_rate ), 0, self.max_size[1])
      self.radius = clamp(int( self.radius + (random.gauss(0,1)*10)*mutation_rate ), 1, max_circle_radius)

      col_to_update = int(random.random()*4) #only update one of the colours

      if(col_to_update == 0  or all_col):
         self.colour[0] = clamp( int ( self.colour[0] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 1  or all_col):
         self.colour[1] = clamp( int ( self.colour[1] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 2  or all_col):
         self.colour[2] = clamp( int ( self.colour[2] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 3  or all_col): # alpha
         self.alpha = clamp( int ( self.alpha + random.gauss(0,1)*10*mutation_rate ), 10, 245)

class Circle_B_W(Circle):
   def __init__(self, centre_x, centre_y, radius, colour_r, colour_g, colour_b, max_size_x, max_size_y, alpha):
      Circle.__init__(self, centre_x, centre_y, radius, colour_r, colour_r, colour_r, max_size_x, max_size_y, alpha)

   def mutate(self):
      #apply gaussian random mutation
      self.centre[0] = clamp(int( self.centre[0] + (random.gauss(0,1)*15)*mutation_rate ), 0, self.max_size[0])
      self.centre[1] = clamp(int( self.centre[1] + (random.gauss(0,1)*15)*mutation_rate ), 0, self.max_size[1])
      self.radius = clamp(int( self.radius + (random.gauss(0,1)*10)*mutation_rate ), 1, max_circle_radius)

      col_to_update = int(random.random()*2) #either colour or alpha

      if(col_to_update == 0  or all_col):
         colour = clamp( int ( self.colour[0] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
         self.colour[0] = self.colour[1] = self.colour[2] = colour
      if(col_to_update == 1  or all_col): # alpha
         self.alpha = clamp( int ( self.alpha + random.gauss(0,1)*10*mutation_rate ), 10, 245)

#triangle
class Tri(Shape):
   def __init__(self, points, colour_r, colour_g, colour_b, max_size_x, max_size_y, alpha):
      self.points = points # [[pt0_x, pt0_y], [pt1_x, pt1_y], [pt2_x, pt2_y]]
      self.colour = [colour_r, colour_g, colour_b]
      self.alpha = np.clip(alpha, 10, 245)
      self.max_size = [max_size_x, max_size_y]

   def get_colour(self):
      return self.colour[0]+(self.colour[1]<<8)+(self.colour[2]<<16)

   def mutate(self):
      #apply gaussian random mutation
      for i in range(3):
         for j in range(2):
            self.points[i][j] = clamp(int( self.points[i][j] + (random.gauss(0,1)*10)*mutation_rate ), 0, self.max_size[j])

      col_to_update = int(random.random()*4) #only update one of the colours

      if(col_to_update == 0  or all_col):
         self.colour[0] = clamp( int ( self.colour[0] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 1  or all_col):
         self.colour[1] = clamp( int ( self.colour[1] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 2  or all_col):
         self.colour[2] = clamp( int ( self.colour[2] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 3  or all_col): # alpha
         self.alpha = clamp( int ( self.alpha + random.gauss(0,1)*10*mutation_rate ), 10, 245)

class Square(Shape):
   def __init__(self, pt_top_left, side_size, colour_r, colour_g, colour_b, max_size_x, max_size_y, alpha):
      self.point = pt_top_left
      self.side_size = side_size
      self.colour = [colour_r, colour_g, colour_b]
      self.alpha = np.clip(alpha, 10, 245)
      self.max_size = [max_size_x, max_size_y]

   def get_colour(self):
      return self.colour[0]+(self.colour[1]<<8)+(self.colour[2]<<16)

   def mutate(self):
      #apply gaussian random mutation
      self.point[0] = clamp( int ( self.point[0] + random.gauss(0,1)*10*mutation_rate ), 0, self.max_size[0]-1)
      self.point[1] = clamp( int ( self.point[1] + random.gauss(0,1)*10*mutation_rate ), 0, self.max_size[1]-1)
      self.side_size = int ( self.side_size + random.gauss(0,1)*10*mutation_rate )

      if self.side_size < 1:
         self.side_size = 1
      else:
         if self.point[0]+self.side_size > self.max_size[0]:
            self.side_size = self.max_size[0]-self.point[0]
         if self.point[1]+self.side_size > self.max_size[1]:
            self.side_size = self.max_size[1]-self.point[1]

      col_to_update = int(random.random()*4) #only update one of the colours

      if(col_to_update == 0  or all_col):
         self.colour[0] = clamp( int ( self.colour[0] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 1  or all_col):
         self.colour[1] = clamp( int ( self.colour[1] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 2  or all_col):
         self.colour[2] = clamp( int ( self.colour[2] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
      if(col_to_update == 3  or all_col): # alpha
         self.alpha = clamp( int ( self.alpha + random.gauss(0,1)*10*mutation_rate ), 10, 245)

class Point(Shape):
   def __init__(self, x, y, colour_r, colour_g, colour_b, max_size_x, max_size_y):
      self.x = x
      self.y = y
      self.colour = [colour_r, colour_g, colour_b]
      self.max_size = [max_size_x, max_size_y]

   def mutate(self):
      mutation_pos = random.random()

      if(mutation_pos < 0.2): #TODO parameter
         #apply gaussian random mutation
         self.x = clamp( int ( self.x + random.gauss(0,1)*5*mutation_rate ), 0, self.max_size[0]-1)
         self.y = clamp( int ( self.y + random.gauss(0,1)*5*mutation_rate ), 0, self.max_size[1]-1)

      elif mutation_pos >= 0.2:
         col_to_update = int(random.random()*3) #only update one of the colours

         if(col_to_update == 0  or all_col):
            self.colour[0] = clamp( int ( self.colour[0] + random.gauss(0,1)*20*mutation_rate ), 0, 255)
         if(col_to_update == 1  or all_col):
            self.colour[1] = clamp( int ( self.colour[1] + random.gauss(0,1)*20*mutation_rate ), 0, 255)
         if(col_to_update == 2  or all_col):
            self.colour[2] = clamp( int ( self.colour[2] + random.gauss(0,1)*20*mutation_rate ), 0, 255)

class ShapeImage(object):
   def __init__(self, size_x, size_y, fixed_transparency):
      self.size = (size_x, size_y)
      self.lst_elements = []
      self.fitness = -1
      self.fixed_transparency = fixed_transparency #-1 means no fixed transparency (use shape alpha), otherwise values from 0 to 1

   #create a duplicate of this image with mutation (slight changes)
   def copy_mutate(self):
      si = self.__class__(self.size[0], self.size[1], element_transparency)

      operation = random.random() #remove/add shape or mutate?

      si.lst_elements = copy.deepcopy(self.lst_elements) #create the copy

      if(operation < prob_add_del_element): # add or remove a shape from copy
         if(random.random() < prob_add_vs_del and len(si.lst_elements) < nb_elements_max): # add shape
            si.add_random_element()

         elif(len(si.lst_elements) > 0): #remove shape
            idx_to_remove = int(random.random()*len(si.lst_elements))
            del si.lst_elements[idx_to_remove]

      #exchange position of two element in the copy
      elif operation >= prob_add_del_element and operation <= prob_add_del_element+prob_exchange_elements and len(si.lst_elements) >= 2:
         idx_element_ex = random.randint(0, len(si.lst_elements)-2) #chose index from 0 to len-2 so that it can be swapped with len-1 element

         elem = si.lst_elements[idx_element_ex]
         si.lst_elements[idx_element_ex] = si.lst_elements[idx_element_ex+1]
         si.lst_elements[idx_element_ex+1] = elem

      elif len(si.lst_elements) > 0:
         #chose a single circle to mutate
         idx_elem_to_mutate = random.randint(0, len(si.lst_elements)-1)
         si.lst_elements[idx_elem_to_mutate].mutate()
      return si

   def get_bitmap(self):
      ret_bmp_np = np.ones((self.size[0], self.size[1], 3))*backgroud_colour ##empty image of parameter background colour

      # for circ in reversed(self.lst_elements): #step the list backward. (draw last elements in the front)
      for elem in self.lst_elements: #step the list backward. (draw last elements in the front)

         mask = self.get_mask_matrix(elem)
         mask_rgb = np.repeat(mask[:,:,np.newaxis], 3, axis=2) #have a matrix of true values for the element

         #fill element colour in the matrix
         elem_value = np.where(mask_rgb == [True, True, True], [elem.colour[0], elem.colour[1], elem.colour[2]], [0,0,0])
         mask_bg_shape = np.multiply(mask_rgb, ret_bmp_np)
         mask_bg = np.multiply(~mask_rgb, ret_bmp_np) #false value will have the background colour
         # mask_bg_shape = mask_bg+elem_value #add both element and the background

         if self.fixed_transparency >= 0 and self.fixed_transparency <= 1:
            elem_value = np.clip((1.0-self.fixed_transparency)*elem_value+self.fixed_transparency*mask_bg_shape, 0, 255)
         else: #use transparency of the element
            elem_value = np.clip((elem.alpha/255.0)*elem_value+(1.0-(elem.alpha/255.0))*mask_bg_shape, 0, 255)

            ret_bmp_np = elem_value + mask_bg

      return ret_bmp_np


class ShapeImage_Circle(ShapeImage):

   def get_mask_matrix(self, circ):
      #get coords for the circle
      y,x = np.ogrid[-circ.centre[0]:self.size[0]-circ.centre[0], -circ.centre[1]:self.size[1]-circ.centre[1]]

      mask = x*x + y*y <= circ.radius*circ.radius
      return mask

   def add_random_element(self):
      self.lst_elements.append(Circle(int(self.size[0]*random.random()), int(self.size[1]*random.random()), int(max_circle_radius/new_shape_size_divisor*random.random()), int(0xff*random.random()), int(0xff*random.random()), int(0xff*random.random()), self.size[0], self.size[1], int(0xff*random.random())))

   #reproduce two images to have a offpring which is combination of the two images + a random
   # should be images with same amount of circles
   def reproduce_images(self, img2):
      si = ShapeImage(self.size[0], self.size[1], element_transparency)
      mutated = 1
      all_col = 1 #update all colours
      for c1, c2 in zip(self.lst_elements, img2.lst_elements):
         if random.random() > prob_circ_mutation:
            mutated = 0
         else:
            mutated = 1

         interp = random.random()
         new_circle_pos_x = clamp(int( ((1.0-interp)*c1.centre[0]+(interp)*c2.centre[0]) + (random.random()*30-15)*mutation_rate*mutated ), 0, self.size[0])
         new_circle_pos_y = clamp(int( ((1.0-interp)*c1.centre[1]+(interp)*c2.centre[1]) + (random.random()*30-15)*mutation_rate*mutated ), 0, self.size[1])
         new_circle_radius = clamp(int( ((1.0-interp)*c1.radius+(interp)*c2.radius) + (random.random()*20-10)*mutation_rate*mutated ), 1, max_circle_radius)

         col_to_update = int(random.random()*3) #only update one of the colours

         new_circle_colr = int ( (c1.colour[0]+c2.colour[0])/2)
         new_circle_colg = int ( (c1.colour[1]+c2.colour[1])/2)
         new_circle_colb = int ( (c1.colour[2]+c2.colour[2])/2)

         if(col_to_update == 0  or all_col):
            new_circle_colr = clamp( int ( new_circle_colr + (random.random()*40-20)*mutation_rate*mutated ), 0, 255)
         if(col_to_update == 1  or all_col):
            new_circle_colg = clamp( int ( new_circle_colg + (random.random()*40-20)*mutation_rate*mutated ), 0, 255)
         if(col_to_update == 2  or all_col):
            new_circle_colb = clamp( int ( new_circle_colb + (random.random()*40-20)*mutation_rate*mutated ), 0, 255)

         si.lst_elements.append(Circle(new_circle_pos_x, new_circle_pos_y, new_circle_radius, new_circle_colr, new_circle_colg, new_circle_colb, self.size[0], self.size[1]))
      return si

class ShapeImage_Tri(ShapeImage):

   #barycentric coord, from https://stackoverflow.com/questions/13300904/determine-whether-point-lies-inside-triangle
   def is_pt_in_tri(self, pt, pts_tri):
      alpha = ((pts_tri[1][1] - pts_tri[2][1])*(pt[0] - pts_tri[2][0]) + (pts_tri[2][0] - pts_tri[1][0])*(pt[1] - pts_tri[2][1])) / ((pts_tri[1][1] - pts_tri[2][1])*(pts_tri[0][0] - pts_tri[2][0]) + (pts_tri[2][0] - pts_tri[1][0])*(pts_tri[0][1] - pts_tri[2][1]));
      beta = ((pts_tri[2][1] - pts_tri[0][1])*(pt[0] - pts_tri[2][0]) + (pts_tri[0][0] - pts_tri[2][0])*(pt[1] - pts_tri[2][1])) / ((pts_tri[1][1] - pts_tri[2][1])*(pts_tri[0][0] - pts_tri[2][0]) + (pts_tri[2][0] - pts_tri[1][0])*(pts_tri[0][1] - pts_tri[2][1]));
      gamma = 1.0 - alpha - beta;

      return (alpha > 0) and (beta > 0) and (gamma > 0)

   def get_mask_matrix(self, tri):
      #get coords for the circle
      x,y = np.ogrid[0:self.size[0], 0:self.size[1]]

      # mask = self.is_pt_in_tri([x,y], tri.points)
      alpha = (((tri.points[1][1] - tri.points[2][1])*(x - tri.points[2][0]) + (tri.points[2][0] - tri.points[1][0])*(y - tri.points[2][1])) / ((tri.points[1][1] - tri.points[2][1])*(tri.points[0][0] - tri.points[2][0]) + (tri.points[2][0] - tri.points[1][0])*(tri.points[0][1] - tri.points[2][1])))
      beta = (((tri.points[2][1] - tri.points[0][1])*(x - tri.points[2][0]) + (tri.points[0][0] - tri.points[2][0])*(y - tri.points[2][1])) / ((tri.points[1][1] - tri.points[2][1])*(tri.points[0][0] - tri.points[2][0]) + (tri.points[2][0] - tri.points[1][0])*(tri.points[0][1] - tri.points[2][1])))
      gamma = (-alpha)-beta+1.0
      mask = (alpha>=0)*(beta>=0)*(gamma>=0)
      return mask

   def add_random_element(self):

      lst_points = []

      for i in range(3):
         lst_points.append([])
         for j in range(2):
            lst_points[i].append(int(self.size[j]*random.random()))

      self.lst_elements.append(Tri(lst_points, int(0xff*random.random()), int(0xff*random.random()), int(0xff*random.random()), self.size[0], self.size[1], int(0xff*random.random())))

   #reproduce two images to have a offpring which is combination of the two images + a random
   # should be images with same amount of circles
   #TODO
   def reproduce_images(self, img2):
      pass

class ShapeImage_Square(ShapeImage):

   def get_mask_matrix(self, square):
      #get coords for the circle
      x,y = np.ogrid[0:self.size[0], 0:self.size[1]]

      #needs a numpy logical and to create a mask
      mask = np.logical_and(np.logical_and(x >= square.point[0], x <= square.point[0]+square.side_size), np.logical_and(y >= square.point[1], y <= square.point[1]+square.side_size))
      return mask

   def add_random_element(self):

      top_left_pt = [0, 0]
      top_left_pt[0] = (int(self.size[0]*random.random()))
      top_left_pt[1] = (int(self.size[1]*random.random()))
      size = int(min(self.size[0], self.size[1])*random.random())

      if top_left_pt[0]+size > self.size[0]:
         size = self.size[0]-top_left_pt[0]
      if top_left_pt[1]+size > self.size[1]:
         size = self.size[1]-top_left_pt[1]

      self.lst_elements.append(Square(top_left_pt, size, int(0xff*random.random()), int(0xff*random.random()), int(0xff*random.random()), self.size[0], self.size[1], int(0xff*random.random())))

   #reproduce two images to have a offpring which is combination of the two images + a random
   # should be images with same amount of circles
   #TODO
   def reproduce_images(self, img2):
      pass

class ShapeImage_Voronoi(ShapeImage):

   def get_bitmap(self):
      ret_bmp_np = np.ones((self.size[0], self.size[1], 3))*backgroud_colour ##empty image of parameter background colour

      #needs a numpy logical and to create a mask
      # mask = np.logical_and(np.logical_and(x >= square.point[0], x <= square.point[0]+square.side_size), np.logical_and(y >= square.point[1], y <= square.point[1]+square.side_size))
      dist_list = []

      dist_min = np.ones((self.size[0], self.size[1]))*100000000000000

      for elem in self.lst_elements:
         x,y = np.ogrid[0:self.size[0], 0:self.size[1]]

         dist = np.sqrt(np.power(x-elem.x, 2)+np.power(y-elem.y, 2))
         dist_list.append( dist )

         mask = dist < dist_min
         mask_rgb = np.repeat(mask[:,:,np.newaxis], 3, axis=2) #have a matrix of true values for the element
         elem_value = np.where(mask_rgb == [True, True, True], [elem.colour[0], elem.colour[1], elem.colour[2]], [0,0,0])
         mask_bg = np.multiply(~mask_rgb, ret_bmp_np) #false value will have the background colour
         ret_bmp_np = mask_bg + elem_value

         dist_min = np.minimum(dist_min, dist)

      return ret_bmp_np

   def add_random_element(self):

      pt_x = (int(self.size[0]*random.random()))
      pt_y = (int(self.size[1]*random.random()))

      self.lst_elements.append(Point(pt_x, pt_y, int(0xff*random.random()), int(0xff*random.random()), int(0xff*random.random()), self.size[0], self.size[1] ))

   #reproduce two images to have a offpring which is combination of the two images + a random
   # should be images with same amount of circles
   #TODO
   def reproduce_images(self, img2):
      pass
