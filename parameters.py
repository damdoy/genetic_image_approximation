max_circle_radius = 150
mutation_rate = 1
prob_add_del_element = 0.15 #prob of an add or removal of circle vs circle mutation
prob_add_vs_del = 0.8 #chances to add a circle vs removing it
prob_exchange_elements = 0.1 #prob to exchange position of two circles (doesnt seem that useful)
all_col = 0 #update all colours

pop_size = 10 #initial pop size
nb_elements_max = 96
nb_elements_initial = 0 # how many shapes in the first populations
nb_elite = 5 # real pop will be 2*nb_elite
element_transparency = -0.5 #<0 means use the circles transparency
black_and_white = 0 #not used for now
backgroud_colour = (0xff, 0xff, 0xff) #(R, G, B) white
# backgroud_colour = (0x7f, 0x7f, 0x7f) #(R, G, B) gray
# backgroud_colour = (0xff, 0x00, 0x00) #(R, G, B) red
gaussian_blur_reference_image_sigma = 0.5 # sigma 0 = no gaussian blur
new_shape_size_divisor = 4.0 #how much smaller should new shapes be

max_threads = 1 #select the max numbers of threads that will be used

## shape selection
SHAPE_TYPE_CIRCLE = 0
SHAPE_TYPE_TRIANGLE = 1
SHAPE_TYPE_SQUARE = 2
shape_type = SHAPE_TYPE_CIRCLE

save_directory = "img/" #where the images for the iterations will be saved
