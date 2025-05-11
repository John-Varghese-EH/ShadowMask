import os

def apply_alpha_attack(image_path, output_path=None):
    """
    Dummy alpha attack: just copies the image (replace with real logic).
    """
    if not output_path:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_alpha{ext}"
    with open(image_path, "rb") as fin, open(output_path, "wb") as fout:
        fout.write(fin.read())
    return output_path
