# genetic_image_approximation

Approximate images using basic shapes such as circles using genetic algorithms

The algorithm creates a population of images containing circles of various colours
and are compared to the reference images, the closest images to the reference (that is less different) will
be selected to be duplicated with a small "mutation", gaussian change of their parameters.

As such, the images will slowly get closer to the reference image

## Examples:

![origina](examples/matterhorn2_small.png) ![circles](examples/matterhorn2_small_circles.png) ![tris](examples/matterhorn2_small_tris.png)
