#! /usr/bin/env python3

################################################################################
###                                  NOTES                                   ###
################################################################################

# EXPLANATION GOES HERE

################################################################################
###                                   TODO                                   ###
################################################################################

# Clean up file
# Improve interface
# test different scenarios (bits, sizes, stack IMG and TXT in a single image)

################################################################################
###                                  IMPORT                                  ###
################################################################################

from PIL import Image
from os import system, path

################################################################################
################################################################################
###                           ENCODE TEXT IN IMAGE                           ###
################################################################################
################################################################################

def encode_text_in_image():
    print("------------------------------------------")
    print("           ENCODE TEXT IN IMAGE           ")
    print("------------------------------------------")

    img = get_img_from_path('ENTER PATH TO IMAGE TO ENCODE TEXT IN: ')
    width, height = img.size
    
    message = get_message()

    max_x, max_y, max_num = check_max_chars(width, height, message)
    start_x, start_y = get_start_coordinates(max_x, max_y, max_num, width, height)
    start_num = coord_to_num(start_x, start_y, width)

    bit_index = which_bit('Which bit to encode the message in LSB 0 - MSB 7 (0 recommended)? ')
    bin_text = text_to_binary(message)

    pixels = img.load()

    # Initialize pixel/coord counter
    num = start_num
    # make multiple of 8, so bytes align with decoder
    remainder = num % 8
    num = num - remainder

    # ENCODE
    for bin_idx in range(len(bin_text)):
        x, y = num_to_coord(num, width)
        r,g,b = pixels[x,y]
        # R
        if bin_idx % 3 == 0:
            r_val = pixels[x,y][0]
            new_r_val = write_bit_to_color(r_val, bin_text[bin_idx], bit_index)
            #print(bin_idx, num, bin_text[bin_idx], r_val, new_r_val)
            pixels[x,y]= (new_r_val, g, b)
            #print(pixels[x,y][0])

        # G
        elif bin_idx % 3 == 1:
            g_val = pixels[x,y][1]
            new_g_val = write_bit_to_color(g_val, bin_text[bin_idx], bit_index)
            #print(bin_idx, num, bin_text[bin_idx], g_val, new_g_val)
            pixels[x,y] = (r, new_g_val, b)
            #print(pixels[x,y][1])
        # B
        elif bin_idx % 3 == 2:
            b_val = pixels[x,y][2]
            new_b_val = write_bit_to_color(b_val, bin_text[bin_idx], bit_index)
            #print(bin_idx, num, bin_text[bin_idx], b_val, new_b_val)
            pixels[x,y] = (r, g, new_b_val)
            #print(pixels[x,y][2])
            num += 1
        else:
            print('ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR-ERROR')

    # SAVE
    encoded_img_name = input('ENTER PATH/NAME FOR ENCODED IMAGE OUTPUT: ')
    img.save(encoded_img_name, format = 'png')
    print('IMAGE SAVED AS:', encoded_img_name)
    input('Press enter to continue.')


# Takes COLOR VALUE (0-255) as INT, bit (0-1), as STRING, and index as int.
# Returns INT with new color value, having replaced bit.
def write_bit_to_color(color_val, bit, idx):
    new_bin_color_val = list(format(color_val, '08b'))
    new_bin_color_val[idx] = bit
    new_color = int(''.join(new_bin_color_val), 2)

    return new_color

def text_to_binary(text):
    bin_text = ''.join(format(ord(i), '08b') for i in text)
    return bin_text

# Checks the image is large enough to fit the message
# Returns MAX COORDINATES for message to start at.
def check_max_chars(width, height, msg):

    msg_bin_length = len(msg) * 8
    total_pixels = width * height
    pixels_needed = int(msg_bin_length / 3) + 1

    # Check if there are enough pixels to FIT the message
    if total_pixels >= pixels_needed:
        # Calculate MAX COORDS
        last_starting_pixel = total_pixels - pixels_needed
        max_x, max_y = num_to_coord(last_starting_pixel, width)
        max_num = coord_to_num(max_x, max_y, width)

        # print('msg len', msg_bin_length, 'total px', total_pixels, 'px needed', pixels_needed)
        # print('last:', last_starting_pixel, 'x', max_x, 'y', max_y)
        # print('max num:', max_num)

        return max_x, max_y, max_num

    else:
        print("THE IMAGE ISN'T LARGE ENOUGH TO FIT THE MESSAGE")
        quit_fn()

