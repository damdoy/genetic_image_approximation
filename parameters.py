max_circle_size = 150
mutation_rate = 1
# prob_circ_mutation = 0.25
prob_add_del_element = 0.15 #prob of an add or removal of circle vs circle mutation
prob_add_vs_del = 0.8 #chances to add a circle vs removing it
prob_exchange_elements = 0.1 #prob to exchange position of two circles (doesnt seem that useful)
mix_mode = 0# combines colours of different circles

pop_size = 10 #initial pop size
nb_circles_max = 96
nb_circles_initial = 0
nb_elite = 3 # real pop will be nb_elite*nb_elite
circle_transparency = -0.5 #<0 means use the circles transparency
black_and_white = 0 #not used for now
backgroud_colour = (0xff, 0xff, 0xff)
# backgroud_colour = (0x7f, 0x7f, 0x7f) #(R, G, B)
# backgroud_colour = (0xff, 0x00, 0x00) #(R, G, B)
gaussian_blur_reference_image_sigma = 0.5 # sigma 0 = no gaussian blur
new_shape_size_divisor = 4.0 #how much smaller should new shapes be

SHAPE_TYPE_CIRCLE = 0
SHAPE_TYPE_TRIANGLE = 1
SHAPE_TYPE_SQUARE = 2
shape_type = SHAPE_TYPE_TRIANGLE

all_col = 0 #update all colours
