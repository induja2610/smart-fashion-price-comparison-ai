from datasets import load_dataset
from pathlib import Path

print("Loading Fashion Product Images dataset...")

dataset = load_dataset(
    "ashraq/fashion-product-images-small",
    split="train"
)

print("Dataset loaded!")

# Shirt folders are one level above the tshirt folder
base = Path("../shirt")

folders = {
    "Men": base / "men",
    "Women": base / "women",
    "Boys": base / "kids_boy",
    "Girls": base / "kids_girl"
}

for folder in folders.values():
    folder.mkdir(parents=True, exist_ok=True)

count = {
    "Men": 0,
    "Women": 0,
    "Boys": 0,
    "Girls": 0
}

MAX_IMAGES = 100

for item in dataset:

    gender = str(item["gender"])
    article = str(item["articleType"]).lower()

    # Select shirt items, but exclude T-shirts
    if "shirt" not in article:
        continue

    if "tshirt" in article or "t-shirt" in article:
        continue

    if gender not in folders:
        continue

    if count[gender] >= MAX_IMAGES:
        continue

    image = item["image"]

    filename = f"{gender.lower()}_{count[gender] + 1}.jpg"

    image.save(folders[gender] / filename)

    count[gender] += 1

    print(f"{gender}: {count[gender]}")

    if all(count[g] >= MAX_IMAGES for g in count):
        break

print("\nDONE!")
print(count)