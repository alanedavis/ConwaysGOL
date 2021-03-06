#!/usr/bin/python
"""
 Author: James A. Shackleford
   Date: Oct. 16th, 2015

   A simple implementation of Conway's Game of Life
"""
import patterns_Alan_Davis_061
import sys
import argparse
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import time
parser = argparse.ArgumentParser()

def generate_world(opts):
    """
    Accepts: opts  -- parsed command line options
    Returns: world -- a list of lists that forms a 2D pixel buffer

    Description: This function generates a 2D pixel buffer with dimensions
                 opts.cols x opts.rows (in pixels).  The initial contents
                 of the generated world is determined by the value provided
                 by opts.world_type: either 'random' or 'empty'  A 'random'
                 world has 10% 'living' pixels and 90% 'dead' pixels.  An
                 'empty' world has 100% 'dead' pixels.
    """
    world = []

    ## TASK 1
    if opts.world_type == "empty":  # If the user argument is "empty", and does the following
        for x in range(opts.rows):  # For the entire length of the row
            mat = []  # Creates an empty matrix
            for y in range(opts.cols):  # For the entire length of the column
                mat.append(0)  # For all of the rows, and all of the columns, make the values "0"
            world.append(mat)  # The new matrix "mat" will replace "world"
        return world  # Returns world

    if opts.world_type == "random":  # If the user argument is "random", and does the following
        for x in range(opts.rows):  # For the entire length of the row
            mat = []  # Creates an empty matrix
            cutoff = opts.cols/10  # Cutoff will be equal to 10% of the amount of columns
            count = 0  # initializes the variable "0"
            for y in range(opts.cols):  # For the entire length of the column
                if count <= int(cutoff):  # This will continue to add "1" to the matrix until 10% of the matrix has ones
                    mat.append(1)  # Adds 1 to the matrix
                    count = count + 1  # Count iterates up by one
                else:
                    mat.append(0)  # Now that 10% of the matrix is "1" the rest of the matrix will be turned into "0"'s
            random.shuffle(mat)  # Shuffles the "1"'s that are on one side of the cell around the whole cell
            world.append(mat)  # The new matrix "mat" will replace "world"
        return world  # Returns world

def update_frame(frame_num, opts, world, img):
    """
    Accepts: frame_num  -- (automatically passed in) current frame number
             opts       -- a populated command line options instance
             world      -- the 2D world pixel buffer
             img        -- the plot image
    """

    # set the current plot image to display the current 2D world matrix
    img.set_array(world)

    # Create a *copy* of 'world' called 'new_world' -- 'new_world' will be
    # our offscreen drawing buffer.  We will draw the next frame to
    # 'new_world' so that we may maintain an in-tact copy of the current
    # 'world' at the same time.
    new_world = []
    for row in world:
        new_world.append(row[:])

    ## TASK 3
    map = range(len(new_world))
    for i in map:  # Iterates through the columns
        for j in map:  # Iterates through the rows
            sqr1 = world[(i-1) % opts.cols][(j-1) % opts.cols]  # Top left of the initial pixel
            sqr2 = world[(i-1) % opts.cols][j % opts.cols]  # Top middle of the initial pixel
            sqr3 = world[(i-1) % opts.cols][(j+1) % opts.cols]  # Top right of the initial pixel
            sqr4 = world[i % opts.cols][(j-1) % opts.cols]  # Left of the initial pixel
            sqr5 = world[i % opts.cols][(j+1) % opts.cols]  # Right of the initial pixel
            sqr6 = world[(i+1) % opts.cols][(j-1) % opts.cols]  # Bottom left of the initial pixel
            sqr7 = world[(i+1) % opts.cols][j % opts.cols]  # Bottom middle of the initial pixel
            sqr8 = world[(i+1) % opts.cols][(j+1) % opts.cols]  # Bottom right of the initial pixel
            square = (sqr1 + sqr2 + sqr3 + sqr4 + sqr5 + sqr6 + sqr7 + sqr8)

            if new_world[i][j] == 1:  # If the pixel is alive
                if (square < 2) or (square > 3):  # If the total amount of live pixels is less than 2 or bigger than 3
                    new_world[i][j] = 0  # Make the initial live pixel dead

            if new_world[i][j] == 0:  # If the pixel is dead
                if square == 3:  # If there are 3 alive pixels
                    new_world[i][j] = 1  # Make the initial dead pixel alive




    #  Copy the contents of the new_world into the world
    # (i.e. make the future the present)
    world[:] = new_world[:]
    return img,

