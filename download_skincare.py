import os
import shutil
import pandas as pd

dataset_path = r"C:\Users\acer\Downloads\myntradataset"
csv_path = os.path.join(dataset_path, "styles.csv")
images_path = os.path.join(dataset_path, "images")

output_path = r"C:\Users\acer\OneDrive\Desktop\smart fashion price comparison using AI\dataset_clean\skincare"

os.makedirs(output_path, exist_ok=True)

df = pd.read_csv(csv_path, on_bad_lines="skip")

categories = [
    "Face Moisturisers",
    "Face Wash and Cleanser",
    "Sunscreen",
    "Eye Cream",
    "Body Lotion",
    "Face Serum and Gel"
]

count = 0

for category in categories:
    rows = df[
        df["articleType"].astype(str).str.lower() == category.lower()
    ]

    for _, row in rows.iterrows():
        image_id = str(row["id"])
        image_file = os.path.join(images_path, image_id + ".jpg")

        if os.path.exists(image_file):
            destination = os.path.join(
                output_path,
                image_id + ".jpg"
            )
            shutil.copy2(image_file, destination)
            count += 1

print("Skincare images copied successfully!")
print("Total images copied:", count)
