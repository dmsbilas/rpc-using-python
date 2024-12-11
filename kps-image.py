import insightface
import cv2
import numpy as np

# Load the InsightFace model
model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=-1)  # Use ctx_id=-1 for CPU

# Load the image
image_path = "cup-1.jpeg"  # Replace with the path to your image
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image not found or unable to load!")

# Detect faces and extract keypoints
faces = model.get(image)
# print("faces")
# print(faces)
kps_list = [];
print("Keypoints for all detected faces:")
for idx, face in enumerate(faces):
    print(f"Face {idx + 1}:")
    print(face.kps)
    kps_list.append(face.kps)
# Optional: Draw keypoints on the image
# Draw rectangles based on keypoints
for kps in kps_list:
    kps = np.array(kps)  # Convert to numpy array for easier calculations
    x_min, y_min = np.min(kps, axis=0).astype(int)  # Convert to integers
    x_max, y_max = np.max(kps, axis=0).astype(int)  # Convert to integers
    
    # Draw rectangle
    cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

# Optionally save the output
output_path = "output_image.jpg"
cv2.imwrite(output_path, image)

# Display the image with keypoints
cv2.imshow("Keypoints", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
