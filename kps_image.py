import insightface
import cv2
import numpy as np

class ImageToKps:
    def __init__(self):
        self.model = insightface.app.FaceAnalysis()
        self.model.prepare(ctx_id=-1)  # Use ctx_id=-1 for CPU

    def get_kps_all_faces(self, image_path):
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to load!")
        faces = self.model.get(image)
        kps_list = [];
        for idx, face in enumerate(faces):
            print(f"Face {idx + 1}:")
            kps_list.append(face.kps)
        print(kps_list)
        return kps_list

    def draw_rectangles(self, input_image_path, output_path):
        image = cv2.imread(input_image_path)
        if image is None:
            raise ValueError("Image not found or unable to load!")
        kps_list = self.get_kps_all_faces(input_image_path)
        for kps in kps_list:
            kps = np.array(kps)  # Convert to numpy array for easier calculations
            x_min, y_min = np.min(kps, axis=0).astype(int)  # Convert to integers
            x_max, y_max = np.max(kps, axis=0).astype(int)  # Convert to integers
            # Draw rectangle
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

        # Optionally save the output
        cv2.imwrite(output_path, image)
        return image