# Gets START COORDINATES for pixel to start encoding message.
# Returns 3 INTs: X, Y coordinates
def get_start_coordinates(max_x, max_y, max_num, width, height):
    print('')
    print('ENTER X AND Y COORDINATES FOR THE START OF THE MESSAGE')
    print('X = 0, Y = 0, IS THE TOP LEFT PIXEL WIDTH = ', (width -1), 'HEIGHT =', (height -1))
    print('X =', max_x, 'Y =', max_y, 'IS THE MAX COORDINATE TO FIT THE MESSAGE')
    x = input('X = ')
    y = input('Y = ')
    
    if x.isdigit() and y.isdigit():
        x = int(x)
        y = int(y)
        start_num = coord_to_num(x, y, width)
        
        if start_num <= max_num and x <= (width-1):
            return x, y
        
        else:
            print('\nINVALID COORDINATE. ENTER COORD BETWEEN: [0,0] - [%d,%d]' % (max_x, max_y))
            x, y = get_start_coordinates(max_x, max_y, max_num, width, height)
            return x, y

        
    else:
        print('\nINVALID COORDINATE. ENTER COORD BETWEEN: [0,0] - [%d,%d]' % (max_x, max_y))
        x, y = get_start_coordinates(max_x, max_y, max_num, width, height)
        return x, y

# Gets USER INPUT message to encode. Returns MESSAGE as STR
def get_message():
    message = input('MESSAGE TO ENCODE: ')
    return message


################################################################################
###                          IMAGE/MATRIX COORDINATES                        ###
################################################################################

# Takes X, Y coordinates as INTs, and image WIDTH as INT
# Returns INT corresponding to pixel number of coordinates
def coord_to_num(x, y, width):
    if x < 0:
        x = 0
    elif x >= (width):
        x = width - 1

    num = x + y * width
    return num


# Takes INT of pixel number (^see funcion above^), and image WIDTH as INT
# Returns X, Y coordinates as 2 INTs.
def num_to_coord(num, width):
    x = num % width
    y = int(num / width)
    return x, y

################################################################################
################################################################################
###                           DECODE TEXT IN IMAGE                           ###
################################################################################
################################################################################

def decode_text_in_img():
    print("------------------------------------------")
    print("           DECODE IMAGE IN IMAGE          ")
    print("------------------------------------------")

    encoded_img = get_img_from_path('ENTER PATH TO ENCODED IMAGE (TO DECODE): ')
    encoded_pixels = encoded_img.load()    
    width, height = encoded_img.size

    bit_index = which_bit('Which bit to decode? LSB 0 - MSB 7 (0 recommended) ')
    
    bin_string = ''

    for y in range(height):
        for x in range(width):
            r, g, b = encoded_pixels[x,y]
            for val in [r,g,b]:
                bin_val = format(val, '08b')
                bin_string += bin_val[bit_index]

    decoded_text = binary_to_text(bin_string)
    # print(bin_string)
    print()
    print(decoded_text)
    print()
    # Save text fil
    out_file = input('ENTER PATH/NAME FOR DECODED TEXT OUTPUT: ')
    with open(out_file, 'w') as f:
        f.write(decoded_text)
    print('TEXT FILE SAVED AS:', out_file)
    input('Press enter to continue.')

# Tales a string of binary characters. Returns a string of ASCII characters.
def binary_to_text(bin_text):
    decoded_text = ''.join(chr(int(bin_text[i:i+8], 2)) for i in range(0, len(bin_text), 8))
    return decoded_text

################################################################################
###                              TEXT IN IMAGE                               ###
###                                  SHARED                                  ###
################################################################################

def which_bit(question):
    bit = input(question)
    if bit.isdigit():
        bit = int(bit)
        if 0 <= bit <= 7:
            bit_index = - bit - 1
            return bit_index
        else:
            print('PLEASE ENTER A NUMBER BETWEEN 0 AND 7')
            bit = which_bit()
            bit_index = - bit - 1
            return bit_index
    else:
        print('PLEASE ENTER A NUMBER BETWEEN 0 AND 7')
        bit = which_bit()
        bit_index = - bit - 1
        return bit_index

################################################################################
################################################################################
###                                  ENCODE                                  ###
###                              IMAGE IN IMAGE                              ###
################################################################################
################################################################################

