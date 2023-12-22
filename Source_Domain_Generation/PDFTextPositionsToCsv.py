import fitz
import xml.etree.ElementTree as ET
import os
# from cropForDiscriminator import CropInformation # SB commented out--got ModuleNotFoundError & doesn't seemed to be used anywhere in this script anyways

name = 'source_domain'

doc = fitz.open('C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/Source_Domain_Generation/Ezek-Rev.pdf') # 'generate_book.pdf')

os.mkdir('C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/Source_Domain_Generation/book_generation/' + name)
os.mkdir('C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/Source_Domain_Generation/book_generation/' + name + '-csv')
i = 1

print('Processing ' + str(len(doc)) + ' PDFs:')
for page in doc:
    csvDelimiter = '$' # because ',' can be part of the text
    zoom = 3.9 # zoom has to be adapted to fit with target domain / historical scripts
    mat = fitz.Matrix(zoom, zoom)

    pix = page.get_pixmap(matrix=mat) # increase picture size to be roughly the same as the scanned pictures (so in one crop there are roughly the same number of lines)
        # SB: previously page.getPixmap
    text = page.get_text('xml', flags=2)
        # SB: previously page.getText

    pix.save('C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/Source_Domain_Generation/book_generation/' + name + '/' + name + '-' + f"{i:03d}" + '.png')
        # SB: previously pix.writePNG
    f= open('currpage.xml','w+')

    f.write(str(text))
    f.close()

    csv = open('C:/Users/scott/Desktop/ManuscriptProject/Code/Generating-Synthetic-Handwritten-Historical-Documents/Source_Domain_Generation/book_generation/' + name + '-csv/' + name + '-' + f"{i:03d}" + '.csv', 'w+')  # information of all normal chars in pdf
    # lettrine = open('lettrine/lettrine-' + f"{i:03d}" + '.csv', 'w+')  # information of all lettrine in pdf # SB commented out (FileNotFoundError)
    csv.write('char' + csvDelimiter + 'x0' + csvDelimiter + 'y0' + csvDelimiter + 'x1' + csvDelimiter + 'y1\n')
    root = ET.parse('currpage.xml').getroot()

    last_x0 = ''
    last_x1 = ''
    last_info = {}
    create_before = False
    for font in root.findall('block/line/font'): # todo: lettrine with no font may be problem
        if font.get('name') == 'GoudyInitialen' or font.get('name') == 'CALLIG15': # GaudyInitialen is the font of the lettrines
            print('lettrine', i)
            char = font.findall('char')[0]

            quad = char.get('quad')
            # lettrine.write(char.get('c') + csvDelimiter + str(float(quad.rsplit(' ')[0]) * zoom) + csvDelimiter + str(
            #    float(quad.rsplit(' ')[1]) * zoom) + csvDelimiter + str(float(quad.rsplit(' ')[2]) * zoom) + csvDelimiter + str(
            #    float(char.get('y')) * zoom) + '\n') # SB commented out (FileNotFoundError)

        else:
            # since pymupdf gets wrong information about fake spaces and the position of letters before and after them, they have to be adjusted
            for char in font.findall('char'):
                quad = char.get('quad')

                bla = char.get('c')
                if create_before:
                    csv.write(last_info['char'] + csvDelimiter + last_info['x0'] + csvDelimiter + last_info[
                        'y0'] + csvDelimiter + str(float(quad.rsplit(' ')[2]) * zoom) + csvDelimiter + last_info[
                                  'y1'] + '\n')
                    last_info = {}
                    create_before = False
                # if a character has the same x0 and x1 position, and after it comes a space, the space doesn't exist in the real text and
                # the character has the x1 position of the space
                # if a character has the same x0 and x1 position, and after it doesn't comes a space, the space exist in the real text and
                # is added to the word
                if not (char.get('c') == ' '): # and char.get('x') == last_x0): # pymupdf/fitz sometimes sees spaces that doesn't exist that start as the same position as the former char, this is to remove them
                    y0_new = float(((float(char.get('y'))*zoom - float(quad.rsplit(' ')[1])*zoom) / 2) + float(quad.rsplit(' ')[1])*zoom) # (y1-y0)/2 + y0 ; the height of the font is double of what it should be

                    if not last_x1 == '' and round(float(quad.rsplit(' ')[0]), 1) > round(float(last_x1), 1) and (quad.rsplit(' ')[0] == quad.rsplit(' ')[2]): # SB: I had to add {not last_x1 == '' and} b/c of error--not being able to take float of last_x1 when it was empty
                        csv.write(' ' + csvDelimiter + str(float(last_x1)*zoom)+ csvDelimiter + str(y0_new) + csvDelimiter + str(float(quad.rsplit(' ')[0])*zoom) + csvDelimiter + str(float(char.get('y'))*zoom) + '\n')
                        last_info = {'char': char.get('c'), 'x0': str(float(quad.rsplit(' ')[0])*zoom), 'y0': str(y0_new), 'y1': str(float(char.get('y'))*zoom)}
                        create_before = True
                    elif abs(float(quad.rsplit(' ')[0]) - float(quad.rsplit(' ')[2])) < 0.5:
                        last_info = {'char': char.get('c'), 'x0': str(float(quad.rsplit(' ')[0])*zoom), 'y0': str(y0_new), 'y1': str(float(char.get('y'))*zoom)}
                        create_before = True
                    elif not last_x1 == '' and round(float(quad.rsplit(' ')[0]), 0) > round(float(last_x1), 0): # SB: I had to add {not last_x1 == '' and} b/c of error--not being able to take float of last_x1 when it was empty
                        csv.write(' ' + csvDelimiter + str(float(last_x1)*zoom)+ csvDelimiter + str(y0_new) + csvDelimiter + str(float(quad.rsplit(' ')[0])*zoom) + csvDelimiter + str(float(char.get('y'))*zoom) + '\n')
                        csv.write(char.get('c') + csvDelimiter + str(float(quad.rsplit(' ')[0])*zoom)+ csvDelimiter + str(y0_new) + csvDelimiter + str(float(quad.rsplit(' ')[2])*zoom) + csvDelimiter + str(float(char.get('y'))*zoom) + '\n')

                    else:
                        csv.write(char.get('c') + csvDelimiter + str(float(quad.rsplit(' ')[0])*zoom)+ csvDelimiter + str(y0_new) + csvDelimiter + str(float(quad.rsplit(' ')[2])*zoom) + csvDelimiter + str(float(char.get('y'))*zoom) + '\n')

                last_x0 = quad.rsplit(' ')[0]
                last_x1 = quad.rsplit(' ')[2]
    csv.close()

    i += 1
    if (i % 50) == 0:
        print(str(i) + ' PDFs converted')
