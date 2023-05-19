import sys, os, argparse
from PIL import Image
from pynput import keyboard

parser = argparse.ArgumentParser(
                    prog='Pluton CLI Image Viewer',
                    description='An image viewer in your terminal!',
                    epilog='SpamixOfficial 2023')
parser.add_argument('file', help='The image file to open with Pluton', type=str, action="store")
args = parser.parse_args()

if not os.path.exists(args.file):
    print("Error! File does not exist. Maybe you did a --> tpyo? <-- (typo)")
    quit()

horange = [0, 50]
verange = [0, 50]
row = 0
im = Image.open(args.file)
rgb_im = im.convert('RGBA')
pix = rgb_im.load()

result = ""
progress = 0
width, height = im.size
goal = width * height

result = ''
tresult = ''

def on_press(key):
    if key == keyboard.Key.up:
        movepic(direct="up")
    elif key == keyboard.Key.down:
        movepic(direct="down")
    elif key == keyboard.Key.right:
        movepic(direct="right")
    elif key == keyboard.Key.left:
        movepic(direct="left")

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
██████╗ ██╗   ██╗███████╗██╗██╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║██║
██████╔╝ ╚████╔╝ █████╗  ██║██║
██╔══██╗  ╚██╔╝  ██╔══╝  ╚═╝╚═╝
██████╔╝   ██║   ███████╗██╗██╗
╚═════╝    ╚═╝   ╚══════╝╚═╝╚═╝
                               
        """)
        return False


def print_to(text, side="bottom"):
    if side == "bottom":
        sys.stdout.write("\033[999B")  # Move the cursor to the bottom
        sys.stdout.write("\033[K")     # Clear the current line
        sys.stdout.write(text)         # Print the desired text
        #sys.stdout.write("\033[999A")  # Move the cursor back to the original position
        #sys.stdout.write("\033[K")     # Clear the current line
    elif side == "top":
        sys.stdout.write("\033[999A")  # Move the cursor to the top
        sys.stdout.write("\033[K")     # Clear the current line
        sys.stdout.write(text)         # Print the desired text

def printpix(rgbaval=(255, 255, 255, 1), length=1):
    if rgbaval[3] >= 0.5:
        red = rgbaval[0]
        green = rgbaval[1]
        blue = rgbaval[2]
        return f"\033[48:2::{red}:{green}:{blue}m{'  ' * length}\033[49m"
    elif rgbaval[3] <= 0.5:
        return '  '

def printtext(back=(255, 255, 255, 1), text="hi", text_color=(255, 0, 0)):
    if back[3] >= 0.5:
        red = back[0]
        green = back[1]
        blue = back[2]
        tred = text_color[0]
        tgreen = text_color[1]
        tblue = text_color[2]
        return f"\033[48;2;{red};{green};{blue}m\033[38;2;{tred};{tgreen};{tblue}m{text}\033[0m"
    elif back[3] <= 0.5:
        return ' '
        
def movepic(direct="default"):
    global row, tresult, horange, verange, progress, result
    if direct == "default":
        for i in range(verange[0], verange[1]):
            progress += 1
            for pixr in range(horange[0], horange[1]):
                tresult += printpix(pix[pixr, row])
                progress += 1
            row += 1
            tresult += "\n"
    elif not direct == "default":
        row = 0
        tresult = ""
        if direct == "right":
            if not horange[1] == width:
                horange[0] += 50
                horange[1] += 50
            if horange[1] > width:
                horange[1] = width
            for row in range(verange[0], verange[1]):
                progress += 1
                for pixr in range(horange[0], horange[1]):
                    tresult += printpix(pix[pixr, row])
                    progress += 1
                tresult += "\n"
        elif direct == "left":
            if not horange[1] - horange[0] == 50:
                if horange[1] == width:
                    horange[1] = horange[1] + (50 - (horange[1] - horange[0]))
            if not horange[0] == 0:
                horange[0] -= 50
                horange[1] -= 50
            if horange[0] < 0:
                horange[0] = 0
            for row in range(verange[0], verange[1]):
                progress += 1
                for pixr in range(horange[0], horange[1]):
                    tresult += printpix(pix[pixr, row])
                    progress += 1
                tresult += "\n"
        elif direct == "down":
            if not verange[1] == height:
                verange[0] += 50
                verange[1] += 50
            if not verange[1] - verange[0] == 50:
                if verange[1] == height:
                    verange[1] = verange[1] + (50 - (verange[1] - verange[0]))
            if verange[1] > height:
                verange[1] = height
            for row in range(verange[0], verange[1]):
                progress += 1
                for pixr in range(horange[0], horange[1]):
                    tresult += printpix(pix[pixr, row])
                    progress += 1
                #row += 1
                tresult += "\n"
        elif direct == "up":
            if not verange[1] - verange[0] == 50:
                if verange[1] == height:
                    verange[1] = verange[1] + (50 - (verange[1] - verange[0]))
            if not verange[0] == 0:
                verange[0] -= 50
                verange[1] -= 50
            if verange[0] < 0:
                verange[0] = 0
            for row in range(verange[0], verange[1]):
                progress += 1
                for pixr in range(horange[0], horange[1]):
                    tresult += printpix(pix[pixr, row])
                    progress += 1
                #row += 1
                tresult += "\n"       
        os.system('cls' if os.name == 'nt' else 'clear')
        print(tresult)
        print_to(result)
            

#for i in range(0, 50):
#    progress += 1
#    for pixr in range(0, 50):
#        tresult += printpix(pix[pixr, row])
#        progress += 1
#    row += 1
#    tresult += "\n"
os.system('cls' if os.name == 'nt' else 'clear')
movepic()

print(tresult)

# Creating Interface
#result += printpix(length=31)   
result += "\n"
result += printtext((255, 255, 255, 1), "↑", (0, 0, 0))
result += f"\033[38;2;{255};{255};{255}m Up\033[0m"
result += "  "
result += printtext((255, 255, 255, 1), "↓", (0, 0, 0))
result += f"\033[38;2;{255};{255};{255}m Down\033[0m"
result += "  "
result += printtext((255, 255, 255, 1), "→", (0, 0, 0))
result += f"\033[38;2;{255};{255};{255}m Right\033[0m"
result += "  "
result += printtext((255, 255, 255, 1), "←", (0, 0, 0))
result += f"\033[38;2;{255};{255};{255}m Left\033[0m"
result += "  "
result += printtext((255, 255, 255, 1), "Esc", (0, 0, 0))
result += f"\033[38;2;{255};{255};{255}m Exit\033[0m"
result += "\n"
#result += printpix(length=1)
#result += printpix(length=15) 
print_to(result)
#sys.stdout.write("\033[C") 
#print(len(result))
#while True:
#    tinput = input().lower()
#    if tinput == "e":
#        quit()
#    elif tinput == "z":
 #       quit()
 #   elif tinput == "x":
 #       quit()


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
