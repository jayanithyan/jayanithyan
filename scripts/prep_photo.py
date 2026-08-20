from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = input_path.with_name("source-prepped.png")

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    print("Removing background...")

    with open(input_path, "rb") as file:
        input_data = file.read()

    output_data = remove(input_data)

    temp_path = input_path.with_name("temp-no-bg.png")
    with open(temp_path, "wb") as file:
        file.write(output_data)

    print("Processing contrast...")

    image = cv2.imread(str(temp_path), cv2.IMREAD_UNCHANGED)

    if image is None:
        print("Could not read processed image.")
        sys.exit(1)

    if image.shape[2] == 4:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]
    else:
        bgr = image
        alpha = np.full(
            (image.shape[0], image.shape[1]),
            255,
            dtype=np.uint8
        )

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    white = np.full_like(enhanced, 255)

    alpha_float = alpha.astype(np.float32) / 255.0

    composited = (
        enhanced.astype(np.float32) * alpha_float
        + white.astype(np.float32) * (1 - alpha_float)
    )

    composited = np.clip(composited, 0, 255).astype(np.uint8)

    Image.fromarray(composited).save(output_path)

    temp_path.unlink()

    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()