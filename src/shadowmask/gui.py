from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from .core import alpha_layer_attack  # Import core logic

class ShadowMaskUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.filechooser = FileChooserIconView()
        self.add_widget(self.filechooser)
        self.img = Image()
        self.add_widget(self.img)
        self.process_btn = Button(text="Apply ShadowMask")
        self.process_btn.bind(on_press=self.process_image)
        self.add_widget(self.process_btn)
        self.status = Label(text="Select an image and click the button.")
        self.add_widget(self.status)

    def process_image(self, instance):
        selected = self.filechooser.selection
        if not selected:
            self.status.text = "No image selected!"
            return
        img_path = selected[0]
        self.img.source = img_path
        # Example: call processing function and update output
        # alpha_layer_attack(img_path, ...)
        self.status.text = f"Processed: {img_path}"

class ShadowMaskApp(App):
    def build(self):
        return ShadowMaskUI()

if __name__ == "__main__":
    ShadowMaskApp().run()
