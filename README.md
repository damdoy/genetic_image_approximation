# genetic_image_approximation

Approximate images using basic shapes such as circles using genetic algorithms

The algorithm creates a population of images containing circles of various colours
and are compared to the reference images, the closest images to the reference (that is less different) will
be selected to be duplicated with a small "mutation", gaussian change of their parameters.

As such, the images will slowly get closer to the reference image

## How to run

`python3 genetic_images.py <filename>`

## Examples:

![original](examples/matterhorn2_small.png) ![circles](examples/matterhorn2_small_circles.png) ![tris](examples/matterhorn2_small_tris.png) ![squares](examples/matterhorn2_small_squares.png)

![original](examples/bird_small.png) ![circles](examples/bird_small_circles.png) ![tris](examples/bird_small_tris.png) ![squares](examples/bird_small_squares.png)
