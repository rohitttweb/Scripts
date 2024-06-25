import cv2
import os

imgarr = []  # list to store rows of images
frame_no = 0
# loop through the folders and images
for i in range(1, 18):
    imgarr_row = []  # list to store images in a row
    for x in range(1, 18):
        frame_no = frame_no + 1
        img = cv2.imread("pokemone/ep1/" + str(frame_no) + " frame.png")
        # Resize the image
        img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5)
        imgarr_row.append(img)
    imgarr.append(imgarr_row)

# Function to vertically concatenate and then horizontally concatenate images
def concat_vh(list_2d):
    # Vertically concatenate rows of images
    vconcatenated = [cv2.hconcat(list_h) for list_h in list_2d]
    # Horizontally concatenate rows of images
    return cv2.vconcat(vconcatenated)

# Concatenate images
img_tile = concat_vh(imgarr)

# Save the concatenated image to a folder
output_folder = "pokemone/ep1/concated"
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
output_path = os.path.join(output_folder, "concatenated_image.png")
cv2.imwrite(output_path, img_tile)

print(f"Concatenated image saved at: {output_path}")
