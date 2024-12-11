import insightface
import cv2

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

print("Keypoints for all detected faces:")
for idx, face in enumerate(faces):
    print(f"Face {idx + 1}:")
    print(face.kps)

# Optional: Draw keypoints on the image
# for face in faces:
#     for i, point in enumerate(face.kps):
#         print(f"Point {i}: {point}")

# Display the image with keypoints
cv2.imshow("Keypoints", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