def blit(world, sprite, x, y):
    """
    Accepts: world  -- a 2D world pixel buffer generated by generate_world()
             sprite -- a 2D matrix containing a pattern of 1s and 0s
             x      -- x world coord where left edge of sprite will be placed
             y      -- y world coord where top edge of sprite will be placed

    Returns: (Nothing)

    Description: Copies a 2D pixel pattern (i.e sprite) into the larger 2D
                 world.  The sprite will be copied into the 2D world with
                 its top left corner being located at world coordinate (x,y)
    """
    ## TASK 2
    for i in range(len(sprite)):  # This will iterate through the amount of columns
        for j in range(len(sprite[0])):  # This will iterate through the amount of rows
            world[i+y][j+x] = sprite[i][j]  # Replaces part of the world matrix with a sub-matrix (sprite) at the x and y

def run_simulation(opts, world):
    """
    Accepts: opts  -- a populated command line options class instance
             world -- a 2D world pixel buffer generated by generate_world()

    Returns: (Nothing)

    Description: This function generates the plot that we will use as a
                 rendering surfance.  'Living' cells (represented as 1s in
                 the 2D world matrix) will be rendered as black pixels and
                 'dead' cells (represetned as 0s) will be rendered as
                 white pixels.  The method FuncAnimation() accepts 4
                 parameters: the figure, the frame update function, a
                 tuple containing arguments to pass to the update function,
                 and the frame update interval (in milliseconds).  Once the
                 show() method is called to display the plot, the frame
                 update function will be called every 'interval'
                 milliseconds to update the plot image (img).
    """
    if not world:
        print("The 'world' was never created.  Exiting")
        sys.exit()

    fig = plt.figure()
    img = plt.imshow(world, interpolation='none', cmap='Greys', vmax=1, vmin=0)
    ani = animation.FuncAnimation(fig,
                                  update_frame,
                                  fargs=(opts, world, img),
                                  interval=opts.framedelay)

    plt.show()


def report_options(opts):
    """
    Accepts: opts  -- a populated command line options class instance

    Returns: (Nothing)

    Descrption: This function simply prints the parameters used to
                start the 'Game of Life' simulation.
    """

    print("Conway's Game of Life")
    print("=====================")
    print("   World Size: %i x %i" % (opts.rows, opts.cols))
    print("   World Type: %s" % (opts.world_type))
    print("  Frame Delay: %i (ms)" % (opts.framedelay))


def get_commandline_options():
    """
    Accepts: (Nothing)

    Returns: opts  -- an instance of the options class that possesses members
                      specified by the 'dest' parameter of the add_option()
                      method.  Members contain the 'default' value unless
                      the user supplies a value from the command line using
                      the appropriate switch (i.e. '-r 100' or '--rows 100')

    optparse module documentation:
    https://docs.python.org/2/library/optparse.html
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--rows',
                        help='set # of rows in the world',
                        action='store',
                        type=int,
                        dest='rows',
                        default=50)

    parser.add_argument('-c', '--columns',
                        help='set # of columns in the world',
                        action='store',
                        type=int,
                        dest='cols',
                        default=50)

    parser.add_argument('-w', '--world',
                        help='type of world to generate',
                        action='store',
                        type=str,
                        dest='world_type',
                        default='empty')

    parser.add_argument('-d', '--framedelay',
                        help='time (in milliseconds) between frames',
                        action='store',
                        type=int,
                        dest='framedelay',
                        default=10)

    opts = parser.parse_args()

    return opts


def main():
    """
    The main function -- everything starts here!
    """
    opts = get_commandline_options()
    world = generate_world(opts)
    report_options(opts)

    blit(world, patterns_Alan_Davis_061.starrynight, 20, 20)

    run_simulation(opts, world)


if __name__ == '__main__':
    main()

#Finished