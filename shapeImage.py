import numpy as np
import random
import copy
from parameters import *

def clamp(val, a, b):
   if(val < a):
      return a
   if(val > b):
      return b
   return val

class Circle:
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
      self.centre[0] = clamp(int( self.centre[0] + (random.gauss(0,1)*15)*mutation_rate ), 0, self.max_size[0])
      self.centre[1] = clamp(int( self.centre[1] + (random.gauss(0,1)*15)*mutation_rate ), 0, self.max_size[1])
      self.radius = clamp(int( self.radius + (random.gauss(0,1)*10)*mutation_rate ), 1, max_circle_size)

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
      self.radius = clamp(int( self.radius + (random.gauss(0,1)*10)*mutation_rate ), 1, max_circle_size)

      col_to_update = int(random.random()*2) #either colour or alpha

      if(col_to_update == 0  or all_col):
         colour = clamp( int ( self.colour[0] + random.gauss(0,1)*10*mutation_rate ), 0, 255)
         self.colour[0] = self.colour[1] = self.colour[2] = colour
      if(col_to_update == 1  or all_col): # alpha
         self.alpha = clamp( int ( self.alpha + random.gauss(0,1)*10*mutation_rate ), 10, 245)


class ShapeImage:

   def __init__(self, size_x, size_y, fixed_transparency):
      self.size = (size_x, size_y)
      self.lst_rects = []
      self.lst_circles = []
      self.fitness = -1
      self.fixed_transparency = fixed_transparency #-1 means no fixed transparency (use circle alpha), otherwise values from 0 to 1


   def get_bitmap(self):
      ret_bmp_np = np.ones((self.size[0], self.size[1], 3))*0xff ##array of white values (255, 255,255)

      # for circ in reversed(self.lst_circles): #step the list backward. (draw last elements in the front)
      for circ in self.lst_circles: #step the list backward. (draw last elements in the front)

         #get coords for the circle
         y,x = np.ogrid[-circ.centre[0]:self.size[0]-circ.centre[0], -circ.centre[1]:self.size[1]-circ.centre[1]]

         mask = x*x + y*y <= circ.radius*circ.radius
         mask_circle = np.repeat(mask[:,:,np.newaxis], 3, axis=2) #have a matrix of true values for the circle

         #fill circle colour in the matrix
         circle_value = np.where(mask_circle == [True, True, True], [circ.colour[0], circ.colour[1], circ.colour[2]], [0,0,0])
         mask_bg_circle = np.multiply(mask_circle, ret_bmp_np)
         mask_bg = np.multiply(~mask_circle, ret_bmp_np) #false value will have the background colour
         # mask_bg_and_circle = mask_bg+circle_value #add both circle and the background

         if self.fixed_transparency >= 0 and self.fixed_transparency <= 1:
            circle_value = np.clip((1.0-self.fixed_transparency)*circle_value+self.fixed_transparency*mask_bg_circle, 0, 255)
         else: #use transparency of the circle
            circle_value = np.clip((circ.alpha/255.0)*circle_value+(1.0-(circ.alpha/255.0))*mask_bg_circle, 0, 255)

            ret_bmp_np = circle_value + mask_bg

      return ret_bmp_np

   def add_random_element(self):

      self.lst_circles.append(Circle(int(self.size[0]*random.random()), int(self.size[1]*random.random()), int(max_circle_size/new_shape_size_divisor*random.random()), int(0xff*random.random()), int(0xff*random.random()), int(0xff*random.random()), self.size[0], self.size[1], int(0xff*random.random())))


   #create a duplicate of this image with mutation (slight changes)
   def copy_mutate(self):
      si = ShapeImage(self.size[0], self.size[1], circle_transparency)

      operation = random.random() #remove/add circle or mutate?

      si.lst_circles = copy.deepcopy(self.lst_circles) #create the copy

      if(operation < prob_add_del_circle): # add or remove a circle from copy
         if(random.random() < prob_add_vs_del and len(si.lst_circles) < nb_circles_max): # add circle
            si.add_random_element()

         elif(len(si.lst_circles) > 0): #remove circle
            idx_to_remove = int(random.random()*len(si.lst_circles))
            del si.lst_circles[idx_to_remove]

      #exchange position of two circle in the copy
      elif operation >= prob_add_del_circle and operation <= prob_add_del_circle+prob_exchange_circles and len(si.lst_circles) >= 2:
         idx_circle_ex = random.randint(0, len(si.lst_circles)-2) #chose index from 0 to len-2 so that it can be swapped with len-1 element

         circ = si.lst_circles[idx_circle_ex]
         si.lst_circles[idx_circle_ex] = si.lst_circles[idx_circle_ex+1]
         si.lst_circles[idx_circle_ex+1] = circ

      elif len(si.lst_circles) > 0:
         #chose a single circle to mutate
         idx_circle_to_mutate = random.randint(0, len(si.lst_circles)-1)
         si.lst_circles[idx_circle_to_mutate].mutate()
      return si

   #reproduce two images to have a offpring which is combination of the two images + a random
   # should be images with same amount of circles
   def reproduce_images(self, img2):
      si = ShapeImage(self.size[0], self.size[1], circle_transparency)
      mutated = 1
      all_col = 1 #update all colours
      for c1, c2 in zip(self.lst_circles, img2.lst_circles):
         if random.random() > prob_circ_mutation:
            mutated = 0
         else:
            mutated = 1

         interp = random.random()
         new_circle_pos_x = clamp(int( ((1.0-interp)*c1.centre[0]+(interp)*c2.centre[0]) + (random.random()*30-15)*mutation_rate*mutated ), 0, self.size[0])
         new_circle_pos_y = clamp(int( ((1.0-interp)*c1.centre[1]+(interp)*c2.centre[1]) + (random.random()*30-15)*mutation_rate*mutated ), 0, self.size[1])
         new_circle_radius = clamp(int( ((1.0-interp)*c1.radius+(interp)*c2.radius) + (random.random()*20-10)*mutation_rate*mutated ), 1, max_circle_size)
         # new_circle_radius = clamp(int( (c1.radius+c2.radius)/2 + (random.random()*30-15)*0*mutated ), 1, max_circle_size)

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

         si.lst_circles.append(Circle(new_circle_pos_x, new_circle_pos_y, new_circle_radius, new_circle_colr, new_circle_colg, new_circle_colb, self.size[0], self.size[1]))
      return si
