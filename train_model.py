import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from model_config import CLASS_NAMES, NUM_CLASSES


# =========================
# 1. Dataset Settings
# =========================

DATASET_DIR = "dataset_clean"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 15


# =========================
# 2. Load Training Dataset
# =========================

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    labels="inferred",
    label_mode="int",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="training",
    seed=123
)


# =========================
# 3. Load Validation Dataset
# =========================

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    labels="inferred",
    label_mode="int",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    subset="validation",
    seed=123
)


# =========================
# 4. Improve Performance
# =========================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)


# =========================
# 5. Data Augmentation
# =========================

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])


# =========================
# 6. Build AI Model
# =========================

model = keras.Sequential([
    layers.Input(shape=(224, 224, 3)),

    data_augmentation,

    layers.Rescaling(1.0 / 255),

    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),

    layers.Dense(NUM_CLASSES, activation="softmax")
])


# =========================
# 7. Compile Model
# =========================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# =========================
# 8. Display Model
# =========================

model.summary()


# =========================
# 9. Train Model
# =========================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)


# =========================
# 10. Save Trained Model
# =========================

model.save("fashion_model.keras")

print("\nTraining completed successfully!")
print("Model saved as: fashion_model.keras")