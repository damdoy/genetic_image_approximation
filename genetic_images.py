from tkinter import *
from shapeImage import *
import math
import random
from PIL import Image
import numpy as np
import cProfile
import copy
from parameters import *
from skimage.filter import gaussian_filter
import threading
from concurrent.futures import ThreadPoolExecutor

master = Tk()

def compare_bitmaps(bitmap1, bitmap2, size_x, size_y):
   return ((bitmap1-bitmap2)**2).mean(axis=None)

def compare_pop_bitmap(bitmap1, pop, size_x, size_y):
   bitmap_pop = pop.get_bitmap()
   fitness = compare_bitmaps(bitmap1, bitmap_pop, size_x, size_y)
   pop.fitness = fitness

def read_img(filename):
   img = Image.open(filename)
   ary = np.array(img)
   print(ary[125][125])
   ret = []

   for x in range(0, len(ary[0])):
      ret.append([])
      for y in range(0, len(ary)):
         val = ary[y][x]
         ret[x].append([val[0],val[1],val[2]])
   return ret

#create a population of shapeimage with random parameters
def create_population(pop_size, elem_size, img_size_x, img_size_y):
   pop = []
   for i in range(0, pop_size):
      if shape_type == SHAPE_TYPE_CIRCLE:
         si = ShapeImage_Circle(img_size_x, img_size_y, element_transparency)
      elif shape_type == SHAPE_TYPE_TRIANGLE:
         si = ShapeImage_Tri(img_size_x, img_size_y, element_transparency)
      elif shape_type == SHAPE_TYPE_SQUARE:
         si = ShapeImage_Square(img_size_x, img_size_y, element_transparency)
      for j in range(0, elem_size):
         si.add_random_element()
      pop.append(si)
   return pop

#keep value between threshold
def clamp(val, a, b):
   if(val < a):
      return a
   if(val > b):
      return b
   return val

#iteration for the reproduction model
def genetic_iteration_reproduce(pop, nb_elite, bitmap_reference):
   pop_size = len(pop)
   fit_results = get_fitness(pop, bitmap_reference)

   new_pop = []

   for i in range(0, nb_elite):
      new_pop.append(pop[fit_results[i][0]])

   for i in range(0, nb_elite):
      for j in range(0, nb_elite):
         if i != j and len(new_pop) < pop_size:
            new_img = new_pop[i].reproduce_images(new_pop[j])
            new_pop.append(new_img)

   return new_pop

#for the copy and mutate model
def genetic_iteration_copy_mutate(pop, nb_elite, bitmap_reference, fit_results):
   pop_size = len(pop)
   # fit_results = get_fitness(pop, bitmap_reference)

   new_pop = []

   # copy best in new pop
   for i in range(0, nb_elite):
      new_pop.append(pop[fit_results[i][0]])

   for i in range(0, nb_elite):
      new_img = new_pop[i].copy_mutate()
      new_pop.append(new_img)

   return new_pop

#returns sorted list of fitness for all pop
def get_fitness(pop, bitmap_reference):
   pop_size = len(pop)
   fit_results = []

   executor = ThreadPoolExecutor(max_threads)
   futures = []
   for i in range(0, pop_size):
      if pop[i].fitness < 0: #if fitness already calculated, ignore
         futures.append( executor.submit(compare_pop_bitmap, bitmap_reference, pop[i], len(bitmap_reference), len(bitmap_reference[0]) ) ) #sends calculation to the thread pool

   for i in range(0, len(futures)):
      futures[i].result()

   for i in range(0, pop_size):
      fit_results.append((i, pop[i].fitness))

   def sortSecond(v):
      return v[1]

   fit_results.sort(key = sortSecond)

   return fit_results

#returns sorted list of fitness for all pop
def get_fitness_no_threads(pop, bitmap_reference):
   pop_size = len(pop)
   fit_results = []

   for i in range(0, pop_size):
      if pop[i].fitness < 0: #if fitness already calculated, ignore
         compare_pop_bitmap(bitmap_reference, pop[i], len(bitmap_reference), len(bitmap_reference[0]))

   for i in range(0, pop_size):
      fit_results.append((i, pop[i].fitness))

   def sortSecond(v):
      return v[1]

   fit_results.sort(key = sortSecond)

   return fit_results

#draw it on the gui
def draw(canvas_width, canvas_height, bitmap):
   for x in range(canvas_width):
      for y in range(canvas_height):
         val = (bitmap[x][y][0]<<16)+(bitmap[x][y][1]<<8)+bitmap[x][y][2] ##red was at position of blue
         img.put('#{0:0{1}X}'.format(val,6), (x, y))

#save the bitmap in a file
def save(bitmap, filename):
   ar = np.zeros(shape=(len(bitmap[0]), len(bitmap), 3))

   for i in range(0, len(bitmap[0])):
      for j in range(0, len(bitmap)):
         for k in range(0, 3):
            ar[i][j][k] = bitmap[j][i][k] #rotation

   im = Image.fromarray(ar.astype(np.uint8))
   im.save(filename)

if len(sys.argv) != 2:
   print("should have two parameters")
   exit()

str_image_ref = sys.argv[1]

print("selected image: " + str_image_ref)

bitmap_reference = read_img(str_image_ref)

bitmap_reference = np.array(bitmap_reference) #transform bitmap to numpy array

canvas_width = len(bitmap_reference)
canvas_height = len(bitmap_reference[0])

#apply gaussian blur (helps approx)
bitmap_reference = bitmap_reference.astype(float)
bitmap_reference = gaussian_filter(bitmap_reference, sigma=gaussian_blur_reference_image_sigma, multichannel=True)
bitmap_reference = bitmap_reference.astype(int)

#gui for display
w = Canvas(master, width=canvas_width, height=canvas_height)
w.pack()
img = PhotoImage(width=canvas_width, height=canvas_height)
w.create_image((canvas_width/2, canvas_height/2), image=img, state="normal")

initial_pop = create_population(pop_size, nb_elements_initial, canvas_width, canvas_height)

fit_results = get_fitness(initial_pop, bitmap_reference)

print(fit_results)

bitmap = initial_pop[fit_results[0][0]].get_bitmap()

pop = initial_pop

fit_results = get_fitness(pop, bitmap_reference)
last_best = 100000000000000 #safe assumption

for i in range(0, 30000):
   # pop = genetic_iteration_reproduce(pop, nb_elite, bitmap_reference)
   pop = genetic_iteration_copy_mutate(pop, nb_elite, bitmap_reference, fit_results)
   fit_results = get_fitness(pop, bitmap_reference)
   print("iteration: "+str(i))
   print("nb_circ: "+str(len(pop[fit_results[0][0]].lst_elements)))
   print(fit_results)
   if(last_best > fit_results[0][1] and i%10 == 0):
      last_best = fit_results[0][1]
      save(pop[fit_results[0][0]].get_bitmap(), "img/iteration"+str(i)+".png")

   if i%10 == 0: #draw every 10 iteration
      # save(pop[fit_results[0][0]].get_bitmap(), "img/iteration"+str(i)+".png")
      pass

bitmap = pop[fit_results[0][0]].get_bitmap()

draw(canvas_width, canvas_height, bitmap)

#mainloop for gui display
mainloop()
