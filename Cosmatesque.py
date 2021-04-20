import PySimpleGUIQt as sg  # Qt version necessary for changeable button color on Mac
import random
import os, sys, subprocess
from PIL import Image
import fractal as fr

# TO DO
# On Mac:
# Make filename entry box wider
# Get "Save" button label to change to "Working..." immediately upon click
# Get window element centering to work
# On Linux:
# Test program, set appearance parameters


# Constants
CA_SIZE = 3
MAX_MODULUS = 5


# Functions for mediating between fractal object and GUI
def button_color(fractal, residue):
    "Returns button color descriptive tuple per residue for GUI"
    black_button = ('white', 'black')   # white (text) on black (background)
    white_button = ('black', 'white')   # black (text) on white (background)
    gray_button = ('gray', 'gray')      # grayed out button
    if residue >= fractal.modulus:
        return gray_button
    elif residue in fractal.white_residues:
        return white_button
    else:
        return black_button

def generate_preview_images():
    "Saves preview images to root directory"
    preview_gradient = fractal.gradient_image(preview_render_size_from_modulus[fractal.modulus])
    preview_gradient = preview_gradient.resize(preview_element_size, resample=Image.NEAREST)
    preview_gradient.save('preview_gradient.png')
    preview_bw = fractal.bw_image(preview_render_size_from_modulus[fractal.modulus])
    preview_bw = preview_bw.resize(preview_element_size, resample=Image.NEAREST)
    preview_bw.save('preview_bw.png')

def auto_filename(picture):
    "Generates picture filename, sans .png. Argument picture should be 'bw' or 'gradient'"
    filename = (
            fractal.summary()
            + ", picture= '" + picture
            + "', size="
            + str(saved_picture_size_per_modulus[fractal.modulus])
    )
    return filename



# GUI preview parameters
preview_render_size_from_modulus = {
    2: 128,
    3: 81,
    4: 128,
    5: 125
}
preview_element_size = (450, 450)   # Fits 1360 x 768 laptop resolution


# Initialize fractal with 3x3 array and Sierpinski triangle parameters + extra white residues
fractal = fr.Fractal(
    modulus=2,
    coefficients=[
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0]
    ],
    white_residues=[1, 2, 3, 4]
)

# Initialize preview files
generate_preview_images()

# Initialize saved picture sizes
saved_picture_size_per_modulus = {
    2: 1024,
    3: 729,
    4: 1024,
    5: 625
}


# Button sizes for GUI
if sys.platform == 'win32':         # Windows
    square_px = (60, 60)        # square button for coefficients, residues
    sq_half_px = (90, 60)       # 1.5 x square button for coefficient operations
    half_px = (156, 60)         # button to fill half column, used for modulus
    long_px = (316, 30)         # long single-line button, used for "Apply to coefficients"
    third_rect_px = (102, 30)   # rectangle to fill 1/3 of column, for residue color operations
    long_tall_px = (316, 60)    # long & tall button, used for "Randomize all"
    presets_px = (102, 60)      # tall rectangle to fill 1/3 of colun, for preset parameters
    save_px = (450, 30)         # spans length of preview images
    long_text_px = (500, 30)    # long text display, used to show save folder path
    text_entry_px = (400, 30)   # filename text input field
    browse_button = (20, 1)     # saved folder browse button, not in px
else:                               # Mac, sys.platform == 'darwin'; no testing on Linux yet
    square_px = (60, 55)        # square button for coefficients, residues
    sq_half_px = (90, 55)       # 1.5 x square button for coefficient operations
    half_px = (150, 55)         # button to fill half column, used for modulus
    long_px = (300, 28)         # long single-line button, used for "Apply to coefficients"
    third_rect_px = (95, 28)    # rectangle to fill 1/3 of column, for residue color operations
    long_tall_px = (300, 55)    # long & tall button, used for "Randomize all"
    presets_px = (105, 55)      # tall rectangle to fill 1/3 of colun, for preset parameters
    save_px = (450, 28)         # spans length of preview images
    long_text_px = (500, 28)    # long text display, used to show save folder path
    text_entry_px = (400, 28)   # filename text input field
    browse_button = (20, 1)     # saved folder browse button, not in px


# Event collections
coefficient_event_keys = [(x,y) for x in range(CA_SIZE) for y in range(CA_SIZE)]
black_white_event_keys = [('black/white', residue) for residue in range(MAX_MODULUS)]


# GUI elements
parameter_column = [[sg.Text('Recurrence coefficients')]]

coefficient_column = [[sg.Button(fractal.coefficients[row][column], size_px=square_px, pad=(0,0), key=(row, column))
                      for column in range(CA_SIZE)] for row in range (CA_SIZE)]
