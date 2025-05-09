from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from .core import alpha_layer_attack, adversarial_pattern_attack
import os

class ShadowMaskUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.filechooser = FileChooserIconView()
        self.add_widget(self.filechooser)
        self.img = Image()
        self.add_widget(self.img)
        self.alpha_btn = Button(text="Apply Alpha Layer Attack")
        self.alpha_btn.bind(on_press=self.alpha_attack)
        self.add_widget(self.alpha_btn)
        self.adv_btn = Button(text="Apply Adversarial Pattern (FGSM)")
        self.adv_btn.bind(on_press=self.adv_attack)
        self.add_widget(self.adv_btn)
        self.status = Label(text="Select an image and choose an attack.")
        self.add_widget(self.status)

    def alpha_attack(self, instance):
        selected = self.filechooser.selection
        if len(selected) < 2:
            self.status.text = "Select two images: visible and AI."
            return
        visible_img, ai_img = selected[:2]
        output_path = os.path.join(os.path.dirname(visible_img), "output_alpha.png")
        try:
            alpha_layer_attack(visible_img, ai_img, output_path)
            self.img.source = output_path
            self.status.text = f"Alpha attack applied: {output_path}"
        except Exception as e:
            self.status.text = f"Error: {e}"

    def adv_attack(self, instance):
        selected = self.filechooser.selection
        if not selected:
            self.status.text = "Select an image for adversarial attack."
            return
        input_img = selected[0]
        output_path = os.path.join(os.path.dirname(input_img), "output_adv.png")
        try:
            adversarial_pattern_attack(input_img, output_path, epsilon=0.03, label_idx=0)
            self.img.source = output_path
            self.status.text = f"Adversarial attack applied: {output_path}"
        except Exception as e:
            self.status.text = f"Error: {e}"

class ShadowMaskApp(App):
    def build(self):
        return ShadowMaskUI()

if __name__ == "__main__":
    ShadowMaskApp().run()
