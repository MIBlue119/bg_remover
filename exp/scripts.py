from rembg import remove
from PIL import Image


def remove_img_background(input_path: str, output_path: str):
    # Open the jpeg file
    image = Image.open(input_path)
    # Remove the background
    result = remove(image)
    # Save the image
    result.save(output_path, "PNG")


if __name__ == "__main__":
    import os
    from pathlib import Path
    import logging
    from tqdm import tqdm

    # Set the logging level
    logging.basicConfig(level=logging.INFO)
    # Set the log file path
    logging.basicConfig(
        filename="./app.log",
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
    )

    pics_dir_path = (
        "/Users/weirenlan/Desktop/self_practice/unlimiter/picture_converter/pics/元鼎-相片庫"
    )

    export_dir_path = (
        Path(
            "/Users/weirenlan/Desktop/self_practice/unlimiter/picture_converter/pics/processed"
        )
        / "元鼎-相片庫-去背"
    )
    os.makedirs(export_dir_path, exist_ok=True)

    # List the image files in the directory
    pics = os.listdir(pics_dir_path)

    for pic in tqdm(pics):
        try:
            # Get the pic file name
            pic_name = pic.split(".")[0]
            remove_img_background(
                os.path.join(pics_dir_path, pic),
                os.path.join(export_dir_path, f"{pic_name}.png"),
            )
        except Exception as e:
            # Log the error
            logging.error(e)
