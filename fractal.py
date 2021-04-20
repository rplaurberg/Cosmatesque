import numpy as np
from PIL import Image
import copy
import os


class Fractal:
    "Describes/generates a fractal using an array of recurrence coefficients and a modulus."

    def __init__(self, coefficients=[[0, 1], [1, 0]], modulus=2, white_residues=[1]):
        # Default parameters generate the Sierpinski triangle
        self.coefficients = coefficients.copy()
        self.reach = len(coefficients)
        self.modulus = modulus
        self.white_residues = white_residues

    def summary(self):
        "Summarizes the fractal-generating arguments as a string. Good for filenames"
        visible_white_residues = [residue for residue in self.white_residues if residue < self.modulus]

        # Exclude last item from square coefficient matrix
        # Use deepcopy to leave original unchanged
        relevant_coefficients = copy.deepcopy(self.coefficients)
        del relevant_coefficients[-1][-1]

        summary_string = (
            str(relevant_coefficients)
            + ", modulus=" + str(self.modulus)
            + ", white_residues=" + str(visible_white_residues)
        )
        return summary_string

    def residue_array(self, size):
        "Carries out recurrence relation to calculate, return residues in size x size array as list-of-lists."

        # Initialize residue array
        residues = [[0 for x in range(size)] for y in range(size)]
        residues[0][0] = 1

        offset = self.reach - 1

        # Carry out recurrence relation to make residue array
        for x in range(size):
            for y in range(size):
                if x + y > 0:
                    new_value = 0
                    for x_i in range(self.reach):
                        for y_i in range(self.reach):
                            if x - offset + x_i >= 0 and y - offset + y_i >= 0:
                                new_value += self.coefficients[y_i][x_i] * residues[y - offset + y_i][x - offset + x_i]
                            # end if
                        # next y_i
                    # next x_i
                    new_value %= self.modulus
                    residues[y][x] = new_value
                # end if
            # next y
        # next x

        return residues

    def bw_image(self, size):
        "Generates black and white PIL Image object"

        residues = self.residue_array(size)

        # Black = 0, white = 255.  Initialize all black.
        monochrome_array = np.zeros((size, size), dtype=np.uint8)
        for x in range(size):
            for y in range(size):
                if residues[y][x] in self.white_residues:
                    monochrome_array[y][x] = 255
        img = Image.fromarray(monochrome_array, mode='L')

        return img

    def gradient_image(self, size):
        "Generates gradient PIL Image object"

        residues = self.residue_array(size)

        # Convert residue array to 0 = black and 1 = white.
        bw_base = [[0 for x in range(size)] for y in range(size)]
        for x in range(size):
            for y in range(size):
                if residues[y][x] in self.white_residues:
                    bw_base[y][x] = 1
                # end if
            # next y
        # next x

        # Iteration parameter: smallest integer d for which modulus ^ d >= residue array size
        # Equivalent to math.ceil(math.log(size, self.modulus)) without rounding errors
        depth = 0
        while self.modulus ** depth < size:
            depth += 1

        # Stack zoomed-in layers of bw_base atop one another
        layered_bw = [[0 for x in range(size)] for y in range(size)]
        for x in range(size):
            for y in range(size):
                new_value = 0
                for d in range(depth):  # Ignore largest value, which would overlay entire image when exact power
                    new_value += bw_base[y // self.modulus ** d][x // self.modulus ** d]
                # next d
                layered_bw[y][x] = new_value
            # next y
        # next x

        # Black = 0, white = 255.  Initialize all black.
        gradient_array = np.zeros((size, size), dtype=np.uint8)
        for x in range(size):
            for y in range(size):
                gradient_array[y][x] = int(layered_bw[y][x] * 255 / (depth))
        img = Image.fromarray(gradient_array, mode='L')

        return img


def make_image(coefficients=[[0, 1], [1]],
               modulus=2,
               white_residues=[1],
               picture='bw',size=1024):
    "Generates and saves an image using Cosmatesque filenames as arguments"
    # Useful for people who want to explore beyond the limitations of the GUI:
    # for example, iterating over a range of parameters or using larger coefficient arrays.
    # Default arguments generate Sierpinski triangle optimized for screen (white on black).
    # Coefficients must be square-minus-a-corner.  Currently no error checking of arguments.

    # Add final '0' to coefficient array
    coefficients[-1].append(0)

    # Make fractal object
    fr = Fractal(coefficients=coefficients, modulus=modulus, white_residues=white_residues)

    filename = (fr.summary()
                + ", picture= '" + picture
                + "', size=" + str(size)
                + ".png"
                )

    # Save and open image
    if picture == 'bw':
        img = fr.bw_image(size=size)
    else:
        img = fr.gradient_image(size=size)
    img.save(filename)
    os.startfile(filename)
