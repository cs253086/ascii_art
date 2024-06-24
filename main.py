import math
from PIL import Image
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

# Define ASCII characters to represent the pixels
ASCII_CHARS = np.asarray(list(' .,:irs?@9B&#'))

def resize_image(image, new_width=100):
    """
    Resize the image while maintaining the aspect ratio.
    """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def image_to_ascii(image_path, width=100):
    """
    Convert the image to an ASCII art.
    """
    # Open the image and resize it
    image = Image.open(image_path)
    image = resize_image(image, new_width=width)

    # Convert the image to grayscale
    image = image.convert('L')

    # Get the pixels as a list
    pixels = image.getdata()

    # Convert the pixels to ASCII characters
    min_pixel = min(pixels)
    max_pixel = max(pixels)
    # Scale pixel values to range between 0 and 1
    scaled_pixels = [(pixel - min_pixel) / (max_pixel - min_pixel) for pixel in pixels]

    # Map scaled pixel values to ASCII characters
    ascii_pixels = [ASCII_CHARS[math.floor(pixel * (len(ASCII_CHARS) - 1))] for pixel in scaled_pixels]

    ascii_pixels = ''.join(ascii_pixels)

    # Split the ASCII art into lines
    lines = [ascii_pixels[i:i + width] for i in range(0, len(ascii_pixels), width)]
    ascii_art = '\n'.join(lines)

    return ascii_art

class AsciiArtApp(App):
    def build(self):
        self.title = 'ASCII Art Converter'
        self.layout = BoxLayout(orientation='vertical')

        self.scrollview = ScrollView(size_hint=(1, 0.9))
        self.label = Label(text='Select an image to convert to ASCII art', font_size='10sp', size_hint_y=None, font_name='RobotoMono-Regular')
        self.scrollview.add_widget(self.label)
        self.layout.add_widget(self.scrollview)

        self.button = Button(text='Select Image', size_hint=(1, 0.1))
        self.button.bind(on_press=self.open_file_chooser)
        self.layout.add_widget(self.button)

        return self.layout

    def open_file_chooser(self, instance):
        filechooser = FileChooserIconView()
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(filechooser)

        select_button = Button(text='Select', size_hint=(1, 0.1))
        popup_layout.add_widget(select_button)

        popup = Popup(title='Choose an image', content=popup_layout, size_hint=(0.9, 0.9))

        def on_file_selection(instance, selection):
            if selection:
                image_path = selection[0]
                ascii_art = image_to_ascii(image_path)
                self.layout.remove_widget(self.button)  # Remove the Select Image button
                self.label.text = ascii_art
                self.label.font_name = 'RobotoMono-Regular'  # Ensure monospaced font
                self.label.font_size = '6sp'
                self.label.texture_update()
                self.label.height = self.label.texture_size[1]
                self.scrollview.scroll_to(self.label)
                popup.dismiss()

        filechooser.bind(on_selection=on_file_selection)
        select_button.bind(on_press=lambda x: on_file_selection(filechooser, filechooser.selection))

        popup.open()

if __name__ == '__main__':
    AsciiArtApp().run()