def encode_img_in_img():
    print("------------------------------------------")
    print("          ENCODE IMAGE IN IMAGE           ")
    print("------------------------------------------")
    # get IMGs
    img_top, img_under =  get_imgs_to_encode()

    # get number of significant bits
    n_SB = get_n_SB()

    # load IMGs
    top_pixels = img_top.load()
    under_pixels = img_under.load()
    width, height = img_top.size
    
    # NEW IMAGE
    encoded_img = Image.new(mode = 'RGB', size = img_top.size, color = 0)
    encoded_pixels = encoded_img.load()
    # Remove LSB from TOP_IMG
    for y in range(height):
        for x in range(width):
            r_top, g_top, b_top = top_pixels[x,y]
            r_top_minus_n_SB = remove_LSBs(r_top, n_SB)
            g_top_minus_n_SB = remove_LSBs(g_top, n_SB)
            b_top_minus_n_SB = remove_LSBs(b_top, n_SB)

            r_under, g_under, b_under = under_pixels[x,y]
            r_under_n_MSB = get_n_MSBs(r_under, n_SB)
            g_under_n_MSB = get_n_MSBs(g_under, n_SB)
            b_under_n_MSB = get_n_MSBs(b_under, n_SB)

            new_r_bin = r_top_minus_n_SB + r_under_n_MSB
            new_g_bin = g_top_minus_n_SB + g_under_n_MSB
            new_b_bin = b_top_minus_n_SB + b_under_n_MSB

            new_r = int(new_r_bin, 2)
            new_g = int(new_g_bin, 2)
            new_b = int(new_b_bin, 2)
            
            encoded_pixels[x,y] = (new_r, new_g, new_b)

    encoded_img_name = input('ENTER PATH/NAME FOR ENCODED IMAGE OUTPUT: ')
    encoded_img.save(encoded_img_name, format = 'png')
    print('IMAGE SAVED AS:', encoded_img_name)
    #encoded_img.show()
    input('Press enter to continue.')

def get_n_MSBs(val, n_SB):
    b_val = bin(val)
    b_val = b_val[2:]
    b_val = b_val.zfill(8)
    n_msb = b_val[0:n_SB]
    #print(val, b_val, n_msb)
    return n_msb

# Takes INT channel value (0-255), returns binary STRING len (8 - num_SigBits)
def remove_LSBs(val, n_SB):
    shifted_val = val >> n_SB
    #b_val = bin(val)
    shifted_b_val = bin(shifted_val)
    shifted_b_val = shifted_b_val[2:]
    shifted_b_val = shifted_b_val.zfill(8 - n_SB)
    # print(val, b_val, shifted_val, shifted_b_val)
    return shifted_b_val

# Gets USER INPUT for 2 images. Checks path and if they're the same size.
# Returns 2 IMAGE objects
def get_imgs_to_encode():    
    img_top = get_img_from_path('ENTER PATH TO TOP IMAGE: ')
    img_under = get_img_from_path('ENTER PATH TO IMAGE TO HIDE: ')

    if img_size_check(img_top, img_under):
        return img_top, img_under

# Returns TRUE if images are the same size.
def img_size_check(img_top, img_under):
    if img_top.size == img_under.size:
        return True
    else:
        print('Images are not the same size')
        quit_fn()

################################################################################
###                                  SHARED                                  ###
################################################################################

# Takes a STR, displayed as a question to the user, and gets a path to an image file
# Checks that the path is correct and that it's a valid image object.
# Returns an IMAGE OBJECT.
def get_img_from_path(question):
    print('ENTER "q" TO QUIT OR')
    img_path = input(question)
    if img_path.lower() == 'q':
        quit_fn()
    elif path.exists(img_path):
        try:
            img = Image.open(img_path)
            img = img.convert('RGB')
            return img
        except:
            print(img_path, 'IS NOT AN IMAGE OR VALID IMAGE FORMAT.')
            quit_fn()
    else:
        print("PATH DOESN'T EXIST")
        img = get_img_from_path(question)
        img = img.convert('RGB')
        return img


def get_n_SB():
    n_SB = input('How many bits to encode/decode? 1 - 4 (2 recommended)? ')
    if n_SB.isdigit():
        n_SB = int(n_SB)
        if 1 <= n_SB <= 4:
            return n_SB
        else:
            print('PLEASE ENTER A NUMBER BETWEEN 1 AND 4')
            n_SB = get_n_SB()
            return n_SB
    else:
        print('PLEASE ENTER A NUMBER BETWEEN 1 AND 4')
        n_SB = get_n_SB()
        return n_SB

################################################################################
################################################################################
###                                  DECODE                                  ###
###                              IMAGE IN IMAGE                              ###
################################################################################
################################################################################

