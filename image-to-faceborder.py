import insightface
import cv2
import numpy as np

# Load the InsightFace model
model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=-1)  # ctx_id=0 uses GPU if available, use ctx_id=-1 for CPU

# Load an image
image_path = "cup-1.jpeg"  # Replace with the path to your image
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image not found or unable to load!")

# Perform face analysis
faces = model.get(image)

print("faces")
print(faces)

# Draw the results on the image
for face in faces:
    bbox = face.bbox.astype(int)  # Bounding box for the face
    cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

    # Extract landmarks
    for point in face.landmark:
        cv2.circle(image, tuple(point.astype(int)), 2, (0, 0, 255), -1)

    # Display confidence score
    confidence_text = f"Conf: {face.det_score:.2f}"
    cv2.putText(image, confidence_text, (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# Display the results
cv2.imshow("Detected Faces", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