coefficient_column[-1][-1] = sg.Button('CURSOR', size_px=square_px, pad=(0,0), disabled=True)

coeff_manip_column = [[sg.Button('Clear', size_px=sq_half_px, pad=(0,0))],
                      [sg.Button('Randomize', size_px=sq_half_px, pad=(0,0), key='randomize coefficients')],
                      [sg.Checkbox('', key='randomize symmetrically')],
                      [sg.Text('Randomize')],
                      [sg.Text('symmetrically')]]

parameter_column += [[sg.Column(coefficient_column), sg.Column(coeff_manip_column, element_justification='center')],
                     [sg.Text('\n')],   # hacky empty space
                     [sg.Text('Modulus', size_px=half_px, pad=(0,0), justification='center'),
                      sg.Button(fractal.modulus, size_px=half_px, pad=(0,0), key='modulus')],
                     [sg.Button('Apply to coefficients', size=long_px, pad=(0,0))],
                     [sg.Text('\n'+'Black/white residues')],
                     [sg.Button(residue, size_px=square_px, pad=(0,0), button_color=button_color(fractal, residue),
                                disabled=(residue >= fractal.modulus), key=('black/white', residue))
                     for residue in range(MAX_MODULUS)],
                     [sg.Button('Reverse', size_px=third_rect_px, pad=(0,0)),
                      sg.Button('Randomize', size_px=third_rect_px, pad=(0,0), key='randomize black/white'),
                      sg.Button('Default', size_px=third_rect_px, pad=(0,0), key='default black/white')],
                     [sg.Text('\n')],
                     [sg.Button('Randomize all', size_px=long_tall_px, pad=(0,0))],
                     [sg.Text('\n')],
                     [sg.Button('Sierpinski\ntriangle', size_px=presets_px, pad=(0,0), key='Sierpinski triangle'),
                      sg.Button('Sierpinski\ncarpet', size_px=presets_px, pad=(0,0), key='Sierpinski carpet'),
                      sg.Button("Fredkin's\nreplicator", size_px=presets_px, pad=(0,0), key="Fredkin's replicator")]
                     ]

gradient_column = [[sg.Text('Gradient image preview')],
                   [sg.Image(filename='preview_gradient.png', key='preview_gradient')],
                   [sg.Button('Save', size_px=save_px, pad=(0, 0), key='save gradient')],
                   [sg.Text('Filename:'),
                    sg.Input(default_text=auto_filename('gradient'), size_px=text_entry_px, key='gradient filename')]
                   ]

bw_column = [[sg.Text('Black and white image preview')],
             [sg.Image(filename='preview_bw.png', key='preview_bw')],
             [sg.Button('Save', size_px=save_px, pad=(0, 0), key='save bw')],
             [sg.Text('Filename:'),
              sg.Input(default_text=auto_filename('bw'), size_px=text_entry_px, key='bw filename')]]

saving_options_column_1 = [
    [sg.Checkbox('Automatic file names  (extension .png not shown)', default=True, enable_events=True, key='auto filename')],
    [sg.Checkbox('Open file after saving', default=True, key='open after save')],
    [sg.Text('Save folder:'),
     sg.Input(default_text=os.getcwd(), enable_events=True, visible=False, key='path'),
     sg.Text(os.getcwd(), size_px=long_text_px, key='save folder')],
    [sg.FolderBrowse('Change save directory', size=browse_button, pad=(0,0), target='path')]
]

saving_options_column_2 = [
    [sg.Text('Saved picture size:'),
     sg.Text(
         str(saved_picture_size_per_modulus[fractal.modulus])
         + ' x '
         + str(saved_picture_size_per_modulus[fractal.modulus]),
         key='saved picture size')],
    [sg.Button('Smaller', size_px=third_rect_px, pad=(0, 0)),
     sg.Button('Larger', size_px=third_rect_px, pad=(0, 0))],
    [sg.Text('Larger images will take longer to render.')]
]

path_column = [[sg.FolderBrowse('Save to', size=third_rect_px, pad=(0,0), target='directory'),
                sg.Text(os.getcwd(), size=(50,1), key='shown directory'),
                ]]

picture_column = [[sg.Column(gradient_column, element_justification='center'),
                   sg.Column(bw_column, element_justification='center')],
                  [sg.Column(saving_options_column_1, element_justification='left'),
                   sg.Column(saving_options_column_2, element_justification='center')]]

layout = [[sg.Column(parameter_column, element_justification='center'),
           sg.Column(picture_column, element_justification='center')]]