def decode_img_in_img():
    print("------------------------------------------")
    print("           DECODE IMAGE IN IMAGE          ")
    print("------------------------------------------")
    encoded_img = get_img_from_path('ENTER PATH TO ENCODED IMAGE (TO DECODE): ')
    encoded_pixels = encoded_img.load()    
    width, height = encoded_img.size

    # Initialize new decoded_img
    decoded_img = Image.new(mode = 'RGB', size = encoded_img.size, color = 0)
    decoded_pixels = decoded_img.load() 
    
    # get number of significant bits
    n_SB = get_n_SB()
    
    for y in range(height):
        for x in range(width):
            encoded_r, encoded_g, encoded_b = encoded_pixels[x,y]
            
            decoded_r = decode_val(encoded_r, n_SB)
            decoded_g = decode_val(encoded_g, n_SB)
            decoded_b = decode_val(encoded_b, n_SB)

            # Write decoded IMG
            decoded_pixels[x,y] = (decoded_r, decoded_g, decoded_b)

    decoded_img_name = input('ENTER PATH/NAME FOR DECODED IMAGE OUTPUT: ')
    # decoded_img_name = 'decoded_smiley_in_frog.png'
    decoded_img.save(decoded_img_name, format = 'png')
    print('DECODED IMAGE SAVED AS: %s' % (decoded_img_name))
    input('Press enter to continue.')


def decode_val(val, n_SB):
    bin_val = bin(val)[2:]
    bin_val = bin_val.zfill(8)
    n_MSBs = bin_val[-n_SB:]
    decoded_bin = n_MSBs + '0'*(8-n_SB)
    decoded_val = int(decoded_bin, 2)
    # print(val, bin(val), decoded_bin, decoded_val)
    return decoded_val
    
# Need to get INPUT and check path
def get_encoded_img():
    encoded_img = Image.open('encoded_smiley_in_frog.png')
    return encoded_img

################################################################################
################################################################################
###                                   MENUS                                  ###
################################################################################
################################################################################

def main_menu():
    clear()

    main_menu_options_list = [1,2,"q"]

    print("------------------------------------------")
    print("  <3AESIC_CYBER> LSB IMAGE STEGANOGRAPHY")
    print("------------------------------------------")
    print("1.   ENCODE")
    print("2.   DECODE")
    print("q.   QUIT")
    option = input('\nSelect your option: ')
    option = check_option(option, main_menu_options_list)
    #print("YOUR OPTION IS:", option)
    if option == 1:
        encode_menu('opt')
    if option == 2:
        decode_menu('opt')


# ENCODE MENU
def encode_menu(encode_opt):
    # Options List
    encode_opt_list = [1,2,"q"]
    
    while encode_opt != "q":
        clear()
        print("------------------------------------------")
        print("                  ENCODE                  ")
        print("------------------------------------------")
        print("1.   IMAGE IN IMAGE")
        print("2.   TEXT IN IMAGE")
        print("m.   BACK TO MAIN MENU")
        print("q.   QUIT")
        
        # INPUT
        encode_opt = input("\nSelect your option: ")
        encode_opt = check_option(encode_opt, encode_opt_list)
        # -1- IMAGE IN IMAGE
        if encode_opt == 1:
            encode_img_in_img()

        # -2- TEXT IN IMAGE
        elif encode_opt == 2:
            encode_text_in_image()

# DECODE MENU
def decode_menu(decode_opt):
    # Options List
    decode_opt_list = [1,2,"q"]
    
    while decode_opt != "q":
        clear()
        print("------------------------------------------")
        print("                  DECODE                  ")
        print("------------------------------------------")
        print("1.   IMAGE IN IMAGE")
        print("2.   TEXT IN IMAGE")
        print("m.   BACK TO MAIN MENU")
        print("q.   QUIT")
        
        # INPUT
        decode_opt = input("\nSelect your option: ")
        decode_opt = check_option(decode_opt, decode_opt_list)
        # -1- IMAGE IN IMAGE
        if decode_opt == 1:
            decode_img_in_img()

        # -2- TEXT IN IMAGE
        elif decode_opt == 2:
            decode_text_in_img()

def check_option(opt, opt_list):
    if opt.lower() == "q":
        quit_fn()
    elif opt.lower() == "m":
        main_menu()
    elif opt.isdigit() and int(opt) in opt_list:
        opt = int(opt)
        return opt
    else:
        opt = input("Please enter a valid option: ")
        opt = check_option(opt, opt_list)
        return opt

def quit_fn():
        print("------------------------------------------")
        print("              GOODBYE FRIEND              ")
        print("------------------------------------------")
        exit()

# CLEAR TERMINAL VIEW
def clear():
    _ = system('clear')

################################################################################
################################################################################
###                                   MAIN                                   ###
################################################################################
################################################################################

def main():
    main_menu()

if __name__ == '__main__':
    main()

################################################################################
###                                 END NOTES                                ###
################################################################################

# all working!
# 2/9/2021
