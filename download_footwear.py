import os
import shutil
import pandas as pd

# Dataset location
dataset_path = r"C:\Users\acer\Downloads\myntradataset"

# CSV
csv_path = os.path.join(dataset_path, "styles.csv")

# Images folder
images_path = os.path.join(dataset_path, "images")

# Project footwear folder
output_path = r"C:\Users\acer\OneDrive\Desktop\smart fashion price comparison using AI\dataset_clean\footwear"

# Create output folder
os.makedirs(output_path, exist_ok=True)

# Read CSV
df = pd.read_csv(csv_path, on_bad_lines="skip")

# Footwear categories
footwear_categories = [
    "Casual Shoes",
    "Sports Shoes",
    "Heels",
    "Flip Flops",
    "Sandals",
    "Formal Shoes",
    "Flats",
    "Sports Sandals"
]

# Copy 25 images from each category
for category in footwear_categories:

    category_images = df[
        df["articleType"].str.lower() == category.lower()
    ].head(25)

    for _, row in category_images.iterrows():

        image_id = str(row["id"])
        image_file = os.path.join(
            images_path,
            image_id + ".jpg"
        )

        if not os.path.exists(image_file):
            continue

        destination = os.path.join(
            output_path,
            image_id + ".jpg"
        )

        shutil.copy2(image_file, destination)

print("Footwear images copied successfully! ✅")
print("Total target images: 200")