# Create the window
window = sg.Window('Cosmatesque', layout, grab_anywhere=True)

# Event loop
while True:
    event, values = window.read()
    # print(event, values)  # Enable for debugging

    # First few functions handle visible changes to GUI

    def refresh_display():
        """
        Refresh all visual components: coefficients, modulus, black/white residues, previews.
        Also update filename and displayed picture size, but there are smaller functions for those alone.
        """

        # Refresh coefficients
        for x in range(CA_SIZE):
            for y in range(CA_SIZE):
                if (x, y) != (CA_SIZE - 1, CA_SIZE - 1):
                    window.Element((x,y)).Update(fractal.coefficients[x][y])
                # end if
            # next y
        # next x

        # Refresh modulus
        window.Element('modulus').Update(fractal.modulus)

        # Refresh black/white buttons
        for residue in range(5):
            window.Element(('black/white', residue)).Update(residue, button_color=button_color(fractal, residue),
                                                            disabled=(residue >= fractal.modulus))

        # Refresh previews
        generate_preview_images()
        window.Element('preview_gradient').Update(filename='preview_gradient.png')
        window.Element('preview_bw').Update(filename='preview_bw.png')

        # Refresh displayed picture size
        window.Element('saved picture size').Update(str(saved_picture_size_per_modulus[fractal.modulus])
                       + ' x '
                       + str(saved_picture_size_per_modulus[fractal.modulus]))

        # Refresh filenames
        if values['auto filename']:
            window.Element('gradient filename').Update(auto_filename('gradient'))
            window.Element('bw filename').Update(auto_filename('bw'))
        else:
            window.Element('gradient filename').Update('')
            window.Element('bw filename').Update('')

    def refresh_picture_size():
        "Refresh the to-be-generated picture size without updating all preview-related elements"
        window.Element('saved picture size').Update(str(saved_picture_size_per_modulus[fractal.modulus])
                       + ' x '
                       + str(saved_picture_size_per_modulus[fractal.modulus]))

    def refresh_filename():
        "Refresh the filaname only without updating all preview-related elements"
        if values['auto filename']:
            window.Element('gradient filename').Update(auto_filename('gradient'))
            window.Element('bw filename').Update(auto_filename('bw'))
        else:
            window.Element('gradient filename').Update('')
            window.Element('bw filename').Update('')


    # Subsequent functions handle data elements only

    def change_coefficient(event):
        row = event[0]
        column = event[1]
        fractal.coefficients[row][column] = (fractal.coefficients[row][column] + 1) % fractal.modulus

    def clear_coefficients():
        for x in range(CA_SIZE):
            for y in range(CA_SIZE):
                fractal.coefficients[y][x] = 0
                # end if
            # next y
        # next x

    def randomize_coefficients():
        for x in range(CA_SIZE):
            for y in range(CA_SIZE):
                fractal.coefficients[y][x] = random.randrange(fractal.modulus)
                if values['randomize symmetrically'] and x > y:
                    fractal.coefficients[y][x] = fractal.coefficients[x][y]
                # end if
            # next y
        # next x
        fractal.coefficients[-1][-1] = 0

    def change_modulus():
        if fractal.modulus < MAX_MODULUS:
            fractal.modulus += 1
        else:
            fractal.modulus = 2     # minimum modulus

    def randomize_modulus():
        fractal.modulus = random.randrange(2, MAX_MODULUS + 1)

    def apply_modulus_to_coefficients():
        for x in range(CA_SIZE):
            for y in range(CA_SIZE):
                fractal.coefficients[y][x] = fractal.coefficients[y][x] % fractal.modulus
                if (x, y) != (CA_SIZE - 1, CA_SIZE - 1):
                    window.Element('modulus').Update(fractal.modulus)
                # end if
            # next y
        # next x

    def change_black_white(event):
        residue = event[1]
        if residue in fractal.white_residues:
            fractal.white_residues.remove(residue)
        else:
            fractal.white_residues.append(residue)
            fractal.white_residues.sort()   # keep sorted for debugging, filename making

    def reverse_black_white():
        for residue in range(MAX_MODULUS):
            if residue in fractal.white_residues:
                fractal.white_residues.remove(residue)
            else:
                fractal.white_residues.append(residue)

    def randomize_black_white():
        old_white_residues = fractal.white_residues.copy()
        old_visible_white_residues = [residue for residue in old_white_residues if residue < fractal.modulus]
        visible_white_residues_changed = False
        visible_colors_distinct = False
        while not(visible_colors_distinct) or not(visible_white_residues_changed):
            new_white_residues = [residue for residue in range(MAX_MODULUS) if random.choice([True, False])]
            new_visible_white_residues = [residue for residue in new_white_residues if residue < fractal.modulus]
            visible_white_residues_changed = new_visible_white_residues != old_visible_white_residues
            visible_colors_distinct = len(new_visible_white_residues) > 0 and len(new_visible_white_residues) < fractal.modulus
        # end while loop, knowing that new and distinct colors are used
        fractal.white_residues = new_white_residues

    def default_black_white():
        fractal.white_residues = [1, 2, 3, 4]

    def sierpinski_triangle():
        fractal.modulus = 2
        fractal.coefficients = [[0, 0, 0],
                                [0, 0, 1],
                                [0, 1, 0]]
        fractal.white_residues = [0]

    def sierpinski_carpet():
        fractal.modulus = 3
        fractal.coefficients = [[0, 0, 0],
                                [0, 1, 1],
                                [0, 1, 0]]
        fractal.white_residues = [0]

    def fredkins_replicator():
        fractal.modulus = 2
        fractal.coefficients = [[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 0]]
        fractal.white_residues = [0]

    def increase_saved_picture_size():
        saved_picture_size_per_modulus[fractal.modulus] *= fractal.modulus

    def decrease_saved_picture_size():
        if saved_picture_size_per_modulus[fractal.modulus] > 1:
            saved_picture_size_per_modulus[fractal.modulus] //= fractal.modulus

    def save_gradient():
        window.Element('save gradient').Update('Working...')  # Why delayed on Mac?
        window.refresh()
        gradient_image = fractal.gradient_image(saved_picture_size_per_modulus[fractal.modulus])
        try:
            filename = values['gradient filename'] + '.png'
            path_and_filename = os.path.join(values['path'], filename)
            gradient_image.save(fp=path_and_filename)
        except:
            sg.popup("Error. Please check filename and directory.", keep_on_top=True)
        else:
            # Success!
            if values['open after save']:
                if sys.platform == 'win32':
                    os.startfile(path_and_filename)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, path_and_filename])
            else:
                sg.popup("Saved!", no_titlebar=True, keep_on_top=True)
        window.Element('save gradient').Update('Save')

    def save_bw():
        window.Element('save bw').Update('Working...')
        window.refresh()
        gradient_image = fractal.bw_image(saved_picture_size_per_modulus[fractal.modulus])
        try:
            filename = values['bw filename'] + '.png'
            path_and_filename = os.path.join(values['path'], filename)
            gradient_image.save(fp=path_and_filename)
        except:
            sg.popup("Error. Please check filename and directory.", keep_on_top=True)
        else:
            # Success!
            if values['open after save']:
                if sys.platform == "win32":
                    os.startfile(path_and_filename)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open" #
                    subprocess.call([opener, path_and_filename])
            else:
                sg.popup("Saved!", no_titlebar=True, keep_on_top=True)
        window.Element('save bw').Update('Save')

    def change_directory():
        window.Element('save folder').Update(str(values['path']))


    if event is None:
        break
    elif event in coefficient_event_keys:
        change_coefficient(event)
        refresh_display()
    elif event == 'Clear':
        clear_coefficients()
        refresh_display()
    elif event == 'randomize coefficients':
        randomize_coefficients()
        refresh_display()
    elif event == 'modulus':
        change_modulus()
        refresh_display()
    elif event == 'Apply to coefficients':
        apply_modulus_to_coefficients()
        refresh_filename()  # preview unchanged, need only to refresh filename
    elif event in black_white_event_keys:
        change_black_white(event)
        refresh_display()
    elif event == 'Reverse':
        reverse_black_white()
        refresh_display()
    elif event == 'randomize black/white':
        randomize_black_white()
        refresh_display()
    elif event == 'default black/white':
        default_black_white()
        refresh_display()
    elif event == 'Randomize all':
        randomize_modulus()
        randomize_coefficients()
        randomize_black_white()
        refresh_display()
    elif event == 'Sierpinski triangle':
        sierpinski_triangle()
        refresh_display()
    elif event == 'Sierpinski carpet':
        sierpinski_carpet()
        refresh_display()
    elif event == "Fredkin's replicator":
        fredkins_replicator()
        refresh_display()
    elif event == 'auto filename':
        refresh_filename()
    elif event == 'Larger':
        increase_saved_picture_size()
        refresh_picture_size()
        refresh_filename()
    elif event == 'Smaller':
        decrease_saved_picture_size()
        refresh_picture_size()
        refresh_filename()
    elif event == 'save gradient':
        save_gradient()
    elif event == 'save bw':
        save_bw()
    elif event == 'path':
        change_directory()
# end while

window.close()
