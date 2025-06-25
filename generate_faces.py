import cv2
import numpy as np

# Image size
img_size = (400, 400, 3)

# Colors
face_color = (255, 224, 189)
background_color = (255, 255, 255)
eyes_color = (0, 0, 0)
mouth_color = (0, 0, 0)

# Face coordinates
center = (200, 200)
axes = (100, 130)

# Function to draw a face with different expressions
def draw_face(expression='neutral'):
    img = np.full(img_size, background_color, dtype=np.uint8)
    # Face
    cv2.ellipse(img, center, axes, 0, 0, 360, face_color, -1)
    # Eyes
    cv2.circle(img, (150, 170), 18, (255, 255, 255), -1)
    cv2.circle(img, (250, 170), 18, (255, 255, 255), -1)
    cv2.circle(img, (150, 170), 8, eyes_color, -1)
    cv2.circle(img, (250, 170), 8, eyes_color, -1)
    # Mouth
    if expression == 'happy':
        cv2.ellipse(img, (200, 250), (50, 25), 0, 0, 180, mouth_color, 4)
    elif expression == 'sad':
        cv2.ellipse(img, (200, 270), (50, 25), 0, 0, -180, mouth_color, 4)
    elif expression == 'surprised':
        cv2.ellipse(img, (200, 250), (25, 35), 0, 0, 360, mouth_color, 4)
    else:  # neutral
        cv2.line(img, (160, 250), (240, 250), mouth_color, 4)
    return img

# List of expressions
expressions = ['neutral', 'happy', 'sad', 'surprised']
frames = []

for expr in expressions:
    frames.append(draw_face(expr))

# Last frame: deliberate corruption (add noise and distortions)
def corrupt_frame(img):
    corrupted = img.copy()
    # Add noise
    noise = np.random.randint(0, 80, img.shape, dtype='uint8')
    corrupted = cv2.add(corrupted, noise)
    # Draw "glitch" lines
    for i in range(10):
        y = np.random.randint(0, img.shape[0])
        cv2.line(corrupted, (0, y), (img.shape[1], y), (0, 0, 255), 2)
    # Shuffle part of the image
    x1 = np.random.randint(0, 300)
    x2 = x1 + 50
    corrupted[:, x1:x2] = np.roll(corrupted[:, x1:x2], shift=20, axis=0)
    return corrupted

corrupted = corrupt_frame(frames[-1])
frames.append(corrupted)

# Save all frames
for idx, frame in enumerate(frames):
    cv2.imwrite(f'face_frame_{idx+1}.png', frame)

print("Generation complete. Frames saved as face_frame_1.png ... face_frame_5.png")
